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
SEND_BLOCKED_REASON = "Sending files or emails out of this computer is prohibited."

# Target pattern: matches baseline/ or source/ directories/paths, or any menu.csv
TARGET_PATTERN = re.compile(
    r'(?:^|[\s"\'/\\])(?:baseline|source)(?:[\s"\'/\\*]|$)|menu\.csv\b',
    re.IGNORECASE
)

# Common deletion verbs/tools across shells
DELETE_VERBS = {
    "rm", "del", "erase", "rmdir", "rd", "remove-item", "ri", "unlink", "shred"
}

# Patterns for commands or libraries that send emails
EMAIL_PATTERNS = [
    # Dedicated email CLI tools
    re.compile(r'\b(?:sendmail|mailx|mutt|msmtp|swaks|ssmtp|blat)\b', re.IGNORECASE),
    # PowerShell email cmdlet
    re.compile(r'\bsend-mailmessage\b', re.IGNORECASE),
    # Standalone mail command (avoiding substring matches like gmail, email)
    re.compile(r'(?:^|[\s;&|])mail(?:\.exe)?\s+', re.IGNORECASE),
    # Python smtplib, .NET SmtpClient, nodemailer
    re.compile(r'\b(?:smtplib|SmtpClient|System\.Net\.Mail|nodemailer)\b', re.IGNORECASE),
]

# Patterns for commands that send/upload files or data out of this computer
EXFIL_PATTERNS = [
    # Remote file copy / sync tools
    re.compile(r'\b(?:scp|sftp|rsync|ftp|tftp)\b', re.IGNORECASE),
    # Cloud storage upload CLIs
    re.compile(r'\b(?:aws\s+s3\s+(?:cp|sync|mv)|gsutil\s+(?:cp|rsync)|az\s+storage\s+blob\s+upload|rclone\s+(?:copy|sync|move))\b', re.IGNORECASE),
    # Curl sending files, form data, or POST/PUT payloads
    re.compile(r'\bcurl(?:\.exe)?\b.*?(?:-[FfTt]|--form\b|--form-string\b|--upload-file\b)', re.IGNORECASE),
    re.compile(r'\bcurl(?:\.exe)?\b.*?(?:-[dD]|--data\S*)\s+["\']?@', re.IGNORECASE),
    re.compile(r'\bcurl(?:\.exe)?\b.*?(?:-[dD]|--data\S*)\s+', re.IGNORECASE),
    re.compile(r'\bcurl(?:\.exe)?\b.*?-(?:X|--request)\s+(?:POST|PUT|PATCH)\b', re.IGNORECASE),
    re.compile(r'\bcurl(?:\.exe)?\b.*?(?:\$\(|\`|\bcat\b|\btype\b|\bGet-Content\b)', re.IGNORECASE),
    re.compile(r'\|\s*(?:[\w/\\.-]*[/\\])?curl(?:\.exe)?\b', re.IGNORECASE),
    re.compile(r'\bcurl(?:\.exe)?\b.*<', re.IGNORECASE),
    # Wget posting data/files
    re.compile(r'\bwget(?:\.exe)?\b.*?(?:--post-file|--post-data)\b', re.IGNORECASE),
    # PowerShell web transfer cmdlets / methods
    re.compile(r'\b(?:invoke-restmethod|invoke-webrequest|irm|iwr)\b.*?(?:-infile\b|-method\s+(?:post|put|patch)|-body\b)', re.IGNORECASE),
    re.compile(r'\b\.(?:UploadFile|UploadData|UploadValues|UploadFileAsync)\b', re.IGNORECASE),
    re.compile(r'\bstart-bitstransfer\b.*?-transfertype\s+upload\b', re.IGNORECASE),
    # Netcat / socat piping or redirecting outbound
    re.compile(r'\b(?:nc|netcat|ncat|socat)\b.*<', re.IGNORECASE),
    re.compile(r'\|\s*(?:[\w/\\.-]*[/\\])?(?:nc|netcat|ncat|socat)\b', re.IGNORECASE),
    # Python / scripts uploading files or making outbound POST requests with data
    re.compile(r'\b(?:requests|httpx)\.(?:post|put|patch)\b.*?(?:files|data|open\b)', re.IGNORECASE),
    re.compile(r'\burllib\.request\.urlopen\b.*?(?:data|open\b)', re.IGNORECASE),
]

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

def is_safe_local_command(cmd: str) -> bool:
    cmd_stripped = cmd.strip()
    if not cmd_stripped:
        return True
    first_token = cmd_stripped.split()[0].lower()
    first_base = os.path.basename(first_token).strip('\'"')
    if first_base.endswith('.exe'):
        first_base = first_base[:-4]

    # Safe inspection and local repository commands when not piped to network/mail tools
    if first_base in ("git", "echo", "printf", "type", "head", "tail", "more", "less", "grep", "findstr"):
        if not re.search(r'\|\s*(?:[\w/\\.-]*[/\\])?(?:curl|wget|nc|netcat|ncat|socat|mail|sendmail|mutt|msmtp|swaks)\b', cmd_stripped, re.IGNORECASE):
            return True
    return False

def would_send_file_or_email(cmd: str) -> bool:
    if not cmd or not isinstance(cmd, str):
        return False

    if is_safe_local_command(cmd):
        return False

    for pattern in EMAIL_PATTERNS:
        if pattern.search(cmd):
            return True

    for pattern in EXFIL_PATTERNS:
        if pattern.search(cmd):
            return True

    # Also check split subcommands
    subcmds = re.split(r'[;&|\n]+', cmd)
    for sub in subcmds:
        sub_stripped = sub.strip()
        if not sub_stripped or is_safe_local_command(sub_stripped):
            continue
        for pattern in EMAIL_PATTERNS:
            if pattern.search(sub_stripped):
                return True
        for pattern in EXFIL_PATTERNS:
            if pattern.search(sub_stripped):
                return True

    return False

def evaluate(payload: dict) -> dict:
    cmd = extract_command(payload)
    if cmd:
        if would_delete_protected(cmd):
            return {
                "decision": "deny",
                "reason": PROTECTED_REASON
            }
        if would_send_file_or_email(cmd):
            return {
                "decision": "deny",
                "reason": SEND_BLOCKED_REASON
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
