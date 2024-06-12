import click
import subprocess
import importlib.util
import sys
from modules.dockerfile import create_dockerfile
from modules.bash import create_bash_script
from modules.k8s import create_k8s_config
from modules.ci_cd import create_ci_cd_pipeline
from modules.azure import azure_menu
from modules.aws import aws_menu
from modules.gcp import gcp_menu
from modules.developer import developer_menu
from modules.settings import settings_menu
from modules.firebase import firebase_menu  

def check_and_install_aider():
    aider_installed = importlib.util.find_spec("aider") is not None

    if not aider_installed:
        click.echo("📦 'aider' is not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', './aider_chat'])
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Failed to install 'aider': {e}")
            sys.exit(1)
        else:
            click.echo("✅ 'aider' installed successfully.")
    else:
        click.echo("✅ 'aider' is already installed.")

def coder_menu(main_menu):
    click.echo("\n📋 Agentic DevOps Menu")
    click.echo("1.    Create Dockerfile")
    click.echo("2.    Create Bash Script")
    click.echo("3.    Create Kubernetes Configuration")
    click.echo("4.    Create CI/CD Pipeline")
    click.echo("5.    Azure Configuration")
    click.echo("6.    AWS Configuration")
    click.echo("7.    GCP Configuration")
    click.echo("8.    Firebase Configuration")
    click.echo("9.    Developer Configuration")
    click.echo("10.   Settings")
    click.echo("11.   Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_dockerfile()
    elif choice == 2:
        create_bash_script()
    elif choice == 3:
        create_k8s_config()
    elif choice == 4:
        create_ci_cd_pipeline()
    elif choice == 5:
        azure_menu()
    elif choice == 6:
        aws_menu()
    elif choice == 7:
        gcp_menu()
    elif choice == 8:
        firebase_menu()  # Call the Firebase menu
    elif choice == 9:
        developer_menu()
    elif choice == 10:
        settings_menu()
    elif choice == 11:
        main_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        coder_menu(main_menu)

def main_menu():
    click.echo("\n📋 Main Menu")
    click.echo("1. 📄 Agentic DevOps")
    click.echo("2. 🚀 Agentic Deployment")
    click.echo("3. ❓ Help")
    click.echo("4. 🔥 Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        coder_menu(main_menu)
    elif choice == 2:
        deployment_menu()
    elif choice == 3:
        click.echo("\nHelp menu...")  # Define your help functionality here
        main_menu()
    elif choice == 4:
        click.echo("\n👋 Exiting. Goodbye!\n")
        sys.exit(0)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        main_menu()

if __name__ == '__main__':
    check_and_install_aider()
    main_menu()
