# coder.py is a new file that contains the main_menu and coder_menu functions. The main_menu function displays the main menu options and prompts the user to choose an option. The coder_menu function displays the Agentic DevOps menu options and calls the appropriate function based on the user's choice. The coder_menu function is called recursively to allow the user to navigate back to the main menu.
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

def start_webui():
    click.echo("\n🚀 Starting Agentic DevOps WebUI...")
    try:
        subprocess.check_call(["aider", "--gui"])
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start WebUI: {e}")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again


def coder_menu(main_menu):
    click.echo("\n📋 Agentic DevOps Menu")
    click.echo("1.    Start Agentic DevOps WebUI")
    click.echo("2.    Create Dockerfile")
    click.echo("3.    Create Bash Script")
    click.echo("4.    Create Kubernetes Configuration")
    click.echo("5.    Create CI/CD Pipeline")
    click.echo("6.    Azure Configuration")
    click.echo("7.    AWS Configuration")
    click.echo("8.    GCP Configuration")
    click.echo("9.    Firebase Configuration")
    click.echo("10.   Developer Configuration")
    click.echo("11.   Settings")
    click.echo("12.   Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        start_webui()
    elif choice == 2:
        create_dockerfile()
    elif choice == 3:
        create_bash_script()
    elif choice == 4:
        create_k8s_config()
    elif choice == 5:
        create_ci_cd_pipeline()
    elif choice == 6:
        azure_menu()
    elif choice == 7:
        aws_menu()
    elif choice == 8:
        gcp_menu()
    elif choice == 9:
        firebase_menu()  # Call the Firebase menu
    elif choice == 10:
        developer_menu()
    elif choice == 11:
        settings_menu()
    elif choice == 12:
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
