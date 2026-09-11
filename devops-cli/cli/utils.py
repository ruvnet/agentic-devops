raise RuntimeError("Retired unsafe legacy execution path. Use Node 22+: node src/cli.mjs status. See docs/migration.md.")

import click
import subprocess
import os
import sys
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
import importlib.metadata as metadata
from main import main_menu

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
        'AZURE_APP_CONFIG_CONNECTION_STRING': 'AZURE_APP_CONFIG_CON_STR'
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


def run_aider_command(instructions, pipeline_path):
    click.echo(f"Running aider command with instructions: {instructions}")
    # Implement the actual functionality as needed
    # Placeholder implementation
    click.echo(f"Pipeline path: {pipeline_path}")
