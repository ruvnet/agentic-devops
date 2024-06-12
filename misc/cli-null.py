import os
import click
import subprocess
import pkg_resources
import sys
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

 
# Utility functions
def check_installation():
    click.echo("🔍 Checking for installed packages and requirements...")
    required_packages = ['click', 'azure-identity', 'azure-mgmt-resource', 'azure-mgmt-web', 'azure-appconfiguration', 'pytest', 'python-dotenv']
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
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
        'AZURE_TENANT_ID': 'AZURE_TENANT_ID',
        'AZURE_SUBSCRIPTION_ID': 'AZURE_SUBSCRIPTION_ID'
    }
    for env_var in required_keys:
        value = os.getenv(env_var)
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
        subscription_id = get_subscription_id()
        credential = ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
        resource_client = ResourceManagementClient(credential, subscription_id)
        deployments = resource_client.deployments.list_at_subscription_scope()
        for deployment in deployments:
            click.echo(f"🌐 Name: {deployment.name}, Resource Group: {deployment.resource_group}, State: {deployment.properties.provisioning_state}")
    except ClientAuthenticationError as e:
        click.echo(f"⚠️ Authentication Error: {e}")
        click.echo("🔧 Please ensure that the client secret is correct and not the client secret ID. You can update the secret and try again.")
        click.echo("🔗 Troubleshooting: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot")
    except Exception as e:
        click.echo(f"⚠️ Error: {e}")
        click.echo("🔧 Please ensure that the service principal has the required permissions. You can assign the 'Owner' role to the service principal using the Azure Portal or Azure CLI.")
        click.echo("🔗 Documentation: https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps")

def main_menu():
    click.echo("📋 Main Menu")
    click.echo("1. List Deployments")
    click.echo("2. Setup Deployment")
    click.echo("3. Create Deployment")
    click.echo("4. Update Deployment")
    click.echo("5. Remove Deployment")
    click.echo("6. Exit")

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
        click.echo("👋 Exiting. Goodbye!")
        sys.exit(0)
    else:
        click.echo("❌ Invalid choice. Please try again.")

@click.command()
def run():
    """
    Start the interactive menu or chat UI.
    """
    check_installation()
    check_cli_tools()
    validate_azure_keys()

    mode = click.prompt("Choose mode (1: Menu, 2: Chat)", type=int)
    if mode == 1:
        main_menu()
    elif mode == 2:
        asyncio.run(agentic_chat())
    else:
        click.echo("❌ Invalid choice. Please choose 1 for Menu or 2 for Chat.")

if __name__ == '__main__':
    run()
