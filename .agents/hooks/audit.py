#!/usr/bin/env python3
"""
Audit hook script for Antigravity PostToolUse on all tools.
Appends one line per tool call to .agents/logs/audit.log:
the step number, the tool name, and a short summary of the action.
No dates or times in the log.
Fast and never fails the tool call.
"""

import json
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def extract_step(payload: dict) -> str:
    for k in ("stepIdx", "step_index", "step_idx", "stepIndex", "step", "stepNumber"):
        if k in payload and payload[k] is not None:
            return str(payload[k]).strip()
    tc = payload.get("toolCall")
    if isinstance(tc, dict):
        for k in ("stepIdx", "step_index", "step_idx", "stepIndex", "step", "stepNumber"):
            if k in tc and tc[k] is not None:
                return str(tc[k]).strip()
    return ""


def extract_tool_name(payload: dict) -> str:
    tc = payload.get("toolCall")
    if isinstance(tc, dict):
        for k in ("name", "tool_name", "toolName", "tool"):
            if k in tc and isinstance(tc[k], str) and tc[k].strip():
                return tc[k].strip()
    for k in ("tool_name", "toolName", "tool", "name"):
        if k in payload and isinstance(payload[k], str) and payload[k].strip():
            return payload[k].strip()
    return ""


def extract_args(payload: dict) -> dict:
    tc = payload.get("toolCall")
    if isinstance(tc, dict):
        for k in ("args", "parameters", "arguments", "input"):
            if k in tc and isinstance(tc[k], dict):
                return tc[k]
    for k in ("args", "parameters", "arguments", "input"):
        if k in payload and isinstance(payload[k], dict):
            return payload[k]
    return {}


def extract_summary(tool_name: str, args: dict, payload: dict) -> str:
    if isinstance(args, dict):
        # 1. Commands
        for k in ("CommandLine", "command", "command_line", "cmd"):
            if k in args and isinstance(args[k], str) and args[k].strip():
                return " ".join(args[k].split())

        # 2. File paths
        for k in ("file_path", "filePath", "Path", "path", "filename", "file", "target", "Target", "uri", "url"):
            if k in args and isinstance(args[k], str) and args[k].strip():
                return " ".join(args[k].split())

        # 3. Tool summaries or descriptions
        for k in ("toolSummary", "summary", "description"):
            if k in args and isinstance(args[k], str) and args[k].strip():
                return " ".join(args[k].split())

        # 4. Search queries, patterns, questions
        for k in ("query", "pattern", "prompt", "question", "message"):
            if k in args and isinstance(args[k], str) and args[k].strip():
                return " ".join(args[k].split())

        # 5. First string value in args
        for k, v in args.items():
            if isinstance(v, str) and v.strip():
                return " ".join(v.split())

        # 6. First scalar value in args
        for k, v in args.items():
            if isinstance(v, (int, float, bool)):
                return str(v)
    elif isinstance(args, str) and args.strip():
        return " ".join(args.split())

    # Fallback to root payload keys if not found in args
    for k in ("CommandLine", "command", "command_line", "cmd", "file_path", "filePath", "Path", "path", "filename", "file", "query", "url"):
        if k in payload and isinstance(payload[k], str) and payload[k].strip():
            return " ".join(payload[k].split())

    return ""


def main():
    try:
        raw = ""
        if len(sys.argv) > 1 and sys.stdin and sys.stdin.isatty():
            raw = sys.argv[1]
        else:
            try:
                if sys.stdin:
                    raw = sys.stdin.read()
            except Exception:
                raw = ""
            if not raw.strip() and len(sys.argv) > 1:
                raw = sys.argv[1]

        if not raw.strip():
            print(json.dumps({}))
            sys.exit(0)

        try:
            payload = json.loads(raw)
        except Exception:
            # If payload is invalid JSON, write nothing and exit cleanly
            print(json.dumps({}))
            sys.exit(0)

        if not isinstance(payload, dict):
            print(json.dumps({}))
            sys.exit(0)

        step = extract_step(payload)
        tool_name = extract_tool_name(payload)
        args = extract_args(payload)
        summary = extract_summary(tool_name, args, payload)

        if len(summary) > 300:
            summary = summary[:297] + "..."

        parts = []
        if step:
            parts.append(step)
        if tool_name:
            parts.append(tool_name)
        if summary:
            parts.append(summary)

        if parts:
            try:
                script_path = os.path.abspath(__file__)
                hooks_dir = os.path.dirname(script_path)
                agents_dir = os.path.dirname(hooks_dir)
                log_dir = os.path.join(agents_dir, "logs")
            except Exception:
                log_dir = "logs" if os.path.isdir("logs") else os.path.join(".agents", "logs")

            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "audit.log")

            line = " ".join(parts) + "\n"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line)

    except Exception:
        # Never fail the tool call; write nothing if anything goes wrong
        pass

    try:
        print(json.dumps({}))
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
