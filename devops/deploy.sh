#!/bin/bash

# Deployment script for ../chat NodeJS NextJS application on Azure using Docker and Azure CLI

echo "🚀 Starting deployment of ../chat application to Azure..."

# Function to prompt for input if environment variable is not set
prompt_for_input() {
    local var_name=$1
    local var_value=$(eval echo \$$var_name)
    if [ -z "$var_value" ]; then
        read -p "Enter $var_name: " var_value
        export $var_name=$var_value
    else
        echo "$var_name is set."
    fi
}

# Required environment variables
env_vars=(
    "AZURE_CLIENT_ID"
    "AZURE_SECRET"
    "AZURE_TENANT_ID"
    "AZURE_SUBSCRIPTION_ID"
    "RESOURCE_GROUP_NAME"
    "LOCATION"
    "REGISTRY_NAME"
    "DEEPGRAM_STT_DOMAIN"
    "DEEPGRAM_API_KEY"
    "OPENAI_API_KEY"
    "EXASEARCH_API_KEY"
)

# Prompt for missing environment variables
for var in "${env_vars[@]}"; do
    if [ "$var" == "DEEPGRAM_STT_DOMAIN" ]; then
        export DEEPGRAM_STT_DOMAIN=${DEEPGRAM_STT_DOMAIN:-"https://api.deepgram.com"}
    fi
    prompt_for_input $var
done

# Check for Azure CLI
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI could not be found. Please install Azure CLI to proceed."
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker could not be found. Please install Docker to proceed."
    exit 1
fi

# Login to Azure
echo "🔑 Logging into Azure..."
az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_SECRET --tenant $AZURE_TENANT_ID --output none
if [ $? -ne 0 ]; then
    echo "❌ Failed to log in to Azure."
    exit 1
fi

# Set Azure subscription
echo "📋 Setting Azure subscription..."
az account set --subscription $AZURE_SUBSCRIPTION_ID
if [ $? -ne 0 ]; then
    echo "❌ Failed to set Azure subscription."
    exit 1
fi

# Create resource group if it doesn't exist
echo "🛠️  Creating resource group..."
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION
if [ $? -ne 0 ]; then
    echo "❌ Failed to create resource group."
    exit 1
fi

# Create Azure Container Registry
echo "📦 Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP_NAME --name $REGISTRY_NAME --sku Basic --admin-enabled true
if [ $? -ne 0 ]; then
    echo "❌ Failed to create Azure Container Registry."
    exit 1
fi

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t $REGISTRY_NAME.azurecr.io/chat-app:v1 ../chat
if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker image."
    exit 1
fi

# Push Docker image to Azure Container Registry
echo "📤 Pushing Docker image to Azure Container Registry..."
az acr login --name $REGISTRY_NAME
docker push $REGISTRY_NAME.azurecr.io/chat-app:v1
if [ $? -ne 0 ]; then
    echo "❌ Failed to push Docker image to Azure Container Registry."
    exit 1
fi

# Deploy Docker container to Azure Container Instances
echo "🚢 Deploying Docker container to Azure Container Instances..."
az container create --resource-group $RESOURCE_GROUP_NAME --name chat-app-container --image $REGISTRY_NAME.azurecr.io/chat-app:v1 --cpu 1 --memory 1 --ports 3000 --dns-name-label chat-app --environment-variables NODE_ENV=production
if [ $? -ne 0 ]; then
    echo "❌ Failed to deploy Docker container to Azure Container Instances."
    exit 1
fi

# Create .env.local file in ../chat directory
echo "📄 Creating .env.local file..."
cat <<EOF > ../chat/.env.local
DEEPGRAM_STT_DOMAIN=$DEEPGRAM_STT_DOMAIN
DEEPGRAM_API_KEY=$DEEPGRAM_API_KEY
OPENAI_API_KEY=$OPENAI_API_KEY
EOF

# Update Dockerfile to use environment variables
echo "🔧 Updating Dockerfile to use environment variables..."
cat <<EOF >> ../chat/Dockerfile

# Set environment variables for Docker
ENV EXASEARCH_API_KEY=$EXASEARCH_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
EOF

echo "✅ Deployment completed successfully. Your application is now running at http://chat-app.$LOCATION.azurecontainer.io:3000"
echo "🦄 rUv loves ya."
