import subprocess
import sys
import shutil
import difflib
from termcolor import cprint

"""
Python Dependency Audit & Fix Script

This script helps ensure all dependencies in `requirements.txt` are secure before pushing to a repository. It:
1. Uninstalls all installed packages.
2. Reinstalls dependencies from `requirements.txt`.
3. Runs `pip-audit` to check for vulnerabilities.
4. If vulnerabilities are found, it attempts to auto-fix them in a loop.
5. Shows color-coded changes to `requirements.txt` after fixing dependencies.
6. Asks for user confirmation before applying fixes.

Usage:
    Run the script before pushing code:
        python audit_fix.py

Dependencies:
    - `pip-audit`: Used for vulnerability scanning (auto-installed if missing).
    - `termcolor`: For color-coded output (install via `pip install termcolor`).
"""

def run_command(command):
    """
    Run a shell command and return its output.
    
    Args:
        command (str): The shell command to execute.

    Returns:
        str: Output of the command.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def uninstall_all_packages():
    """
    Uninstall all installed packages to ensure a clean environment.
    """
    print("\033[1;33mUninstalling all packages...\033[0m")
    packages = run_command("pip freeze")
    if packages:
        subprocess.run("pip freeze | xargs pip uninstall -y", shell=True)

def install_requirements():
    """
    Install dependencies from requirements.txt.
    """
    print("\033[1;33mInstalling dependencies from requirements.txt...\033[0m")
    subprocess.run("pip install -r requirements.txt", shell=True)

def ensure_pip_audit():
    """
    Ensure `pip-audit` is installed. If not, install it. 
    """
    if shutil.which("pip-audit") is None:
        print("\033[1;33mpip-audit not found. Installing...\033[0m")
        subprocess.run("pip install pip-audit", shell=True)

def run_pip_audit():
    """
    Run `pip-audit` to check for vulnerabilities in installed dependencies.

    Returns:
        str: The output of `pip-audit`.
    """
    print("\033[1;34mChecking for vulnerabilities...\033[0m")
    return run_command("pip-audit")

def fix_vulnerabilities():
    """
    Run `pip-audit --fix` in a loop until no vulnerabilities remain.

    - If vulnerabilities are detected, attempts auto-fix.
    - If no vulnerabilities are found, exits cleanly.
    """
    audit_output = run_pip_audit()
    print(f"\033[0;31m{audit_output}\033[0m")

    while "Name    Version   ID" in audit_output:  # Detect audit table header
        print("\033[1;33mVulnerabilities detected. Running pip-audit --fix...\033[0m")
        fix_output = run_command("pip-audit --fix")
        print(f"\033[0;32mFixes Applied:\n{fix_output}\033[0m")
        audit_output = run_pip_audit()
        print(f"\033[0;31m{audit_output}\033[0m")

    print("\033[0;32mNo vulnerabilities detected. Proceeding with push.\033[0m")

def update_requirements():
    """
    Update `requirements.txt` with the latest installed dependencies.
    Displays color-coded changes to the user before applying.

    - Green (+): Added dependencies or updated versions.
    - Red (-): Removed or downgraded dependencies.

    The user is prompted before confirming the changes.
    """
    print("\033[1;34mUpdating requirements.txt with fixed dependencies...\033[0m")

    # Save new package list
    run_command("pip freeze > new_requirements.txt")

    # Read original and new requirements files
    with open("requirements.txt", "r") as f:
        original_lines = f.readlines()

    with open("new_requirements.txt", "r") as f:
        new_lines = f.readlines()

    # Compute the diff
    diff = difflib.unified_diff(original_lines, new_lines, fromfile="requirements.txt", tofile="new_requirements.txt", lineterm="")

    print("\n\033[1;34mChanges to requirements.txt:\033[0m")
    has_changes = False
    for line in diff:
        has_changes = True
        if line.startswith("+") and not line.startswith("+++"):  # New additions
            cprint(line, "green", end="")
        elif line.startswith("-") and not line.startswith("---"):  # Deletions
            cprint(line, "red", end="")
        else:
            print(line, end="")

    if not has_changes:
        print("\033[0;32mNo changes detected.\033[0m")
        return

    # Ask user for confirmation before applying changes
    confirm = input("\n\033[1;33mDo you want to apply these changes? (y/N): \033[0m").strip().lower()
    if confirm == "y":
        print("\033[1;32mApplying changes...\033[0m")
        run_command("mv new_requirements.txt requirements.txt")
    else:
        print("\033[1;31mChanges discarded.\033[0m")
        run_command("rm new_requirements.txt")

def main():
    """
    Main execution function that:
    1. Uninstalls all packages.
    2. Reinstalls dependencies.
    3. Runs security checks.
    4. Fixes vulnerabilities if found.
    5. Updates `requirements.txt` safely.
    """
    uninstall_all_packages()
    install_requirements()
    ensure_pip_audit()
    fix_vulnerabilities()
    update_requirements()

if __name__ == "__main__":
    main()