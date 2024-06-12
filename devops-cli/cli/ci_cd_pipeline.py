import click
from .utils import run_aider_command

def create_ci_cd_pipeline():
    click.echo("\n🚀 Creating CI/CD Pipeline Configuration...")
    instructions = click.prompt("Provide CI/CD pipeline creation instructions", default="Create a CI/CD pipeline for a Python project.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    pipeline_path = "./.github/workflows/ci-cd-pipeline.yml"
    run_aider_command(instructions, [pipeline_path])
    click.echo("✅ CI/CD Pipeline Configuration created successfully.")
    from ..coder import coder_menu
    coder_menu()
