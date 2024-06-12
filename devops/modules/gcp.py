# modules/gcp.py is a new file that contains the create_gcp_config function. This function is called when the user selects the "Create GCP Configuration" option from the coder_menu function in coder.py. The create_gcp_config function prompts the user to provide instructions for creating a GCP configuration and optional guidance for the AI. It then creates a GCP configuration file based on the user's input.
import click
from modules.utils import run_aider_command

def create_gcp_config():
    click.echo("\n🌐 Creating GCP Configuration...")
    instructions = click.prompt("Provide GCP configuration instructions", default="Create a Google Cloud Deployment Manager template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./gcp-config.yaml"
    run_aider_command(instructions, [config_path])
    click.echo("✅ GCP Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def gcp_menu():
    click.echo("\n🌐 GCP Configuration")
    click.echo("1. Create Deployment Manager Template")
    click.echo("2. Create GCP CLI Script")
    click.echo("3. Create GCP IAM Policy")
    click.echo("4. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_gcp_config()
    elif choice == 2:
        click.echo("\n🚀 Creating GCP CLI Script...")
        import coder
        coder.create_bash_script()  # Adjust this if there's a more specific function for GCP CLI scripts
    elif choice == 3:
        click.echo("\n🚀 Creating GCP IAM Policy...")
        create_gcp_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        import coder
        coder.coder_menu(coder.main_menu)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        gcp_menu()
