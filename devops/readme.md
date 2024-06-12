# Deployment Instructions for ../chat Application on Azure

This document provides detailed instructions for deploying the `../chat` NodeJS NextJS application on Azure using Docker and the Azure CLI.

## Prerequisites

- Azure CLI installed
- Docker installed
- An Azure account and active subscription

## Environment Variables

Before you start the deployment, ensure the following environment variables are set. You will be prompted for any missing values when you run the `deploy.sh` script.

- `AZURE_CLIENT_ID`
- `AZURE_SECRET`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `RESOURCE_GROUP_NAME`
- `LOCATION`
- `REGISTRY_NAME`
- `DEEPGRAM_STT_DOMAIN` (default: `https://api.deepgram.com`)
- `DEEPGRAM_API_KEY`
- `OPENAI_API_KEY`
- `EXASEARCH_API_KEY`

## Steps

1. **Login to Azure CLI**: Run `az login` and follow the prompts to log in to your Azure account.

2. **Create a Resource Group**: Use the command `az group create --name <ResourceGroupName> --location <Location>` to create a new resource group in your preferred location.

3. **Create Azure Container Registry (ACR)**: Execute `az acr create --resource-group <ResourceGroupName> --name <RegistryName> --sku Basic --admin-enabled true` to create a container registry.

4. **Build Docker Image**: Navigate to the `../chat` directory and build your Docker image using `docker build -t <RegistryName>.azurecr.io/chat-app:v1 .`.

5. **Push Docker Image to ACR**: Log in to your ACR using `az acr login --name <RegistryName>` and then push your Docker image using `docker push <RegistryName>.azurecr.io/chat-app:v1`.

6. **Deploy to Azure Container Instances (ACI)**: Deploy your application using `az container create --resource-group <ResourceGroupName> --name chat-app-container --image <RegistryName>.azurecr.io/chat-app:v1 --cpu 1 --memory 1 --ports 3000 --dns-name-label chat-app --environment-variables NODE_ENV=production`.

7. **Access Your Application**: Once deployed, your application will be accessible at `http://chat-app.<Location>.azurecontainer.io:3000`.

## Using `deploy.sh` Script

For convenience, a `deploy.sh` script is provided to automate the deployment process. Before running the script, ensure it has execution permissions by running `chmod +x deploy.sh`.

To deploy using the script, simply execute `./deploy.sh` from the terminal. The script will guide you through the deployment process step by step and prompt you for any required environment variables that are not already set.

## Environment Variables for Dockerfile

The script will also update your Dockerfile to include the following environment variables:

- `EXASEARCH_API_KEY`
- `OPENAI_API_KEY`

## Database Configuration

No database is required for the deployment of this application.

## Additional Notes

- Ensure you replace placeholder values such as `<ResourceGroupName>`, `<Location>`, and `<RegistryName>` with your actual values.
- The deployment script `deploy.sh` includes verbose output and emojis for a more interactive deployment experience. It also checks for required components at startup.
- The script creates a `.env.local` file in the `../chat` directory to store `DEEPGRAM_STT_DOMAIN`, `DEEPGRAM_API_KEY`, and `OPENAI_API_KEY`.

For more detailed information on each step, refer to the official [Azure documentation](https://docs.microsoft.com/azure) and [Docker documentation](https://docs.docker.com).
