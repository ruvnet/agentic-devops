import click
from modules.utils import run_aider_command

def create_dockerfile():
    click.echo("\n🚀 Creating Dockerfile...")
    instructions = click.prompt("Provide Dockerfile creation instructions", default="Create a Dockerfile for a Python web app.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    dockerfile_path = "./Dockerfile"
    run_aider_command(instructions, [dockerfile_path])
    click.echo("✅ Dockerfile created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again
