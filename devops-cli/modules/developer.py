# modules/developer.py is a new file that contains the developer_menu function. This function displays a menu for developer-related configurations and allows the user to create .nix configuration, virtual environment (venv), and .devcontainer configuration. The user can also go back to the main menu from this menu.
import click
from modules.utils import run_aider_command

def create_nix_config():
    click.echo("\n🔧 Creating .nix Configuration...")
    instructions = click.prompt("Provide .nix configuration instructions", default="Create a basic Nix configuration.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./default.nix"
    run_aider_command(instructions, [config_path])
    click.echo("✅ .nix Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def create_venv():
    click.echo("\n🔧 Creating Virtual Environment (venv)...")
    instructions = click.prompt("Provide venv creation instructions", default="Create a Python virtual environment.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    venv_path = "./venv"
    run_aider_command(instructions, [venv_path])
    click.echo("✅ Virtual Environment created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def create_devcontainer():
    click.echo("\n🔧 Creating .devcontainer Configuration...")
    instructions = click.prompt("Provide .devcontainer configuration instructions", default="Create a basic .devcontainer.json for a VS Code environment.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./.devcontainer/devcontainer.json"
    run_aider_command(instructions, [config_path])
    click.echo("✅ .devcontainer Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def developer_menu():
    click.echo("\n🛠️ Developer Configuration")
    click.echo("1. Create .nix Configuration")
    click.echo("2. Create Virtual Environment (venv)")
    click.echo("3. Create .devcontainer Configuration")
    click.echo("4. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_nix_config()
    elif choice == 2:
        create_venv()
    elif choice == 3:
        create_devcontainer()
    elif choice == 4:
        import coder
        coder.coder_menu(coder.main_menu)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        developer_menu()
