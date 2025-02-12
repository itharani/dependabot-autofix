import subprocess
import shutil
from termcolor import cprint


# Function to run a shell command and capture output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Function to uninstall all packages
def uninstall_all_packages():
    print("\033[1;33mUninstalling all packages...\033[0m")
    packages = run_command("pip freeze")
    if packages:
        subprocess.run("pip freeze | xargs pip uninstall -y", shell=True)

# Function to install dependencies from requirements.txt
def install_requirements():
    print("\033[1;33mInstalling dependencies from requirements.txt...\033[0m")
    subprocess.run("pip install -r requirements.txt", shell=True)

# Ensure pip-audit is installed
def ensure_pip_audit():
    if shutil.which("pip-audit") is None:
        print("\033[1;33mpip-audit not found. Installing...\033[0m")
        subprocess.run("pip install pip-audit", shell=True)

# Run pip-audit to check for vulnerabilities and auto-fix them
def run_pip_audit():
    print("\033[1;34mChecking for vulnerabilities...\033[0m")
    
    # Run pip-audit and capture the output
    audit_output = run_command("pip-audit -r requirements.txt")
    
    # Print the vulnerabilities found
    if audit_output:
        print("\033[1;31mVulnerabilities found:\033[0m")
        print(f"\033[1;31m{audit_output}\033[0m") 
        print("\033[1;34mApplying fixes...\033[0m")
        return run_command("pip-audit -r requirements.txt --fix")
        
    else:
        print("\033[0;32mNo vulnerabilities found.\033[0m")
        
    
# Function to get the current state of installed packages
def get_installed_packages():
    return run_command("pip freeze").splitlines()

# Function to update requirements.txt with only the fixed packages
def update_requirements(original_packages):
    """
    Update `requirements.txt` with only the fixed dependencies.
    Compares the original package list with the current list of installed packages.
    """
    print("\033[1;34mUpdating requirements.txt with fixed dependencies...\033[0m")

    old_lines = open("requirements.txt").read().split('\n')
    new_lines = open("new_requirements.txt").read().split('\n')

    old_lines_set = set(old_lines)
    new_lines_set = set(new_lines)

    old_added = old_lines_set - new_lines_set 
    old_removed = new_lines_set - old_lines_set

    for line in old_lines:
        if line in old_added:
            print('-', line.strip())
        elif line in old_removed:
            print('+', line.strip())
    
    for line in new_lines:
        if line in old_added:
            print('-', line.strip())
        elif line in old_removed:
            print('+', line.strip())

# Main execution function
def main():
    uninstall_all_packages()
    install_requirements()
    ensure_pip_audit()

    # Get original installed packages
    original_packages = get_installed_packages()

    # Run pip-audit and fix vulnerabilities
    run_pip_audit()

    # Update the requirements.txt with only the fixed packages
    #update_requirements(original_packages)

if __name__ == "__main__":
    main()
