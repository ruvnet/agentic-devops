import click
import os
from modules.utils import run_aider_command

def ensure_firebase_folder():
    if not os.path.exists('./firebase'):
        os.makedirs('./firebase')

def create_firebase_config():
    click.echo("\n🌐 Creating Firebase Configuration...")
    instructions = click.prompt("Provide Firebase configuration instructions", default="Create a basic Firebase configuration.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    ensure_firebase_folder()
    config_path = "./firebase/firebase-config.json"
    run_aider_command(instructions, [config_path])
    click.echo("✅ Firebase Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def create_firestore_rules():
    click.echo("\n🌐 Creating Firestore Rules...")
    instructions = click.prompt("Provide Firestore rules instructions", default="Create Firestore security rules.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    ensure_firebase_folder()
    rules_path = "./firebase/firestore.rules"
    run_aider_command(instructions, [rules_path])
    click.echo("✅ Firestore Rules created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def create_firebase_cli_script():
    click.echo("\n🌐 Creating Firebase CLI Script...")
    instructions = click.prompt("Provide Firebase CLI script instructions", default="Create a Firebase CLI script for deployment.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    ensure_firebase_folder()
    script_path = "./firebase/firebase-cli.sh"
    run_aider_command(instructions, [script_path])
    click.echo("✅ Firebase CLI Script created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def firebase_menu():
    click.echo("\n🌐 Firebase Configuration")
    click.echo("1. Create Firebase Configuration")
    click.echo("2. Create Firestore Rules")
    click.echo("3. Create Firebase CLI Script")
    click.echo("4. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_firebase_config()
    elif choice == 2:
        create_firestore_rules()
    elif choice == 3:
        create_firebase_cli_script()
    elif choice == 4:
        import coder
        coder.coder_menu(coder.main_menu)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        firebase_menu()
