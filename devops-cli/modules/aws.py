# modules/aws.py is a new file that contains the create_aws_config function. This function is called when the user selects the "Create AWS Configuration" option from the coder_menu function in coder.py. The create_aws_config function prompts the user to provide instructions for creating an AWS configuration and optional guidance for the AI. It then creates an AWS configuration file based on the user's input.

import click
from modules.utils import run_aider_command

def create_aws_config():
    click.echo("\n🌐 Creating AWS Configuration...")
    instructions = click.prompt("Provide AWS configuration instructions", default="Create a CloudFormation template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./aws-config.yml"
    run_aider_command(instructions, [config_path])
    click.echo("✅ AWS Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again

def aws_menu():
    click.echo("\n🌐 AWS Configuration")
    click.echo("1. Create CloudFormation Template")
    click.echo("2. Create AWS CLI Script")
    click.echo("3. Create IAM Policy")
    click.echo("4. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_aws_config()
    elif choice == 2:
        click.echo("\n🚀 Creating AWS CLI Script...")
        import coder
        coder.create_bash_script()  # Adjust this if there's a more specific function for AWS CLI scripts
    elif choice == 3:
        click.echo("\n🚀 Creating IAM Policy...")
        create_aws_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        import coder
        coder.coder_menu(coder.main_menu)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        aws_menu()
