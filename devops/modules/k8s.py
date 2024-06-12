# modules/k8s.py is a new file that contains the create_k8s_config function. This function is called when the user selects the "Create Kubernetes Configuration" option from the coder_menu function in coder.py. The create_k8s_config function prompts the user to provide instructions for creating a Kubernetes configuration and optional guidance for the AI. It then creates a Kubernetes configuration file based on the user's input.
import click
from modules.utils import run_aider_command

def create_k8s_config():
    click.echo("\n🚀 Creating Kubernetes Configuration...")
    instructions = click.prompt("Provide Kubernetes configuration instructions", default="Create a Kubernetes config for a web application.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./k8s-config.yml"
    run_aider_command(instructions, [config_path])
    click.echo("✅ Kubernetes Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again
