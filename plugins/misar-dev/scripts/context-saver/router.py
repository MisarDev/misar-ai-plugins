#!/usr/bin/env python3
"""
4D Router — Context Saver v8.3.0
Routes prompts to optimal (model × effort × version × context_window) combination.
4th dimension: 1M-context variants of sonnet 4.6 / opus 4.7 for large-codebase work.
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
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RoutingDecision:
    """Result of 5D routing analysis (model × effort × version × context × dispatch)"""
    model: str          # haiku, sonnet, opus
    effort: str         # low, medium, high, max
    version: str        # 4.5, 4.6, 4.7
    agents: List[str]
    token_estimate: int
    reason: str
    context_1m: bool = False        # True → 1M-context variant
    provider: str = 'claude'         # claude | misarcoder | assisters
    model_id: str = ''
    # 5th dimension: dispatch strategy
    dispatch: str = 'inline'         # inline | subagent | parallel | external
    subagent_type: str = ''          # Agent subagent_type to dispatch to
    parallel_count: int = 1          # number of parallel Agent calls
    dispatch_reason: str = ''        # why this dispatch was chosen


# Version mapping: model → default version (200K context)
VERSION_MAP = {
    'haiku': '4.5',
    'sonnet': '4.6',
    'opus': '4.7',
}

# Standard 200K-context model IDs
MODEL_IDS = {
    'haiku': 'claude-haiku-4-5-20251001',
    'sonnet': 'claude-sonnet-4-6',
    'opus': 'claude-opus-4-7',
}

# 1M-context variant IDs (sonnet 4.6 + opus 4.7 only — haiku has no 1M variant)
MODEL_IDS_1M = {
    'sonnet': 'claude-sonnet-4-6[1m]',
    'opus': 'claude-opus-4-7[1m]',
}

# Triggers that force 1M context window
PATTERNS_1M = [
    'full-suite', 'full suite', 'full audit', 'audit all', 'audit the whole',
    'monorepo', 'entire codebase', 'whole codebase', 'across all files',
    'compliance audit', '49 frameworks', 'all 49', 'all repos', 'all packages',
    'large codebase', 'massive', '1m context', '1m window', '--1m',
    'multi-repo', 'multi-service migration', 'cross-repo',
]

# Tasks Claude should NEVER handle — route to MisarCoder/Assisters
EXTERNAL_PROVIDER_PATTERNS = {
    'misarcoder': [
        'commit message', 'pr description', 'pull request description',
        'changelog', 'release notes', 'readme section', 'api docs',
        'explain this code', 'summarize this', 'simple question',
    ],
    'assisters': [
        'blog post', 'write a blog', 'write an article', 'write a guide',
        'write a tutorial', 'long-form', 'newsletter', 'email campaign',
        'marketing copy', 'landing page copy', 'documentation site',
    ],
}

# 5th Dimension: Task → Dispatch Matrix
# Each entry: (patterns, dispatch_type, subagent_type, parallel_count, reason)
# dispatch_type: 'subagent' | 'parallel' | 'inline'
# subagent_type: Agent subagent_type string (e.g. 'Explore', 'misar-dev:security-agents')
# parallel_count: how many parallel Agent calls to suggest
DISPATCH_MATRIX = [
    # File exploration / search — Explore subagent keeps reads out of main context
    (['find files', 'search for', 'where is', 'locate the', 'which file', 'list all files',
      'find the file', 'grep for', 'search codebase', 'find the function', 'find the component',
      'find the handler', 'find the service', 'find the module', 'find the class', 'find the route',
      'find where', 'look for the', 'show me where', 'where does', 'where can i find',
      'which files contain', 'what files', 'look up the file'],
     'subagent', 'Explore', 1, 'File search isolated in Explore subagent (no context pollution)'),

    # Security — dedicated security-agents subagent
    (['security audit', 'pentest', 'penetration test', 'vulnerability', 'security review',
      'security check', 'secret scan', 'dependency audit', 'security headers', 'sast scan'],
     'subagent', 'misar-dev:security-agents', 1, 'Security analysis in dedicated subagent'),

    # Code review — code-reviewer subagent
    (['review code', 'code review', 'review the code', 'review my code',
      'review this code', 'review pull request', 'review pr', 'check this code'],
     'subagent', 'feature-dev:code-reviewer', 1, 'Code review isolated in code-reviewer subagent'),

    # QA / quality / bugs
    (['qa audit', 'quality audit', 'code quality', 'technical debt', 'bug detective',
      'standards compliance', 'code standards', 'find bugs'],
     'subagent', 'misar-dev:qa-agents', 1, 'QA analysis in dedicated qa-agents subagent'),

    # UI/UX design audit
    (['ui audit', 'ux audit', 'ui/ux audit', 'design audit', 'accessibility audit',
      'component audit', 'layout audit', 'dark mode audit', 'spacing audit', 'typography audit'],
     'subagent', 'misar-dev:uiux-agents', 1, 'UI/UX analysis in dedicated uiux-agents subagent'),

    # Testing
    (['test coverage', 'write tests', 'unit test', 'integration test', 'e2e test',
      'regression test', 'testing audit', 'add tests for', 'test the'],
     'subagent', 'misar-dev:tester-agents', 1, 'Test work in dedicated tester-agents subagent'),

    # Marketing / SEO audit
    (['seo audit', 'marketing audit', 'seo analysis', 'marketing analysis',
      'growth audit', 'content marketing audit', 'ahrefs', 'ai search optimization'],
     'subagent', 'misar-dev:marketing-agents', 1, 'Marketing/SEO in dedicated marketing-agents subagent'),

    # Product strategy
    (['product audit', 'product strategy', 'feature prioritization', 'product design review',
      'product manager review', 'product analysis', 'roadmap review'],
     'subagent', 'misar-dev:product-agents', 1, 'Product analysis in dedicated product-agents subagent'),

    # Brand audit
    (['brand audit', 'brand review', 'brand analysis', 'voice audit', 'logo review',
      'brand guidelines review', 'brand consistency'],
     'subagent', 'misar-dev:brand-agents', 1, 'Brand analysis in dedicated brand-agents subagent'),

    # Content / copy / docs audit
    (['content audit', 'grammar audit', 'copy audit', 'localization audit',
      'docs audit', 'documentation audit', 'copy review'],
     'subagent', 'misar-dev:content-agents', 1, 'Content analysis in dedicated content-agents subagent'),

    # Website audit
    (['audit site', 'website audit', 'site audit', 'audit this website', 'audit the site',
      'audit the url', 'audit this url'],
     'subagent', 'misar-dev:website-auditor-agents', 1, 'Site audit in dedicated website-auditor subagent'),

    # Compliance
    (['compliance audit', 'gdpr', 'hipaa', 'pci dss', 'ccpa', 'regulatory audit',
      '49 frameworks', 'compliance check', 'data privacy audit'],
     'subagent', 'misar-dev:compliance-agents', 1, 'Compliance in dedicated compliance-agents subagent'),

    # SEO content generation
    (['generate article', 'write seo content', 'seo article', 'write content for seo',
      'seo blog post', 'seo-optimized'],
     'subagent', 'misar-dev:seo-content-agents', 1, 'SEO content in dedicated seo-content-agents subagent'),

    # Architecture / system design — Plan subagent
    (['design the architecture', 'architect this', 'system design', 'plan the implementation',
      'design the system', 'how should we architect', 'design the database', 'design the api'],
     'subagent', 'Plan', 1, 'Architecture delegated to Plan subagent (specialist reasoning)'),

    # Software engineering feature build
    (['build this feature', 'implement this feature', 'create this feature',
      'build this app', 'implement this from prd', 'build from spec'],
     'subagent', 'misar-dev:software-engineer-agents', 1, 'Feature build in software-engineer-agents subagent'),

    # Full-suite audit — parallel orchestrator
    (['full-suite', 'full suite audit', 'audit everything', 'audit all', 'complete audit',
      'run all audits', 'comprehensive audit'],
     'parallel', 'misar-dev:orchestrator-agents', 4, 'Full suite → parallel orchestrator (max 4 batches)'),

    # Multi-file / multi-repo exploration — parallel Explore
    (['across multiple files', 'multiple repos', 'all files in', 'scan all',
      'across the codebase', 'explore all', 'check all repos', 'scan all repos'],
     'parallel', 'Explore', 3, 'Multi-file/repo exploration parallelized into 3× Explore subagents'),
]


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
        return VERSION_MAP.get(model, '4.7' if model == 'opus' else '4.6')

    def _wants_1m_context(self, prompt: str, transcript_path: Optional[str]) -> bool:
        """Decide whether the prompt/transcript wants 1M context (independent of model)."""
        prompt_lower = prompt.lower()
        if any(p in prompt_lower for p in PATTERNS_1M):
            self._log("1M context triggered by pattern in prompt")
            return True
        if transcript_path and Path(transcript_path).exists():
            try:
                size = Path(transcript_path).stat().st_size
                tokens = size // 4
                if tokens > 150000:
                    self._log(f"1M context triggered by transcript size: ~{tokens} tokens")
                    return True
            except Exception:
                pass
        return False

    def _wants_opus_promotion(self, prompt: str) -> bool:
        """Heavy-scope prompts (full-suite/compliance/monorepo) should escalate to opus 4.7."""
        prompt_lower = prompt.lower()
        opus_promote_patterns = [
            'full-suite', 'full audit', 'audit all', 'compliance audit',
            '49 frameworks', 'monorepo', 'cross-repo', 'multi-repo',
            'entire codebase', 'whole codebase', 'architecture',
        ]
        return any(p in prompt_lower for p in opus_promote_patterns)

    def _detect_dispatch(self, prompt: str) -> Tuple[str, str, int, str]:
        """Detect optimal dispatch strategy → (dispatch, subagent_type, parallel_count, reason).

        Checks DISPATCH_MATRIX patterns against prompt. Returns first match.
        Returns ('inline', '', 1, reason) if no specialized dispatch needed.
        """
        prompt_lower = prompt.lower()
        for patterns, dispatch, subagent_type, parallel_count, reason in DISPATCH_MATRIX:
            if any(p in prompt_lower for p in patterns):
                self._log(f"Dispatch: {dispatch} → {subagent_type} (parallel={parallel_count})")
                return dispatch, subagent_type, parallel_count, reason
        return 'inline', '', 1, 'No dispatch pattern matched — handled inline'

    def _detect_external_provider(self, prompt: str) -> Optional[str]:
        """Return 'misarcoder' / 'assisters' if prompt is best handled outside Claude."""
        prompt_lower = prompt.lower()
        for provider, patterns in EXTERNAL_PROVIDER_PATTERNS.items():
            if any(p in prompt_lower for p in patterns):
                return provider
        return None

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
        """Main 4D routing logic — model + effort + version + 1M-context + provider."""
        self._log(f"Routing prompt: {prompt[:100]}...")

        # Step 0: External-provider short-circuit (free MoE / WritingSkill)
        external = self._detect_external_provider(prompt)
        if external:
            decision = RoutingDecision(
                model='external',
                effort='low',
                version='n/a',
                agents=[],
                token_estimate=0,
                reason=f"Offloaded to {external} (free, 0 Claude credits)",
                context_1m=False,
                provider=external,
                model_id={'misarcoder': 'gemini-2.5-flash', 'assisters': 'assisters-chat-v1'}[external],
            )
            self._log(f"External provider: {external}")
            self._save_state(decision)
            return decision

        # Step 0b: Pre-decide 1M context demand (model-independent)
        wants_1m = self._wants_1m_context(prompt, transcript_path)
        wants_opus = self._wants_opus_promotion(prompt)

        # Step 1: Determine model
        model, token_estimate = self._estimate_model(prompt)

        # Heavy-scope prompts override haiku/sonnet → opus 4.7
        if wants_opus and model != 'opus':
            self._log(f"Opus promotion: {model} -> opus (heavy-scope prompt)")
            model = 'opus'
            token_estimate = max(token_estimate, 15000)

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
            # Budget override forces haiku → cancel 1M demand (haiku has no 1M)
            wants_1m = False

        # Step 4b: Resolve final 1M flag — only if model supports it AND prompt/transcript wants it
        context_1m = wants_1m and (model in MODEL_IDS_1M)

        # Step 4c: 5th dimension — detect dispatch strategy
        dispatch, subagent_type, parallel_count, dispatch_reason = self._detect_dispatch(prompt)

        # Step 5: Match agents
        matched_agents = self._match_agents(prompt)

        if matched_agents:
            matched_agents = self._add_dependencies(matched_agents)
        else:
            fallback = self.config.get('fallback', {})
            matched_agents = fallback.get('agents', ['general-purpose'])
            # Don't reset model/effort/version if we explicitly promoted to opus or
            # are already running an override. Only fall back if model is still default-sonnet.
            if not budget_override and not wants_opus:
                model = fallback.get('model', 'sonnet')
                effort = fallback.get('effort', 'medium')
                version = fallback.get('version', VERSION_MAP.get(model, '4.6'))
                # Re-evaluate 1M flag after fallback
                context_1m = wants_1m and (model in MODEL_IDS_1M)

        # Step 6: Apply agent token budget
        budget = self.config.get('token_budget', {}).get('max_agents_context', 12000)
        final_agents = self._apply_token_budget(matched_agents, budget)

        # Resolve final model_id (1M variant if applicable)
        if context_1m and model in MODEL_IDS_1M:
            model_id = MODEL_IDS_1M[model]
            ctx_label = '1M'
        else:
            model_id = MODEL_IDS.get(model, 'unknown')
            ctx_label = '200K'

        decision = RoutingDecision(
            model=model,
            effort=effort,
            version=version,
            agents=final_agents,
            token_estimate=token_estimate,
            reason=f"{model}+{effort}+{version}+{ctx_label} | {len(final_agents)} agents | dispatch={dispatch}",
            context_1m=context_1m,
            provider='claude',
            model_id=model_id,
            dispatch=dispatch,
            subagent_type=subagent_type,
            parallel_count=parallel_count,
            dispatch_reason=dispatch_reason,
        )

        self._log(f"Decision: {model}+{effort}+{version}+{ctx_label}, dispatch={dispatch}({subagent_type}), agents={len(final_agents)}, est={token_estimate}")
        self._save_state(decision)
        return decision

    def _save_state(self, decision: RoutingDecision):
        state = {
            'model': decision.model,
            'effort': decision.effort,
            'version': decision.version,
            'context_1m': decision.context_1m,
            'provider': decision.provider,
            'model_id': decision.model_id or MODEL_IDS.get(decision.model, 'unknown'),
            'agents': decision.agents,
            'token_estimate': decision.token_estimate,
            'reason': decision.reason,
            'dispatch': decision.dispatch,
            'subagent_type': decision.subagent_type,
            'parallel_count': decision.parallel_count,
            'dispatch_reason': decision.dispatch_reason,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
        # Also broadcast to shared session bridge so MisarCoder/Assisters see same state
        bridge_dir = Path('/tmp/.misar-session')
        bridge_dir.mkdir(exist_ok=True)
        with open(bridge_dir / 'router_state.json', 'w') as f:
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

    effort_short = {'low': 'low', 'medium': 'med', 'high': 'high', 'max': 'max'}
    ctx = '1m' if decision.context_1m else '200k'

    if args.model_only:
        print(decision.model_id or decision.model)
    elif args.badge:
        if decision.provider != 'claude':
            print(f"[→{decision.provider}|free]")
        elif decision.dispatch == 'subagent':
            print(f"[→subagent:{decision.subagent_type}|{decision.model}|{effort_short.get(decision.effort, decision.effort)}|{ctx}]")
        elif decision.dispatch == 'parallel':
            print(f"[→parallel:{decision.parallel_count}×{decision.subagent_type}|{decision.model}|{effort_short.get(decision.effort, decision.effort)}|{ctx}]")
        else:
            print(f"[{decision.model}|{effort_short.get(decision.effort, decision.effort)}|{decision.version}|{ctx}]")
    elif args.json:
        output = {
            'model': decision.model,
            'effort': decision.effort,
            'version': decision.version,
            'context_1m': decision.context_1m,
            'provider': decision.provider,
            'model_id': decision.model_id or MODEL_IDS.get(decision.model, 'unknown'),
            'agents': decision.agents,
            'token_estimate': decision.token_estimate,
            'reason': decision.reason,
            'dispatch': decision.dispatch,
            'subagent_type': decision.subagent_type,
            'parallel_count': decision.parallel_count,
            'dispatch_reason': decision.dispatch_reason,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Provider: {decision.provider}")
        print(f"Model:    {decision.model} ({decision.model_id or MODEL_IDS.get(decision.model, '?')})")
        print(f"Effort:   {decision.effort}")
        print(f"Version:  {decision.version}")
        print(f"Context:  {'1M' if decision.context_1m else '200K'}")
        print(f"Badge:    [{decision.model}|{effort_short.get(decision.effort, decision.effort)}|{decision.version}|{ctx}]")
        print(f"Dispatch: {decision.dispatch}" + (f" → {decision.subagent_type}" if decision.subagent_type else ""))
        if decision.parallel_count > 1:
            print(f"Parallel: {decision.parallel_count}× {decision.subagent_type}")
        print(f"Dispatch reason: {decision.dispatch_reason}")
        print(f"Agents:   {', '.join(decision.agents) if decision.agents else 'none'}")
        print(f"Tokens:   ~{decision.token_estimate}")
        print(f"Reason:   {decision.reason}")


if __name__ == '__main__':
    main()
