import click
import subprocess
import os
from pathlib import Path

settings = {
    "model": "gpt-4o",
    "weak_model": "gpt-3.5-turbo",
    "max_tokens": 1024
}

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

def create_dockerfile():
    click.echo("\n🚀 Creating Dockerfile...")
    instructions = click.prompt("Provide Dockerfile creation instructions", default="Create a Dockerfile for a Python web app.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    dockerfile_path = "./Dockerfile"
    apply_file = str(Path(dockerfile_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ Dockerfile created successfully.")
    coder_menu()

def create_bash_script():
    click.echo("\n🚀 Creating Bash Script...")
    instructions = click.prompt("Provide Bash script creation instructions", default="Create a basic deployment script.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    script_path = "./script.sh"
    apply_file = str(Path(script_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ Bash Script created successfully.")
    coder_menu()

def create_k8s_config():
    click.echo("\n🚀 Creating Kubernetes Configuration...")
    instructions = click.prompt("Provide Kubernetes configuration instructions", default="Create a Kubernetes config for a web application.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./k8s-config.yml"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ Kubernetes Configuration created successfully.")
    coder_menu()

def create_ci_cd_pipeline():
    click.echo("\n🚀 Creating CI/CD Pipeline Configuration...")
    instructions = click.prompt("Provide CI/CD pipeline creation instructions", default="Create a CI/CD pipeline for a Python project.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    pipeline_path = "./.github/workflows/ci-cd-pipeline.yml"
    apply_file = str(Path(pipeline_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ CI/CD Pipeline Configuration created successfully.")
    coder_menu()

def create_azure_config():
    click.echo("\n🌐 Creating Azure Configuration...")
    instructions = click.prompt("Provide Azure configuration instructions", default="Create an Azure Resource Manager template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./azure-config.json"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ Azure Configuration created successfully.")
    coder_menu()

def create_aws_config():
    click.echo("\n🌐 Creating AWS Configuration...")
    instructions = click.prompt("Provide AWS configuration instructions", default="Create a CloudFormation template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./aws-config.yml"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ AWS Configuration created successfully.")
    coder_menu()

def create_gcp_config():
    click.echo("\n🌐 Creating GCP Configuration...")
    instructions = click.prompt("Provide GCP configuration instructions", default="Create a Google Cloud Deployment Manager template.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./gcp-config.yaml"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ GCP Configuration created successfully.")
    coder_menu()

def create_nix_config():
    click.echo("\n🔧 Creating .nix Configuration...")
    instructions = click.prompt("Provide .nix configuration instructions", default="Create a basic Nix configuration.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./default.nix"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ .nix Configuration created successfully.")
    coder_menu()

def create_venv():
    click.echo("\n🔧 Creating Virtual Environment (venv)...")
    instructions = click.prompt("Provide venv creation instructions", default="Create a Python virtual environment.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    venv_path = "./venv"
    apply_file = str(Path(venv_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ Virtual Environment created successfully.")
    coder_menu()

def create_devcontainer():
    click.echo("\n🔧 Creating .devcontainer Configuration...")
    instructions = click.prompt("Provide .devcontainer configuration instructions", default="Create a basic .devcontainer.json for a VS Code environment.")
    guidance = click.prompt("Provide any initial optional guidance for the AI (press Enter to skip)", default="", show_default=False)
    if guidance:
        instructions = f"{guidance}. {instructions}"
    config_path = "./.devcontainer/devcontainer.json"
    apply_file = str(Path(config_path).resolve())
    run_aider_command(instructions, [apply_file])
    click.echo("✅ .devcontainer Configuration created successfully.")
    coder_menu()

def update_settings():
    click.echo("\n🛠️ Update Settings")
    settings["model"] = click.prompt("Enter model to use", default=settings["model"])
    settings["weak_model"] = click.prompt("Enter weak model to use", default=settings["weak_model"])
    settings["max_tokens"] = click.prompt("Enter max tokens", default=settings["max_tokens"], type=int)
    click.echo("✅ Settings updated successfully.")
    settings_menu()

def view_settings():
    click.echo("\n🔧 Current Settings")
    for key, value in settings.items():
        click.echo(f"{key}: {value}")
    settings_menu()

def settings_menu():
    click.echo("\n📋 Settings Menu")
    click.echo("1. View Settings")
    click.echo("2. Update Settings")
    click.echo("3. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        view_settings()
    elif choice == 2:
        update_settings()
    elif choice == 3:
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        settings_menu()

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
        create_bash_script()  # You can adjust this to a more specific function if needed
    elif choice == 3:
        click.echo("\n🚀 Creating Azure Policy...")
        create_azure_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        azure_menu()

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
        create_bash_script()  # You can adjust this to a more specific function if needed
    elif choice == 3:
        click.echo("\n🚀 Creating IAM Policy...")
        create_aws_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        aws_menu()

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
        create_bash_script()  # You can adjust this to a more specific function if needed
    elif choice == 3:
        click.echo("\n🚀 Creating GCP IAM Policy...")
        create_gcp_config()  # You can adjust this to a more specific function if needed
    elif choice == 4:
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        gcp_menu()

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
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        developer_menu()

def coder_menu():
    click.echo("\n📋 Agentic DevOps Menu")
    click.echo("1. Create Dockerfile")
    click.echo("2. Create Bash Script")
    click.echo("3. Create Kubernetes Configuration")
    click.echo("4. Create CI/CD Pipeline")
    click.echo("5. Azure Configuration")
    click.echo("6. AWS Configuration")
    click.echo("7. GCP Configuration")
    click.echo("8. Developer Configuration")
    click.echo("9. Settings")
    click.echo("10. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        create_dockerfile()
    elif choice == 2:
        create_bash_script()
    elif choice == 3:
        create_k8s_config()
    elif choice == 4:
        create_ci_cd_pipeline()
    elif choice == 5:
        azure_menu()
    elif choice == 6:
        aws_menu()
    elif choice == 7:
        gcp_menu()
    elif choice == 8:
        developer_menu()
    elif choice == 9:
        settings_menu()
    elif choice == 10:
        from cli import main_menu
        main_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        coder_menu()

if __name__ == '__main__':
    coder_menu()