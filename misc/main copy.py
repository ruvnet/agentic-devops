import click
import subprocess
import importlib.metadata as metadata
import os
import sys
from lionagi import Session
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.appconfiguration import AzureAppConfigurationClient
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from cli.ci_cd_pipeline import create_ci_cd_pipeline
from cli.utils import (
    check_installation,
    check_cli_tools,
    validate_azure_keys,
    verbose_output,
    run_tests,
    list_deployments_cmd,
    setup_deployment_cmd,
    create_deployment_cmd,
    update_deployment_cmd,
    remove_deployment_cmd,
    get_subscription_id
)
from cli.agentic import initialize_lionagi_session, handle_user_input

@click.group()
def cli():
    pass

@cli.command()
def welcome():
    click.echo(r"""
        ___                    __  _         ____                            
       /   | ____ ____  ____  / /_(______   / __ \___ _   ______  ____  _____
      / /| |/ __ `/ _ \/ __ \/ __/ / ___/  / / / / _ | | / / __ \/ __ \/ ___/
     / ___ / /_/ /  __/ / / / /_/ / /__   / /_/ /  __| |/ / /_/ / /_/ (__  ) 
    /_/  |_\__, /\___/_/ /_/\__/_/\___/  /_____/\___/|___/\____/ .___/____/  
          /____/                                              /_/            

    Welcome to the CLI tool!
    """)

@cli.command()
def create_pipeline():
    create_ci_cd_pipeline()

@click.command()
def run():
    """
    Start the interactive menu or chat UI.
    """
    mode = click.prompt("Choose mode (1: Menu, 2: Chat)", type=int)
    if mode == 1:
        main_menu()
    elif mode == 2:
        asyncio.run(agentic_chat())
    else:
        click.echo("❌ Invalid choice. Please choose 1 for Menu or 2 for Chat.")
        main_menu()

def main_menu():
    click.echo("\n📋 Main Menu")
    click.echo("1. List Deployments")
    click.echo("2. Setup Deployment")
    click.echo("3. Create Deployment")
    click.echo("4. Update Deployment")
    click.echo("5. Remove Deployment")
    click.echo("6. Load Coder Menu")
    click.echo("7. Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        list_deployments_cmd()
    elif choice == 2:
        setup_deployment_cmd()
    elif choice == 3:
        create_deployment_cmd()
    elif choice == 4:
        update_deployment_cmd()
    elif choice == 5:
        remove_deployment_cmd()
    elif choice == 6:
        import coder
        coder.coder_menu()
    elif choice == 7:
        click.echo("\n👋 Exiting. Goodbye!\n")
        sys.exit(0)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        main_menu()

async def agentic_chat():
    session = await initialize_lionagi_session()
    click.echo("🚀 Welcome to the interactive DevOps chat! Type 'exit' to leave the chat.")
    
    while True:
        user_input = click.prompt("💬 You", type=str)

        if user_input.lower() in ['exit', 'quit']:
            click.echo("👋 Exiting chat mode. Goodbye!")
            break

        try:
            # Parse important elements from user input 
            repo_path = None
            if "../" in user_input:
                repo_path = user_input.split("../")[1].strip()
            elif "./" in user_input:
                repo_path = user_input.split("./")[1].strip()

            if repo_path:
                click.echo(f"🔍 Analyzing directory structure for {repo_path}...")
            else:
                # Ask for clarification if path not provided
                repo_path = click.prompt("Enter the path to the repository directory", type=str, default=".")
                click.echo(f"🔍 Analyzing directory structure for {repo_path}...")

            click.echo("📁 Listing files and directories...")
            files_and_dirs = subprocess.check_output(f"ls -lR {repo_path}", shell=True, text=True)

            # Chunk the directory information to limit tokens
            max_tokens = 2048  
            chunks = [files_and_dirs[i:i+max_tokens] for i in range(0, len(files_and_dirs), max_tokens)]

            review_results = []
            for chunk in chunks:
                click.echo("🤖 Sending directory information to LionAGI for review...")
                review_result = await handle_user_input(session, chunk)
                review_results.append(review_result)

            click.echo("🦁 LionAGI review:")
            for result in review_results:
                click.echo(result)

            click.echo("🤔 Generating potential actions based on the request...")
            action_prompt = f"User request: {user_input}\nDirectory information:\n{files_and_dirs}"
            potential_actions = await handle_user_input(session, action_prompt)

            click.echo("📝 Potential actions:")
            click.echo(potential_actions)

            execute_action = click.confirm("Do you want to execute any of the suggested actions?")
            if execute_action:
                selected_action = click.prompt("Enter the action you want to execute", type=str)
                click.echo(f"⚙️ Executing: {selected_action}") 
                subprocess.run(selected_action, shell=True, check=True)
            else:
                click.echo("⏭️ Skipping action execution.")

        except subprocess.CalledProcessError as e:
            click.echo(f"⚠️ Error: {e.output}")
        except Exception as e:
            click.echo(f"⚠️ Error: {e}")

if __name__ == '__main__':
    check_installation()
    check_cli_tools()
    validate_azure_keys()
    run()

