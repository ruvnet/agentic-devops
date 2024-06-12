#modules/azure.py is a new file that contains the create_azure_config function. This function is called when the user selects the "Create Azure Configuration" option from the coder_menu function in coder.py. The create_azure_config function prompts the user to provide instructions for creating an Azure configuration and optional guidance for the AI. It then creates an Azure configuration file based on the user's input.

import click
from modules.utils import run_aider_command

def create_azure_config():
    click.echo("\n🌐 Creating Azure Configuration...")
    instructions = click.prompt("Provide Azure configuration instructions", default="Create an Azure Resource Manager template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./azure-config.json"
    run_aider_command(instructions, [config_path])
    click.echo("✅ Azure Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def azure_menu():
    click.echo("\n🌐 Azure Configuration")
    click.echo("1. Create ARM Template")
    click.echo("2. Create Azure CLI Script")
    click.echo("3. Create Azure Policy")
    click.echo("4. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_azure_config()
    elif choice == 2:
        click.echo("\n🚀 Creating Azure CLI Script...")
        import coder
        coder.create_bash_script()  # Adjust this if there's a more specific function for Azure CLI scripts
    elif choice == 3:
        click.echo("\n🚀 Creating Azure Policy...")
        create_azure_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        import coder
        coder.coder_menu(coder.main_menu)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        azure_menu()
