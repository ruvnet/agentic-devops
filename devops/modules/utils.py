import click
import subprocess

def run_aider_command(instructions, file_paths):
    command = ["aider"] + file_paths + ["-m", instructions]
    click.echo(f"Running command: {' '.join(command)}")  # Verbose output

    # Running the command without capturing the output to show interactive UI
    process = subprocess.run(command)

    if process.returncode != 0:
        click.echo(f"Error: Aider exited with code {process.returncode}")
        fix_errors(file_paths)

def fix_errors(file_paths):
    command = ["aider"] + file_paths + ["--fix"]
    click.echo(f"Running error fix command: {' '.join(command)}")  # Verbose output

    # Running the command without capturing the output to show interactive UI
    subprocess.run(command)
