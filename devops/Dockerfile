# Use the official Microsoft Azure CLI image as the base image
FROM mcr.microsoft.com/azure-cli

# Set the working directory
WORKDIR /app

# Copy the output directory to the container
COPY ./output/ .

# Set the default command to deploy to Azure
CMD ["az", "deployment", "group", "create", "--resource-group", "myResourceGroup", "--template-file", "azuredeploy.json", "--parameters", "@azuredeploy.parameters.json"]
