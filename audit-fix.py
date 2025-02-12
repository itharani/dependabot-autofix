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

# Main execution function
def main():
    uninstall_all_packages()
    install_requirements()
    ensure_pip_audit()
    # Run pip-audit and fix vulnerabilities
    run_pip_audit()

if __name__ == "__main__":
    main()
