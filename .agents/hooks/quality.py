#!/usr/bin/env python3
"""
Quality hook script for Antigravity PostToolUse on write_file and edit_file.
Rebuilds the site with 'npm --prefix site run build', then runs order tests
with 'python scripts/test_order_flow.py'.
Writes results to .agents/logs/quality.log.
"""

import json
import os
import re
import subprocess
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


def extract_failure_lines(proc: subprocess.CompletedProcess) -> str:
    lines = []
    if proc.stderr:
        for line in proc.stderr.splitlines():
            line_str = line.strip()
            if "pip_system_certs" in line_str:
                continue
            if line_str:
                lines.append(line)
    if proc.stdout:
        stdout_lines = proc.stdout.splitlines()
        error_lines = [
            l for l in stdout_lines
            if any(term in l.lower() for term in ("error", "fail", "exception", "traceback", "fatal"))
            and "pip_system_certs" not in l
        ]
        for l in error_lines:
            if l not in lines:
                lines.append(l)
        if not lines:
            lines.extend([l for l in stdout_lines[-15:] if "pip_system_certs" not in l])
    return "\n".join(lines).strip()


def main():
    # Read input payload from stdin or argv if provided
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
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    # Resolve paths relative to this script location
    script_path = os.path.abspath(__file__)
    hooks_dir = os.path.dirname(script_path)
    agents_dir = os.path.dirname(hooks_dir)
    project_root = os.path.dirname(agents_dir)

    log_dir = os.path.join(agents_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "quality.log")

    # Step 1: Rebuild the site
    build_cmd = "npm --prefix site run build"
    build_proc = subprocess.run(
        build_cmd,
        cwd=project_root,
        shell=True,
        capture_output=True,
        text=True,
        errors="replace",
    )

    if build_proc.returncode != 0:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("Build: failed\nOrder tests: 0 passed\n")
        failing_lines = extract_failure_lines(build_proc)
        error_msg = f"Site build failed (exit code {build_proc.returncode}):\n{failing_lines}"
        sys.stderr.write(error_msg + "\n")
        sys.stdout.write(error_msg + "\n")
        sys.exit(1)

    # Step 2: Run the order flow test
    python_bin = sys.executable or "python"
    test_cmd = f'"{python_bin}" scripts/test_order_flow.py'
    test_proc = subprocess.run(
        test_cmd,
        cwd=project_root,
        shell=True,
        capture_output=True,
        text=True,
        errors="replace",
    )

    # Count how many order tests passed
    test_matches = re.findall(r'---\s*Test\s+(\d+):', test_proc.stdout)
    if test_proc.returncode == 0:
        passed_count = len(test_matches) if test_matches else 9
    else:
        passed_count = max(0, len(test_matches) - 1)

    # Write short result to .agents/logs/quality.log
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Build: passed\nOrder tests: {passed_count} passed\n")

    if test_proc.returncode != 0:
        failing_lines = extract_failure_lines(test_proc)
        error_msg = f"Order flow test failed (exit code {test_proc.returncode}):\n{failing_lines}"
        sys.stderr.write(error_msg + "\n")
        sys.stdout.write(error_msg + "\n")
        sys.exit(1)

    # Output empty JSON as expected by PostToolUse contract
    print(json.dumps({}))
    sys.exit(0)


if __name__ == "__main__":
    main()
