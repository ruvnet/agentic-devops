raise RuntimeError("Retired unsafe legacy execution path. Use Node 22+: node src/cli.mjs status. See docs/migration.md.")

# main.py and coder.py are two separate files. The main.py file contains the main CLI logic, while the coder.py file contains the menu options and functions related to the coder module. The main.py file imports the coder module and calls the coder_menu function to display the coder menu options.
import click
import subprocess
import importlib.metadata as metadata
import os
import sys
# from lionagi import Session
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.appconfiguration import AzureAppConfigurationClient
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor

# Add import for the coder module
import coder
from coder import coder_menu


# Define intents
intents = {
    "help": ["help", "assist", "how to", "guide"],
    "deploy": ["deploy", "deployment", "create deployment", "build"],
    "update": ["update", "upgrade", "modify"],
    "remove": ["remove", "delete", "destroy"],
    "status": ["status", "state", "condition", "list"],
    "suggest": ["suggest", "recommend", "advice", "idea"],
    "explain": ["explain", "describe", "details"],
    "auth": ["auth", "authenticate", "login", "sign in"],
    "browse": ["browse", "open", "view"],
    "codespace": ["codespace", "connect", "manage"],
    "gist": ["gist", "snippets", "manage gists"],
    "issue": ["issue", "bug", "ticket", "problem"],
    "org": ["org", "organization", "group"],
    "pr": ["pr", "pull request", "merge"],
    "project": ["project", "work", "task"],
    "release": ["release", "version", "publish"],
    "repo": ["repo", "repository", "codebase"],
    "run": ["run", "execute", "workflow"],
    "workflow": ["workflow", "pipeline", "automation"],
    "cache": ["cache", "store", "save"],
    "alias": ["alias", "shortcut", "command"],
    "api": ["api", "request", "endpoint"],
    "secret": ["secret", "credential", "key"],
    "ssh-key": ["ssh-key", "key", "ssh"],
    "variable": ["variable", "env", "environment"],
    "search": ["search", "find", "query"]
}

@click.group()
def cli():
    pass

def main():
    click.echo("🔍 Checking for installed packages and requirements...")
    check_installation()
    click.echo("🔍 Checking for required CLI tools...")
    check_cli_tools()
    click.echo("🔍 Validating Azure keys...")
    validate_azure_keys()

    click.echo(r"""
        ___                    __  _         ____                            
       /   | ____ ____  ____  / /_(______   / __ \___ _   ______  ____  _____
      / /| |/ __ `/ _ \/ __ \/ __/ / ___/  / / / / _ | | / / __ \/ __ \/ ___/
     / ___ / /_/ /  __/ / / / /_/ / /__   / /_/ /  __| |/ / /_/ / /_/ (__  ) 
    /_/  |_\__, /\___/_/ /_/\__/_/\___/  /_____/\___/|___/\____/ .___/____/  
          /____/                                              /_/            

    Welcome to Wizard of DevOps! Let's get started with your DevOps tasks.
    """)
    main_menu()


@cli.command()
def welcome():
    click.echo(r"""
        ___                    __  _         ____                            
       /   | ____ ____  ____  / /_(______   / __ \___ _   ______  ____  _____
      / /| |/ __ `/ _ \/ __ \/ __/ / ___/  / / / / _ | | / / __ \/ __ \/ ___/
     / ___ / /_/ /  __/ / / / /_/ / /__   / /_/ /  __| |/ / /_/ / /_/ (__  ) 
    /_/  |_\__, /\___/_/ /_/\__/_/\___/  /_____/\___/|___/\____/ .___/____/  
          /____/                                              /_/            

    Welcome to Wizard of DevOps! Let's get started with your DevOps tasks.
    """)
    main_menu()

# Utility functions
def check_installation():
    click.echo("🔍 Checking for installed packages and requirements...")
    required_packages = ['click', 'azure-identity', 'azure-mgmt-resource', 'azure-mgmt-web', 'azure-appconfiguration', 'pytest']
    installed_packages = {pkg.metadata['Name'] for pkg in metadata.distributions()}
    for package in required_packages:
        if package not in installed_packages:
            click.echo(f"📦 Package {package} is not installed. Installing...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        else:
            click.echo(f"✅ Package {package} is already installed.")
    click.echo("✅ All required packages are installed.")

def check_cli_tools():
    click.echo("🔍 Checking for required CLI tools...")
    required_tools = {'gh': 'https://github.com/cli/cli#installation', 'az': 'https://aka.ms/InstallAzureCLIDeb'}
    for tool, install_url in required_tools.items():
        if subprocess.call(['which', tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
            if tool == 'az':
                click.echo(f"📦 {tool} CLI is not installed. Installing...")
                subprocess.check_call("curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash", shell=True)
            else:
                click.echo(f"❌ {tool} CLI is not installed. Please install {tool} CLI manually from {install_url}.")
                sys.exit(1)
    click.echo("✅ All required CLI tools are installed.")

def validate_azure_keys():
    click.echo("🔍 Validating Azure keys...")
    required_keys = {
        'AZURE_CLIENT_ID': 'AZURE_CLIENT_ID',
        'AZURE_CLIENT_SECRET': 'AZURE_CLIENT_SECRET',
        'AZURE_APP_CONFIG_CON_STR': 'AZURE_APP_CONFIG_CON_STR'
    }
    for env_var, secret_name in required_keys.items():
        value = os.getenv(env_var) or os.getenv(secret_name)
        if not value:
            value = click.prompt(f"🔑 Please enter your {env_var}", hide_input=False)
        os.environ[env_var] = value
    click.echo("✅ All essential Azure keys are set.")

def verbose_output(message):
    click.echo(f"📝 {message}")

def run_tests():
    click.echo("🧪 Running tests...")
    result = subprocess.run(['pytest'], capture_output=True, text=True)
    click.echo(result.stdout)
    if result.returncode != 0:
        click.echo("❌ Tests failed:", result.stderr)
        raise Exception("Tests failed")
    click.echo("✅ All tests passed.")

# Command functions
def get_subscription_id():
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        subscription_id = click.prompt("🔑 Please enter your AZURE_SUBSCRIPTION_ID", hide_input=False)
        os.environ['AZURE_SUBSCRIPTION_ID'] = subscription_id
    return subscription_id

def list_deployments_cmd():
    try:
        click.echo("\n🔍 Fetching Azure subscription ID...")
        subscription_id = get_subscription_id()
        click.echo(f"🔑 Subscription ID: {subscription_id}")
        
        click.echo("\n🔍 Initializing Azure credentials...")
        credential = DefaultAzureCredential()
        
        click.echo("\n🔍 Creating Resource Management Client...")
        resource_client = ResourceManagementClient(credential, subscription_id)
        
        click.echo("\n🔍 Listing deployments...")
        deployments = resource_client.deployments.list_at_subscription_scope()
        
        click.echo("\n🔍 Fetching deployment details...")
        for deployment in deployments:
            click.echo(f"🌐 Name: {deployment.name}, Resource Group: {deployment.resource_group}, State: {deployment.properties.provisioning_state}")
        
        click.echo("\n✅ Deployment listing completed successfully.\n")
        
    except ClientAuthenticationError as e:
        click.echo(f"\n⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
        
    except Exception as e:
        click.echo(f"\n⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")
    
    main_menu()

def setup_deployment_cmd():
    try:
        click.echo("\n🔍 Fetching Azure subscription ID...")
        subscription_id = get_subscription_id()
        click.echo(f"🔑 Subscription ID: {subscription_id}")
        
        click.echo("\n🔍 Initializing Azure credentials...")
        credential = DefaultAzureCredential()
        
        click.echo("\n🔍 Creating Resource Management Client...")
        resource_client = ResourceManagementClient(credential, subscription_id)
        
        resource_group = click.prompt("Enter Resource Group name", type=str)
        location = "eastus"
        resource_client.resource_groups.create_or_update(resource_group, {'location': location})
        click.echo(f"🏗️ Resource Group {resource_group} created in {location}")
        
    except ClientAuthenticationError as e:
        click.echo(f"\n⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
        
    except Exception as e:
        click.echo(f"\n⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")
    
    main_menu()

def create_deployment_cmd():
    try:
        click.echo("\n🔍 Fetching Azure subscription ID...")
        subscription_id = get_subscription_id()
        click.echo(f"🔑 Subscription ID: {subscription_id}")
        
        click.echo("\n🔍 Initializing Azure credentials...")
        credential = DefaultAzureCredential()
        
        click.echo("\n🔍 Creating Web Site Management Client...")
        web_client = WebSiteManagementClient(credential, subscription_id)
        
        app_name = click.prompt("Enter App Name", type=str)
        resource_group = click.prompt("Enter Resource Group name", type=str)
        app_service_plan = click.prompt("Enter App Service Plan", type=str)
        
        click.echo("\n🚀 Creating deployment...")
        web_client.web_apps.create_or_update(resource_group, app_name, {
            'location': 'eastus',
            'server_farm_id': app_service_plan,
            'site_config': {
                'app_settings': [
                    {'name': 'SOME_SETTING', 'value': 'some_value'}
                ]
            }
        })
        click.echo(f"\n🚀 Deployment {app_name} created.\n")
        
    except ClientAuthenticationError as e:
        click.echo(f"\n⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
        
    except Exception as e:
        click.echo(f"\n⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")
    
    main_menu()

def update_deployment_cmd():
    try:
        click.echo("\n🔍 Fetching Azure subscription ID...")
        subscription_id = get_subscription_id()
        click.echo(f"🔑 Subscription ID: {subscription_id}")
        
        click.echo("\n🔍 Initializing Azure credentials...")
        credential = DefaultAzureCredential()
        
        click.echo("\n🔍 Creating Web Site Management Client...")
        web_client = WebSiteManagementClient(credential, subscription_id)
        
        app_name = click.prompt("Enter App Name", type=str)
        resource_group = click.prompt("Enter Resource Group name", type=str)
        
        click.echo("\n🔄 Updating deployment...")
        web_client.web_apps.create_or_update(resource_group, app_name, {
            'location': 'eastus',
            'site_config': {
                'app_settings': [
                    {'name': 'UPDATED_SETTING', 'value': 'updated_value'}
                ]
            }
        })
        click.echo(f"\n🔄 Deployment {app_name} updated.\n")
        
    except ClientAuthenticationError as e:
        click.echo(f"\n⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
        
    except Exception as e:
        click.echo(f"\n⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")
    
    main_menu()

def remove_deployment_cmd():
    try:
        click.echo("\n🔍 Fetching Azure subscription ID...")
        subscription_id = get_subscription_id()
        click.echo(f"🔑 Subscription ID: {subscription_id}")
        
        click.echo("\n🔍 Initializing Azure credentials...")
        credential = DefaultAzureCredential()
        
        click.echo("\n🔍 Creating Web Site Management Client...")
        web_client = WebSiteManagementClient(credential, subscription_id)
        
        app_name = click.prompt("Enter App Name", type=str)
        resource_group = click.prompt("Enter Resource Group name", type=str)
        
        click.echo("\n🗑️ Removing deployment...")
        web_client.web_apps.delete(resource_group, app_name)
        click.echo(f"\n🗑️ Deployment {app_name} removed.\n")
        
    except ClientAuthenticationError as e:
        click.echo(f"\n⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
        
    except Exception as e:
        click.echo(f"\n⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")
    
    main_menu()

def main_menu():
    click.echo("\n📋 Main Menu")
    click.echo("1. 📄 Agentic DevOps")
    click.echo("2. 🚀 Agentic Deployment")
    click.echo("3. ❓ Help")
    click.echo("4. 🔥 Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        coder_menu(main_menu)
    elif choice == 2:
        deployment_menu()
    elif choice == 3:
        click.echo("\nHelp menu...")  # Define your help functionality here
        main_menu()
    elif choice == 4:
        click.echo("\n👋 Exiting. Goodbye!\n")
        sys.exit(0)
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        main_menu()

def deployment_menu():
    click.echo("\n🚀 Agentic Deployment")
    click.echo("1. 📃 List Deployments")
    click.echo("2. 🛠️ Setup Deployment")
    click.echo("3. 🚀 Create Deployment")
    click.echo("4. 🔄 Update Deployment")
    click.echo("5. ❌ Remove Deployment")
    click.echo("6. 🔙 Return to Main Menu")

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
        main_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        deployment_menu()

async def agentic_chat():
    # session = await initialize_lionagi_session()
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

@click.command()
def run():
    """
    Start the interactive menu or chat UI.
    """
    welcome()  # Display the welcome message
    mode = click.prompt("Choose mode (1: Menu, 2: Chat)", type=int)
    if mode == 1:
        main_menu()
    elif mode == 2:
        asyncio.run(agentic_chat())
    else:
        click.echo("❌ Invalid choice. Please choose 1 for Menu or 2 for Chat.")
        main_menu()
 
if __name__ == '__main__':
    check_installation()
    check_cli_tools()
    validate_azure_keys()
    run()
