#!/usr/bin/env python3
"""
3D Router — Context Saver v7.0.0
Routes prompts to optimal (model × effort × version) combination.
"""

import os
import sys
import json
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RoutingDecision:
    """Result of 3D routing analysis"""
    model: str      # haiku, sonnet, opus
    effort: str     # low, medium, high, max
    version: str    # 4.5, 4.6
    agents: List[str]
    token_estimate: int
    reason: str


# Version mapping: model → version
VERSION_MAP = {
    'haiku': '4.5',
    'sonnet': '4.6',
    'opus': '4.6',
}

# Model IDs for reference
MODEL_IDS = {
    'haiku': 'claude-haiku-4-5-20251001',
    'sonnet': 'claude-sonnet-4-6',
    'opus': 'claude-opus-4-6',
}


class UnifiedRouter:
    """Routes prompts to optimal model + effort + version combination"""

    def __init__(self):
        self.router_dir = Path.home() / '.claude' / 'router'
        self.config_path = self.router_dir / 'config.yaml'
        self.state_file = self.router_dir / 'state.json'
        self.log_file = self.router_dir / 'router.log'

        self.router_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        if not self.config_path.exists():
            return {}
        if not _HAS_YAML:
            self._log("WARNING: PyYAML not installed. Using fallback routing. Run: pip3 install pyyaml")
            return {}
        with open(self.config_path) as f:
            return yaml.safe_load(f) or {}

    def _log(self, message: str):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

    def _get_patterns(self, section: str, key: str) -> List[str]:
        """Safe pattern extraction from config sections."""
        entries = self.config.get(section, {}).get(key, [])
        if not entries or not isinstance(entries, list):
            return []
        first = entries[0]
        if not isinstance(first, dict):
            return []
        return first.get('pattern', [])

    def _estimate_model(self, prompt: str) -> Tuple[str, int]:
        """Estimate task complexity → (model, token_estimate)"""
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())

        # Check for misar-dev slash commands first (3D)
        misar_commands = self.config.get('misar_dev_commands', {})
        for cmd, routing in misar_commands.items():
            if cmd in prompt_lower:
                if isinstance(routing, dict):
                    model = routing.get('model', 'sonnet')
                elif isinstance(routing, str):
                    model = routing
                else:
                    continue
                token_est = 15000 if model == 'opus' else 5000 if model == 'sonnet' else 1000
                return model, token_est

        # Keyword-based routing
        haiku_patterns = self._get_patterns('model_routing', 'haiku')
        if any(p in prompt_lower for p in haiku_patterns) or word_count < 10:
            return 'haiku', 1000

        opus_patterns = self._get_patterns('model_routing', 'opus')
        if any(p in prompt_lower for p in opus_patterns) or word_count > 100:
            return 'opus', 15000

        return 'sonnet', 5000

    def _estimate_effort(self, prompt: str, model: str) -> str:
        """Estimate effort level based on prompt patterns and model."""
        prompt_lower = prompt.lower()

        # Check misar-dev commands for explicit effort
        misar_commands = self.config.get('misar_dev_commands', {})
        for cmd, routing in misar_commands.items():
            if cmd in prompt_lower and isinstance(routing, dict):
                return routing.get('effort', 'medium')

        # Pattern-based effort detection
        max_patterns = self._get_patterns('effort_routing', 'max')
        if any(p in prompt_lower for p in max_patterns):
            return 'max'

        high_patterns = self._get_patterns('effort_routing', 'high')
        if any(p in prompt_lower for p in high_patterns):
            return 'high'

        low_patterns = self._get_patterns('effort_routing', 'low')
        if any(p in prompt_lower for p in low_patterns):
            return 'low'

        # Default effort based on model
        if model == 'opus':
            return 'high'
        elif model == 'haiku':
            return 'low'
        return 'medium'

    def _resolve_version(self, model: str) -> str:
        """Resolve version for a model."""
        # Check config first
        version_routing = self.config.get('version_routing', {})
        for ver, info in version_routing.items():
            if isinstance(info, dict) and model in info.get('models', []):
                return ver
        # Fallback to hardcoded map
        return VERSION_MAP.get(model, '4.6')

    def _match_agents(self, prompt: str) -> List[str]:
        """Find matching agents for prompt"""
        prompt_lower = prompt.lower()
        matched_agents = set()
        priorities = {}

        routing_rules = self.config.get('routing_rules', {})

        for category, rule in routing_rules.items():
            patterns = rule.get('patterns', [])
            if any(pattern.lower() in prompt_lower for pattern in patterns):
                agents = rule.get('agents', [])
                priority = rule.get('priority', 'medium')
                for agent in agents:
                    matched_agents.add(agent)
                    priorities[agent] = priority

        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        return sorted(
            matched_agents,
            key=lambda a: priority_order.get(priorities.get(a, 'medium'), 2)
        )

    def _add_dependencies(self, agents: List[str]) -> List[str]:
        dependencies = self.config.get('agent_dependencies', {})
        all_agents = set(agents)
        for agent in agents:
            deps = dependencies.get(agent, [])
            all_agents.update(deps)
        return list(all_agents)

    def _apply_token_budget(self, agents: List[str], max_tokens: int = 12000) -> List[str]:
        estimated_tokens = len(agents) * 500
        if estimated_tokens <= max_tokens:
            return agents
        max_agents = max_tokens // 500
        self._log(f"Token budget exceeded, limiting to {max_agents} agents")
        return agents[:max_agents]

    def _check_token_budget(self, transcript_path: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """Check token budget — return (model_override, effort_override) if needed."""
        if not transcript_path or not Path(transcript_path).exists():
            return None
        try:
            size = Path(transcript_path).stat().st_size
            tokens = size // 4
            usage_pct = (tokens / 200000) * 100

            budget_overrides = self.config.get('token_budget', {}).get('budget_overrides', {})

            if usage_pct >= 90:
                override = budget_overrides.get('above_90', {})
                return (override.get('model', 'haiku'), override.get('effort', 'low'))
            elif usage_pct >= 70:
                override = budget_overrides.get('above_70', {})
                return (override.get('model', 'haiku'), override.get('effort', 'low'))
            elif usage_pct >= 40:
                # Return None but log the cap (handled in route())
                self._log(f"Budget at {usage_pct:.0f}% — capping at sonnet+medium")
                return None
        except Exception:
            pass
        return None

    def route(self, prompt: str, transcript_path: Optional[str] = None) -> RoutingDecision:
        """Main 3D routing logic — returns optimal model + effort + version + agents"""
        self._log(f"Routing prompt: {prompt[:100]}...")

        # Step 1: Determine model
        model, token_estimate = self._estimate_model(prompt)

        # Step 2: Determine effort
        effort = self._estimate_effort(prompt, model)

        # Step 3: Resolve version
        version = self._resolve_version(model)

        # Step 4: Check token budget for overrides
        budget_override = self._check_token_budget(transcript_path)
        if budget_override:
            old = f"{model}+{effort}"
            model, effort = budget_override
            version = self._resolve_version(model)
            self._log(f"Budget override: {old} -> {model}+{effort}")

        # Step 5: Match agents
        matched_agents = self._match_agents(prompt)

        if matched_agents:
            matched_agents = self._add_dependencies(matched_agents)
        else:
            fallback = self.config.get('fallback', {})
            matched_agents = fallback.get('agents', ['general-purpose'])
            if not budget_override:
                model = fallback.get('model', 'sonnet')
                effort = fallback.get('effort', 'medium')
                version = fallback.get('version', '4.6')

        # Step 6: Apply agent token budget
        budget = self.config.get('token_budget', {}).get('max_agents_context', 12000)
        final_agents = self._apply_token_budget(matched_agents, budget)

        decision = RoutingDecision(
            model=model,
            effort=effort,
            version=version,
            agents=final_agents,
            token_estimate=token_estimate,
            reason=f"{model}+{effort}+{version} | {len(final_agents)} agents"
        )

        self._log(f"Decision: {model}+{effort}+{version}, agents={len(final_agents)}, est={token_estimate}")
        self._save_state(decision)
        return decision

    def _save_state(self, decision: RoutingDecision):
        state = {
            'model': decision.model,
            'effort': decision.effort,
            'version': decision.version,
            'model_id': MODEL_IDS.get(decision.model, 'unknown'),
            'agents': decision.agents,
            'token_estimate': decision.token_estimate,
            'reason': decision.reason,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Context Saver — 3D Router (model×effort×version)')
    parser.add_argument('prompt', nargs='?', help='User prompt to route')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--model-only', action='store_true', help='Output only the model name')
    parser.add_argument('--badge', action='store_true', help='Output 3D badge format')

    args = parser.parse_args()

    if not args.prompt:
        args.prompt = sys.stdin.read().strip()

    if not args.prompt:
        print("Error: No prompt provided", file=sys.stderr)
        sys.exit(1)

    router = UnifiedRouter()
    decision = router.route(args.prompt)

    if args.model_only:
        print(decision.model)
    elif args.badge:
        effort_short = {'low': 'low', 'medium': 'med', 'high': 'high', 'max': 'max'}
        print(f"[{decision.model}|{effort_short.get(decision.effort, decision.effort)}|{decision.version}]")
    elif args.json:
        output = {
            'model': decision.model,
            'effort': decision.effort,
            'version': decision.version,
            'model_id': MODEL_IDS.get(decision.model, 'unknown'),
            'agents': decision.agents,
            'token_estimate': decision.token_estimate,
            'reason': decision.reason
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Model:    {decision.model} ({MODEL_IDS.get(decision.model, '?')})")
        print(f"Effort:   {decision.effort}")
        print(f"Version:  {decision.version}")
        print(f"Badge:    [{decision.model}|{decision.effort}|{decision.version}]")
        print(f"Agents:   {', '.join(decision.agents) if decision.agents else 'none'}")
        print(f"Tokens:   ~{decision.token_estimate}")
        print(f"Reason:   {decision.reason}")


if __name__ == '__main__':
    main()
