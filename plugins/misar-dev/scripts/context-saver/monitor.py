#!/usr/bin/env python3
"""
Token Monitor — Context Saver v7.0.0
Tracks token usage with 3D routing recommendations (model×effort×version).
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional


# Version mapping
VERSION_MAP = {'haiku': '4.5', 'sonnet': '4.6', 'opus': '4.6'}


class TokenMonitor:
    """Monitor token usage and provide 3D optimization recommendations"""

    def __init__(self):
        self.router_dir = Path.home() / '.claude' / 'router'
        self.session_log = self.router_dir / 'session.log'
        self.monitor_state = self.router_dir / 'monitor-state.json'

        self.MAX_WINDOW = 200000
        self.WARN_THRESHOLD = 0.70
        self.CRITICAL_THRESHOLD = 0.90

        self.router_dir.mkdir(parents=True, exist_ok=True)

    def estimate_tokens(self, transcript_path: str) -> int:
        """Estimate tokens from transcript file size (1 token ~ 4 bytes)"""
        try:
            return os.path.getsize(transcript_path) // 4
        except (OSError, PermissionError, FileNotFoundError) as e:
            if self.router_dir.exists():
                log = self.router_dir / 'monitor.log'
                with open(log, 'a') as f:
                    f.write(f"[{datetime.now().isoformat()}] estimate_tokens error: {e}\n")
            return 0

    def get_usage_percentage(self, tokens: int) -> float:
        return (tokens / self.MAX_WINDOW) * 100

    def track_session(self, tokens: int, model: str = 'auto', effort: str = 'auto') -> Dict:
        prev_tokens = 0
        if self.session_log.exists():
            with open(self.session_log) as f:
                lines = f.readlines()
                if lines:
                    try:
                        parts = lines[-1].strip().split('|')
                        if len(parts) >= 2:
                            prev_tokens = int(parts[1])
                    except (IndexError, ValueError):
                        pass

        delta = tokens - prev_tokens
        version = VERSION_MAP.get(model, 'auto')
        with open(self.session_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()}|{tokens}|{delta}|{model}|{effort}|{version}\n")

        # Count model/effort distribution
        distribution = {'haiku': 0, 'sonnet': 0, 'opus': 0, 'auto': 0}
        effort_dist = {'low': 0, 'medium': 0, 'high': 0, 'max': 0, 'auto': 0}
        with open(self.session_log) as f:
            all_lines = f.readlines()
            prompt_count = len(all_lines)
            for line in all_lines:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    m = parts[3]
                    distribution[m] = distribution.get(m, 0) + 1
                if len(parts) >= 5:
                    e = parts[4]
                    effort_dist[e] = effort_dist.get(e, 0) + 1

        return {
            'tokens': tokens,
            'prev_tokens': prev_tokens,
            'delta': delta,
            'prompt_count': prompt_count,
            'model_distribution': distribution,
            'effort_distribution': effort_dist,
        }

    def get_recommendation(self, usage_pct: float, tokens: int, delta: int) -> Tuple[str, str, Optional[str]]:
        """Returns (model, effort, message)"""
        if usage_pct >= 90:
            return 'haiku', 'low', (
                f"CRITICAL: {usage_pct:.0f}% ({tokens:,}/{self.MAX_WINDOW:,}) "
                f"- Forced haiku+low. Consider /compact or new session."
            )
        elif usage_pct >= 70:
            return 'haiku', 'low', (
                f"HIGH: {usage_pct:.0f}% ({tokens:,}/{self.MAX_WINDOW:,}) "
                f"- Auto-switched to haiku+low."
            )
        elif usage_pct >= 40:
            return 'sonnet', 'medium', (
                f"OK: {usage_pct:.0f}% ({tokens:,}/{self.MAX_WINDOW:,}) "
                f"- Capped at sonnet+medium. No opus."
            )
        else:
            return 'auto', 'auto', None

    def analyze(self, transcript_path: str = None, current_model: str = 'auto', current_effort: str = 'auto') -> Dict:
        if not transcript_path or not os.path.exists(transcript_path):
            return {
                'status': 'no_data',
                'recommended_model': 'sonnet',
                'recommended_effort': 'medium',
                'recommended_version': '4.6',
                'message': 'No transcript data available'
            }

        tokens = self.estimate_tokens(transcript_path)
        usage_pct = self.get_usage_percentage(tokens)
        session = self.track_session(tokens, current_model, current_effort)
        rec_model, rec_effort, message = self.get_recommendation(
            usage_pct, tokens, session['delta']
        )
        rec_version = VERSION_MAP.get(rec_model, '4.6')

        state = {
            'tokens': tokens,
            'usage_pct': usage_pct,
            'recommended_model': rec_model,
            'recommended_effort': rec_effort,
            'recommended_version': rec_version,
            'prompt_count': session['prompt_count'],
            'last_delta': session['delta'],
            'model_distribution': session['model_distribution'],
            'effort_distribution': session['effort_distribution'],
            'timestamp': datetime.now().isoformat()
        }
        with open(self.monitor_state, 'w') as f:
            json.dump(state, f, indent=2)

        return {
            'status': 'ok',
            'tokens': tokens,
            'usage_pct': usage_pct,
            'recommended_model': rec_model,
            'recommended_effort': rec_effort,
            'recommended_version': rec_version,
            'recommended_badge': f"[{rec_model}|{rec_effort}|{rec_version}]",
            'message': message,
            'prompt_count': session['prompt_count'],
            'delta': session['delta'],
            'model_distribution': session['model_distribution'],
            'effort_distribution': session['effort_distribution'],
        }

    def reset_session(self):
        if self.session_log.exists():
            self.session_log.unlink()
        if self.monitor_state.exists():
            self.monitor_state.unlink()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Context Saver — 3D Token Monitor')
    parser.add_argument('--transcript', help='Path to transcript file')
    parser.add_argument('--reset', action='store_true', help='Reset session tracking')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--model', default='auto', help='Current model in use')
    parser.add_argument('--effort', default='auto', help='Current effort level')

    args = parser.parse_args()
    monitor = TokenMonitor()

    if args.reset:
        monitor.reset_session()
        print("Session tracking reset (3D state cleared)")
        return

    result = monitor.analyze(args.transcript, args.model, args.effort)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get('message'):
            print(result['message'])
        if result['status'] == 'ok':
            print(f"Recommended: {result['recommended_badge']}")
            md = result.get('model_distribution', {})
            ed = result.get('effort_distribution', {})
            print(f"Model dist:  haiku={md.get('haiku',0)} sonnet={md.get('sonnet',0)} opus={md.get('opus',0)}")
            print(f"Effort dist: low={ed.get('low',0)} med={ed.get('medium',0)} high={ed.get('high',0)} max={ed.get('max',0)}")


if __name__ == '__main__':
    main()
