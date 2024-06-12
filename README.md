```
        ___                    __  _         ____                            
       /   | ____ ____  ____  / /_(______   / __ \___ _   ______  ____  _____
      / /| |/ __ `/ _ \/ __ \/ __/ / ___/  / / / / _ | | / / __ \/ __ \/ ___/
     / ___ / /_/ /  __/ / / / /_/ / /__   / /_/ /  __| |/ / /_/ / /_/ (__  ) 
    /_/  |_\__, /\___/_/ /_/\__/_/\___/  /_____/\___/|___/\____/ .___/____/  
          /____/                                              /_/            

    Welcome to Wizard of DevOps! Let's get started with your DevOps tasks.
```

# Agentic DevOps 

[![Agentic Engineering](https://raw.githubusercontent.com/ruvnet/agentic-devops/main/assets/2.png)](https://devops.ruv.io)

## Introduction

The Agentic DevOps tool is designed to streamline and automate various DevOps tasks and configurations. This versatile tool supports both a command-line interface (CLI) and a web-based user interface (WebUI), making it accessible for both terminal enthusiasts and those who prefer a graphical interface. 


### What It Does

Agentic DevOps automates the creation of essential DevOps artifacts such as Dockerfiles, Bash scripts, Kubernetes configurations, CI/CD pipelines, and cloud configurations for major providers like Azure, AWS, GCP, Firebase, Supabase, and Cloudflare. It also supports different development architectures, including microservices, serverless, monolithic, event-driven, and API-first development.

### Why It's Useful

By automating repetitive and complex tasks, Agentic DevOps helps reduce human error, speed up deployment processes, and ensure consistent configurations across different environments. It's particularly useful for teams practicing continuous integration and continuous deployment (CI/CD), enabling faster and more reliable software delivery.

### Key Features

- **Multi-platform Support**: Automates configurations for Azure, AWS, GCP, Firebase, Supabase, and Cloudflare.
- **Versatile Development Approaches**: Supports microservices, serverless, monolithic, event-driven, and API-first architectures.
- **Comprehensive Artifact Generation**: Creates Dockerfiles, Bash scripts, Kubernetes configurations, and CI/CD pipelines.
- **User-friendly Interfaces**: Accessible via both CLI and WebUI.
- **Customizable**: Easily extendable to include new modules and configurations.
- **Environment Management**: Helps manage environment variables and secrets.

## Agentic Engineering
Agentic Engineering is a modern approach to software development that integrates artificial intelligence and automation to streamline engineering processes. This methodology enhances efficiency by automating routine tasks, optimizing resource allocation, and providing intelligent insights to support decision-making. By leveraging AI, Agentic Engineering helps development teams achieve higher productivity, better code quality, and faster time-to-market, making it an invaluable tool in today's fast-paced technology landscape.

## Installation
```
pip install agentic-devops
```
o
To install the Agentic DevOps tool, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ruvnet/agentic-devops.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd agentic-devops
   ```

3. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**
   ```bash
   pip install -e .
   ```

5. **Set up the necessary environment variables (see the "Environment Secrets" section below).**

## Environment Secrets

The Agentic DevOps tool requires certain environment variables to be set for authentication and configuration purposes. Make sure to set the following environment variables:

- `OPENAI_API_KEY` : You OpenAi Key

## Optional Keys
- `AZURE_CLIENT_ID`: Your Azure client ID.
- `AZURE_CLIENT_SECRET`: Your Azure client secret.
- `AZURE_APP_CONFIG_CON_STR`: Your Azure App Configuration connection string.
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `GCP_PROJECT_ID`: Your GCP project ID.
- `GCP_SERVICE_ACCOUNT_KEY`: Your GCP service account key.
- `FIREBASE_API_KEY`: Your Firebase API key.
- `SUPABASE_URL`: Your Supabase project URL.
- `SUPABASE_KEY`: Your Supabase project API key.
- `CLOUDFLARE_API_KEY`: Your Cloudflare API key.

You can set these environment variables either in your system environment or by creating a `.env` file in the project root directory. Here is an example of a `.env` file:

```plaintext
OPENAI_API_KEY=sk....
```

6. **Run the App:**
   ```bash
   agentic-devops
   ```

## Menu

The Agentic DevOps tool provides an interactive menu-based interface for navigating and selecting different features. Here is an outline of the CLI menu options:
  ```
        Main Menu:
        1. Start WebUI 🌐
        2. Settings ⚙️
        3. Exit ❌
  ```

### WebUI

The Agentic DevOps tool also provides a web-based user interface (WebUI) for a more intuitive and visual experience. The WebUI uses the same menu structure as the CLI, making it easy to switch between the two interfaces.

#### Start the WebUI

To start the WebUI, select "Start Agentic DevOps WebUI" from the Agentic DevOps menu.

#### Access the WebUI
[![Agentic Engineering](https://raw.githubusercontent.com/ruvnet/agentic-devops/main/assets/1.png)](https://devops.ruv.io)

Open a web browser and navigate to `http://localhost:8501`.

#### WebUI Options

- **Agentic Development**: Choose from different development approaches like microservices, serverless, monolithic, event-driven, API-first, and more.
- **Create Dockerfile**: Input base image, packages to install, and generate a Dockerfile.
- **Create Bash Script**: Define the script purpose and include necessary commands.
- **Create Kubernetes Configuration**: Provide deployment name, container image, cluster name, and namespaces.
- **Create CI/CD Pipeline**: Select a CI/CD provider and define stages for the pipeline.
- **Azure Configuration**: Configure Azure services such as hosting, networking, IAM, database, storage, DevOps, AI & ML, monitoring, and security.
- **AWS Configuration**: Configure AWS services like hosting, networking, IAM, and database.
- **GCP Configuration**: Configure GCP services including hosting, networking, IAM, and database.
- **Firebase Configuration**: Enable Firebase features for your project.
- **Supabase Configuration**: Configure Supabase services such as hosting, authentication, storage, and database.
- **Cloudflare Configuration**: Set up Cloudflare services for DNS, security, and workers.
- **Developer Configuration**: Set up development environments for languages like Python, Node.js, Java, Rust, Go, C#, Ruby, PHP, and C++.

## WebUI
![Agentic Engineering](https://github.com/ruvnet/agentic-devops/blob/main/assets/1.png?raw=true)

The Agentic DevOps tool also provides a web-based user interface (WebUI) for a more intuitive and visual experience. The WebUI uses the same menu structure as the CLI, making it easy to switch between the two interfaces.

### Start the WebUI
To start the WebUI, select "Start Agentic DevOps WebUI" from the Agentic DevOps menu.

### Access the WebUI
Open a web browser and navigate to `http://localhost:8501`.

### WebUI Options
- **Agentic Development**: Choose from different development approaches like microservices, serverless, monolithic, event-driven, API-first, and more.
- **Create Dockerfile**: Input base image, packages to install, and generate a Dockerfile.
- **Create Bash Script**: Define the script purpose and include necessary commands.
- **Create Kubernetes Configuration**: Provide deployment name, container image, cluster name, and namespaces.
- **Create CI/CD Pipeline**: Select a CI/CD provider and define stages for the pipeline.
- **Azure Configuration**: Configure Azure services such as hosting, networking, IAM, database, storage, DevOps, AI & ML, monitoring, and security.
- **AWS Configuration**: Configure AWS services like hosting, networking, IAM, and database.
- **GCP Configuration**: Configure GCP services including hosting, networking, IAM, and database.
- **Firebase Configuration**: Enable Firebase features for your project.
- **Supabase Configuration**: Configure Supabase services such as hosting, authentication, storage, and database.
- **Cloudflare Configuration**: Set up Cloudflare services for DNS, security, and workers.
- **Developer Configuration**: Set up development environments for languages like Python, Node.js, Java, Rust, Go, C#, Ruby, PHP, and C++.

## Advanced Usage

For advanced users, the Agentic DevOps tool offers additional features and customization options:

### Integration with CI/CD
Integrate the tool with external CI/CD pipelines by including it in your build scripts and using its CLI commands.

### Extending Functionality
Extend the functionality by adding new modules and commands in `coder.py` and updating `main.py` to include these new commands.

## Contributing

Contributions to the Agentic DevOps tool are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

The Agentic DevOps tool is open-source software licensed under the [MIT License](https://github.com/ruvnet/agentic-devops/blob/main/LICENSE).
