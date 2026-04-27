#!/usr/bin/env python3
"""
PreToolUse hook: blocks Bash commands that risk exposing credentials.
Receives tool call data as JSON on stdin.
Exits 1 to block, 0 to allow.
"""
import sys
import json
import re

try:
    data = json.loads(sys.stdin.read())
    tool_input = data.get("tool_input", data)
    cmd = tool_input.get("command", "")

    dangerous = [
        r"\bcat\s+\.env\b",
        r"\bcat\s+\S*\.env\b",
        r"\becho\s+\$\{?(?:API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY|ACCESS_TOKEN)[^}]*\}?",
        r"\bprintenv\s+(?:API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY)",
        r"\benv\b.*(?:API_KEY|SECRET|TOKEN|PASSWORD)",
        r"curl\s+.*(?:--header|--data).*(?:API_KEY|SECRET|TOKEN|Bearer)",
    ]

    for pattern in dangerous:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(
                f"BLOCKED: Credential exposure risk detected.\n"
                f"Pattern matched in command: {cmd[:120]}\n"
                f"If intentional, run manually outside Claude Code.",
                file=sys.stderr,
            )
            sys.exit(1)

except Exception:
    pass  # Never block on parse errors — fail open

sys.exit(0)
