import click
import sys
from cli.utils import (
    list_deployments_cmd,
    setup_deployment_cmd,
    create_deployment_cmd,
    update_deployment_cmd,
    remove_deployment_cmd
)
import coder

def main_menu():
    click.echo("\n📋 Main Menu")
    click.echo("1. List Deployments")
    click.echo("2. Setup Deployment")
    click.echo("3. Create Deployment")
    click.echo("4. Update Deployment")
    click.echo("5. Remove Deployment")
    click.echo("6. Load Coder Menu")  # New menu option to load coder menu
    click.echo("7. Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        list_deployments_cmd()
    elif choice == 2:
        setup_deployment_cmd()
    elif choice == 3:
        create_deployment_cmd()
    elif choice == 4:
        update_deployment_cmd()
    elif choice == 5:
        remove_deployment_cmd()
    elif choice == 6:
        coder.coder_menu()  # Call the coder menu function
    elif choice == 7:
        click.echo("\n👋 Exiting. Goodbye!\n")
        sys.exit(0)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        main_menu()
