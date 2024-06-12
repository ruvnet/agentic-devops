# modules/ci_cd.py is a new file that contains the create_ci_cd_pipeline function. This function is called when the user selects the "Create CI/CD Pipeline" option from the coder_menu function in coder.py. The create_ci_cd_pipeline function prompts the user to provide instructions for creating a CI/CD pipeline configuration and optional guidance for the AI. It then creates a CI/CD pipeline configuration file based on the user's input.

import click
from modules.utils import run_aider_command

def create_ci_cd_pipeline():
    click.echo("\n🚀 Creating CI/CD Pipeline Configuration...")
    instructions = click.prompt("Provide CI/CD pipeline creation instructions", default="Create a CI/CD pipeline for a Python project.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    pipeline_path = "./.github/workflows/ci-cd-pipeline.yml"
    run_aider_command(instructions, [pipeline_path])
    click.echo("✅ CI/CD Pipeline Configuration created successfully.")
    import coder
    coder.coder_menu(coder.main_menu)  # Call the coder menu again
