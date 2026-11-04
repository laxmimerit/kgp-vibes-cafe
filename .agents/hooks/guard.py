#!/usr/bin/env python3
"""
Guard hook script for Antigravity PreToolUse on run_command.
Protects baseline/, source/, and menu.csv from accidental deletion.
"""

import sys
import json
import re
import os

PROTECTED_REASON = "The menu and the starting data are protected."

# Target pattern: matches baseline/ or source/ directories/paths, or any menu.csv
TARGET_PATTERN = re.compile(
    r'(?:^|[\s"\'/\\])(?:baseline|source)(?:[\s"\'/\\*]|$)|menu\.csv\b',
    re.IGNORECASE
)

# Common deletion verbs/tools across shells
DELETE_VERBS = {
    "rm", "del", "erase", "rmdir", "rd", "remove-item", "ri", "unlink", "shred"
}

def extract_command(data):
    if not isinstance(data, dict):
        return ""
    # Check standard Antigravity PreToolUse payload
    if "toolCall" in data and isinstance(data["toolCall"], dict):
        tc = data["toolCall"]
        args = tc.get("args", {})
        if isinstance(args, dict):
            for k in ("CommandLine", "command", "command_line", "commandLine", "cmd"):
                if k in args and isinstance(args[k], str):
                    return args[k]
    # Check if toolCall is at root
    args = data.get("args")
    if isinstance(args, dict):
        for k in ("CommandLine", "command", "command_line", "commandLine", "cmd"):
            if k in args and isinstance(args[k], str):
                return args[k]
    for k in ("CommandLine", "command", "command_line", "commandLine", "cmd"):
        if k in data and isinstance(data[k], str):
            return data[k]
    return ""

def subcmd_deletes_protected(subcmd: str) -> bool:
    subcmd = subcmd.strip()
    if not subcmd:
        return False

    has_target = bool(TARGET_PATTERN.search(subcmd))

    # Check for git rm or git clean
    if re.search(r'\bgit\s+(?:rm|clean)\b', subcmd, re.IGNORECASE):
        if has_target:
            return True

    # Check for inline python / node deletion APIs
    if re.search(r'\b(?:os\.remove|os\.unlink|shutil\.rmtree|fs\.unlink|fs\.rm|fs\.rmdir)\b', subcmd, re.IGNORECASE):
        if has_target:
            return True

    # Tokenize command to check the leading verb
    tokens = re.split(r'\s+', subcmd)
    idx = 0
    while idx < len(tokens):
        token = tokens[idx].strip('\'"()')
        lower = os.path.basename(token).lower()
        if lower.endswith('.exe'):
            lower = lower[:-4]

        # Skip shell / interpreter wrappers
        if lower in ("cmd", "powershell", "pwsh", "sudo", "env", "xargs", "sh", "bash"):
            idx += 1
            while idx < len(tokens) and tokens[idx].startswith(('-', '/')):
                idx += 1
            continue

        if lower in DELETE_VERBS:
            if has_target:
                return True
        break

    return False

def would_delete_protected(cmd: str) -> bool:
    if not cmd or not isinstance(cmd, str):
        return False

    # Quick check: does the command reference protected targets at all?
    if not TARGET_PATTERN.search(cmd):
        return False

    # Check split subcommands (split by ;, &&, ||, |, \n)
    subcmds = re.split(r'[;&|\n]+', cmd)
    for sub in subcmds:
        if subcmd_deletes_protected(sub):
            return True

    # Check pipeline/compound combinations where delete verb appears anywhere
    delete_verb_pattern = re.compile(
        r'\b(?:rm|del|erase|rmdir|rd|remove-item|unlink|shred)\b|\bgit\s+(?:rm|clean)\b',
        re.IGNORECASE
    )
    if delete_verb_pattern.search(cmd) and TARGET_PATTERN.search(cmd):
        first_token = cmd.strip().split()[0].lower() if cmd.strip() else ""
        first_base = os.path.basename(first_token).strip('\'"')
        if first_base not in ("cat", "grep", "echo", "printf", "type", "head", "tail", "more", "less"):
            return True

    return False

def evaluate(payload: dict) -> dict:
    cmd = extract_command(payload)
    if cmd and would_delete_protected(cmd):
        return {
            "decision": "deny",
            "reason": PROTECTED_REASON
        }
    return {
        "decision": "allow"
    }

def main():
    raw = ""
    if len(sys.argv) > 1 and sys.stdin.isatty():
        raw = sys.argv[1]
    else:
        try:
            raw = sys.stdin.read()
        except Exception:
            raw = ""
        if not raw.strip() and len(sys.argv) > 1:
            raw = sys.argv[1]

    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    result = evaluate(data)
    print(json.dumps(result))

if __name__ == "__main__":
    main()
