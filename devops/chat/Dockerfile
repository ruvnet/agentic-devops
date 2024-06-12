# Base Image
FROM python:3.8-slim

# Maintainer
LABEL maintainer="Your Name <you@example.com>"

# Install necessary packages
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "main.py"]
