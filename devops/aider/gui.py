# gui.py is a new file that contains the GUI class, which is used to interact with the Streamlit GUI. The GUI class includes methods for displaying the main menu, creating Dockerfiles, Bash scripts, Kubernetes configurations, CI/CD pipelines, and various cloud configurations. The GUI class also includes methods for handling user input and calling the appropriate functions based on the user's choices. The GUI class interacts with the coder.py file to access the main menu and coder menu functions. 
import os
import random
import sys

import streamlit as st

from aider.coders import Coder
from aider.dump import dump  # noqa: F401
from aider.io import InputOutput
from aider.main import main as cli_main
from aider.scrape import Scraper

class CaptureIO(InputOutput):
    lines = []

    def tool_output(self, msg):
        self.lines.append(msg)

    def tool_error(self, msg):
        self.lines.append(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines

def search(text=None):
    results = []
    for root, _, files in os.walk("aider"):
        for file in files:
            path = os.path.join(root, file)
            if not text or text in path:
                results.append(path)
    return results

class State:
    keys = set()

    def init(self, key, val=None):
        if key in self.keys:
            return

        self.keys.add(key)
        setattr(self, key, val)
        return True

@st.cache_resource
def get_state():
    return State()

@st.cache_resource
def get_coder():
    coder = cli_main(return_coder=True)
    if not isinstance(coder, Coder):
        raise ValueError(coder)
    if not coder.repo:
        raise ValueError("GUI can currently only be used inside a git repo")

    io = CaptureIO(
        pretty=False,
        yes=True,
        dry_run=coder.io.dry_run,
        encoding=coder.io.encoding,
    )
    coder.commands.io = io

    return coder

class GUI:
    prompt = None
    prompt_as = "user"
    last_undo_empty = None
    recent_msgs_empty = None
    web_content_empty = None

    def announce(self):
        lines = self.coder.get_announcements()
        lines = "  \n".join(lines)
        return lines

    def show_edit_info(self, edit):
        commit_hash = edit.get("commit_hash")
        commit_message = edit.get("commit_message")
        diff = edit.get("diff")
        fnames = edit.get("fnames")
        if fnames:
            fnames = sorted(fnames)

        if not commit_hash and not fnames:
            return

        show_undo = False
        res = ""
        if commit_hash:
            prefix = "aider: "
            if commit_message.startswith(prefix):
                commit_message = commit_message[len(prefix) :]
            res += f"Commit `{commit_hash}`: {commit_message}  \n"
            if commit_hash == self.coder.last_aider_commit_hash:
                show_undo = True

        if fnames:
            fnames = [f"`{fname}`" for fname in fnames]
            fnames = ", ".join(fnames)
            res += f"Applied edits to {fnames}."

        if diff:
            with st.expander(res):
                st.code(diff, language="diff")
                if show_undo:
                    self.add_undo(commit_hash)
        else:
            with st.container(border=True):
                st.write(res)
                if show_undo:
                    self.add_undo(commit_hash)

    def add_undo(self, commit_hash):
        if self.last_undo_empty:
            self.last_undo_empty.empty()

        self.last_undo_empty = st.empty()
        undone = self.state.last_undone_commit_hash == commit_hash
        if not undone:
            with self.last_undo_empty:
                if self.button(f"Undo commit `{commit_hash}`", key=f"undo_{commit_hash}"):
                    self.do_undo(commit_hash)

    def do_sidebar(self):
        with st.sidebar:
            st.title("Agentic Devops")
            st.caption("Version 0.01.4rc")

            # Add a primary dropdown menu for features
            feature = st.selectbox(
                "Select a Feature",
                [
                    "Select a Feature",  # Default option
                    "Agentic Development",
                    "Create Dockerfile",
                    "Create Bash Script",
                    "Create Kubernetes Configuration",
                    "Create CI/CD Pipeline",
                    "Azure Configuration",
                    "AWS Configuration",
                    "GCP Configuration",
                    "Firebase Configuration",
                    "Supabase Configuration",
                    "Cloudflare Configuration",
                    "Developer Configuration"
                ]
            )

            additional_input = ""
            service = ""

            # Add secondary dropdowns and inputs based on the primary selection
            if feature == "Agentic Development":
                approach = st.selectbox(
                    "Select an Agentic Approach",
                    [
                        "Select an Approach",  # Default option
                        "Microservices Architecture",
                        "Serverless Architecture",
                        "Monolithic Architecture",
                        "Event-Driven Architecture",
                        "API-First Development",
                        "DevOps and Continuous Delivery",
                        "Agile Development",
                        "Test-Driven Development (TDD)",
                        "Behavior-Driven Development (BDD)",
                        "Domain-Driven Design (DDD)"
                    ]
                )

                if approach == "Microservices Architecture":
                    st.markdown("### Microservices Architecture")
                    st.write("Develop software as a suite of small services, each running in its own process and communicating with lightweight mechanisms.")
                    app_name = st.text_input("Application Name", "MyMicroserviceApp")
                    app_description = st.text_area("Application Description", "Description of the microservice application")
                    services = st.text_area("List of Services (comma separated)", "auth-service, user-service, payment-service")
                    technologies = st.text_input("Technologies (comma separated)", "Docker, Kubernetes, Spring Boot")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nServices: {services}\nTechnologies: {technologies}"
                elif approach == "Serverless Architecture":
                    st.markdown("### Serverless Architecture")
                    st.write("Develop software without managing the infrastructure, using cloud services to automatically handle scaling and server management.")
                    app_name = st.text_input("Application Name", "MyServerlessApp")
                    app_description = st.text_area("Application Description", "Description of the serverless application")
                    functions = st.text_area("List of Functions (comma separated)", "login, register, processPayment")
                    cloud_provider = st.selectbox("Cloud Provider", ["AWS Lambda", "Google Cloud Functions", "Azure Functions"])
                    technologies = st.text_input("Technologies (comma separated)", "Node.js, Python, Go")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nFunctions: {functions}\nCloud Provider: {cloud_provider}\nTechnologies: {technologies}"
                elif approach == "Monolithic Architecture":
                    st.markdown("### Monolithic Architecture")
                    st.write("Develop software as a single, unified application.")
                    app_name = st.text_input("Application Name", "MyMonolithicApp")
                    app_description = st.text_area("Application Description", "Description of the monolithic application")
                    modules = st.text_area("List of Modules (comma separated)", "auth, user, payment")
                    technologies = st.text_input("Technologies (comma separated)", "Java, Spring, Hibernate")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nModules: {modules}\nTechnologies: {technologies}"
                elif approach == "Event-Driven Architecture":
                    st.markdown("### Event-Driven Architecture")
                    st.write("Develop software where events trigger actions or updates, promoting decoupling and flexibility.")
                    app_name = st.text_input("Application Name", "MyEventDrivenApp")
                    app_description = st.text_area("Application Description", "Description of the event-driven application")
                    events = st.text_area("List of Events (comma separated)", "UserRegistered, OrderPlaced, PaymentProcessed")
                    technologies = st.text_input("Technologies (comma separated)", "Kafka, RabbitMQ, AWS SNS")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nEvents: {events}\nTechnologies: {technologies}"
                elif approach == "API-First Development":
                    st.markdown("### API-First Development")
                    st.write("Develop software by designing the API first, ensuring consistent and reusable interfaces.")
                    app_name = st.text_input("Application Name", "MyAPIApp")
                    app_description = st.text_area("Application Description", "Description of the API-first application")
                    api_endpoints = st.text_area("List of API Endpoints (comma separated)", "/login, /register, /payments")
                    technologies = st.text_input("Technologies (comma separated)", "OpenAPI, Swagger, REST, GraphQL")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nAPI Endpoints: {api_endpoints}\nTechnologies: {technologies}"
                elif approach == "DevOps and Continuous Delivery":
                    st.markdown("### DevOps and Continuous Delivery")
                    st.write("Implement DevOps practices and continuous delivery pipelines for faster and more reliable software delivery.")
                    app_name = st.text_input("Application Name", "MyDevOpsApp")
                    app_description = st.text_area("Application Description", "Description of the DevOps application")
                    ci_cd_tools = st.text_input("CI/CD Tools (comma separated)", "Jenkins, GitHub Actions, GitLab CI")
                    monitoring_tools = st.text_input("Monitoring Tools (comma separated)", "Prometheus, Grafana, ELK Stack")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nCI/CD Tools: {ci_cd_tools}\nMonitoring Tools: {monitoring_tools}"
                elif approach == "Agile Development":
                    st.markdown("### Agile Development")
                    st.write("Develop software using Agile methodologies for iterative development and flexibility.")
                    app_name = st.text_input("Application Name", "MyAgileApp")
                    app_description = st.text_area("Application Description", "Description of the Agile application")
                    agile_framework = st.selectbox("Agile Framework", ["Scrum", "Kanban", "XP"])
                    sprint_duration = st.text_input("Sprint Duration", "2 weeks")
                    technologies = st.text_input("Technologies (comma separated)", "JIRA, Confluence, Trello")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nAgile Framework: {agile_framework}\nSprint Duration: {sprint_duration}\nTechnologies: {technologies}"
                elif approach == "Test-Driven Development (TDD)":
                    st.markdown("### Test-Driven Development (TDD)")
                    st.write("Develop software by writing tests before implementing the functionality.")
                    app_name = st.text_input("Application Name", "MyTDDApp")
                    app_description = st.text_area("Application Description", "Description of the TDD application")
                    test_frameworks = st.text_input("Test Frameworks (comma separated)", "JUnit, pytest, Mocha")
                    technologies = st.text_input("Technologies (comma separated)", "Java, Python, JavaScript")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nTest Frameworks: {test_frameworks}\nTechnologies: {technologies}"
                elif approach == "Behavior-Driven Development (BDD)":
                    st.markdown("### Behavior-Driven Development (BDD)")
                    st.write("Develop software by writing specifications in a readable format for all stakeholders.")
                    app_name = st.text_input("Application Name", "MyBDDApp")
                    app_description = st.text_area("Application Description", "Description of the BDD application")
                    bdd_frameworks = st.text_input("BDD Frameworks (comma separated)", "Cucumber, SpecFlow, Behave")
                    technologies = st.text_input("Technologies (comma separated)", "Java, C#, Python")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nBDD Frameworks: {bdd_frameworks}\nTechnologies: {technologies}"
                elif approach == "Domain-Driven Design (DDD)":
                    st.markdown("### Domain-Driven Design (DDD)")
                    st.write("Develop software by focusing on the core domain and domain logic.")
                    app_name = st.text_input("Application Name", "MyDDDApp")
                    app_description = st.text_area("Application Description", "Description of the DDD application")
                    bounded_contexts = st.text_area("Bounded Contexts (comma separated)", "Order, Payment, Inventory")
                    technologies = st.text_input("Technologies (comma separated)", "Java, C#, .NET")
                    additional_input = f"App Name: {app_name}\nApp Description: {app_description}\nBounded Contexts: {bounded_contexts}\nTechnologies: {technologies}"

            elif feature == "Create Dockerfile":
                base_image = st.text_input("Base Image", "python:3.8-slim")
                packages = st.text_input("Packages to install (comma separated)", "numpy, pandas")
                additional_input = f"Base Image: {base_image}\nPackages: {packages}"
            elif feature == "Create Bash Script":
                script_purpose = st.text_input("Script Purpose", "Deployment script")
                commands = st.text_area("Commands to include", "echo Hello World")
                additional_input = f"Script Purpose: {script_purpose}\nCommands: {commands}"
            elif feature == "Create Kubernetes Configuration":
                deployment_name = st.text_input("Deployment Name", "my-app-deployment")
                container_image = st.text_input("Container Image", "my-app:latest")
                cluster_name = st.text_input("Cluster Name", "my-cluster")
                namespaces = st.text_input("Namespaces (comma separated)", "default, production")
                additional_input = f"Deployment Name: {deployment_name}\nContainer Image: {container_image}\nCluster Name: {cluster_name}\nNamespaces: {namespaces}"

            elif feature == "Create CI/CD Pipeline":
                provider = st.selectbox(
                    "Select a CI/CD Provider",
                    [
                        "Select a Provider",  # Default option
                        "GitHub Actions",
                        "GitLab CI",
                        "Jenkins",
                        "CircleCI",
                        "Travis CI",
                        "Azure Pipelines",
                        "AWS CodePipeline",
                        "Google Cloud Build",
                        "Bitbucket Pipelines"
                    ]
                )

                if provider == "GitHub Actions":
                    st.markdown("### GitHub Actions CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using GitHub Actions.")
                    pipeline_name = st.text_input("Pipeline Name", "GitHub Actions Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: GitHub Actions\nStages: {stages}"
                elif provider == "GitLab CI":
                    st.markdown("### GitLab CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using GitLab CI.")
                    pipeline_name = st.text_input("Pipeline Name", "GitLab CI Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: GitLab CI\nStages: {stages}"
                elif provider == "Jenkins":
                    st.markdown("### Jenkins CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using Jenkins.")
                    pipeline_name = st.text_input("Pipeline Name", "Jenkins Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: Jenkins\nStages: {stages}"
                elif provider == "CircleCI":
                    st.markdown("### CircleCI CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using CircleCI.")
                    pipeline_name = st.text_input("Pipeline Name", "CircleCI Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: CircleCI\nStages: {stages}"
                elif provider == "Travis CI":
                    st.markdown("### Travis CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using Travis CI.")
                    pipeline_name = st.text_input("Pipeline Name", "Travis CI Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: Travis CI\nStages: {stages}"
                elif provider == "Azure Pipelines":
                    st.markdown("### Azure Pipelines CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using Azure Pipelines.")
                    pipeline_name = st.text_input("Pipeline Name", "Azure Pipelines")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: Azure Pipelines\nStages: {stages}"
                elif provider == "AWS CodePipeline":
                    st.markdown("### AWS CodePipeline CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using AWS CodePipeline.")
                    pipeline_name = st.text_input("Pipeline Name", "AWS CodePipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: AWS CodePipeline\nStages: {stages}"
                elif provider == "Google Cloud Build":
                    st.markdown("### Google Cloud Build CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using Google Cloud Build.")
                    pipeline_name = st.text_input("Pipeline Name", "Google Cloud Build Pipeline")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: Google Cloud Build\nStages: {stages}"
                elif provider == "Bitbucket Pipelines":
                    st.markdown("### Bitbucket Pipelines CI/CD Pipeline")
                    st.write("Configure your CI/CD pipeline using Bitbucket Pipelines.")
                    pipeline_name = st.text_input("Pipeline Name", "Bitbucket Pipelines")
                    stages = st.text_area("Stages (comma separated)", "build, test, deploy")
                    additional_input = f"Pipeline Name: {pipeline_name}\nProvider: Bitbucket Pipelines\nStages: {stages}"

            elif feature == "Azure Configuration":
                service = st.selectbox(
                    "Select Azure Service",
                    [
                        "Select Service",  # Default option
                        "Hosting",
                        "Networking",
                        "IAM",
                        "Database",
                        "Storage",
                        "DevOps",
                        "AI & Machine Learning",
                        "Monitoring",
                        "Security"
                    ]
                )
                if service == "Hosting":
                    st.markdown("### Azure Hosting Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    app_service_name = st.text_input("App Service Name", "my-app-service")
                    region = st.text_input("Region", "East US")
                    sku = st.selectbox("Pricing Tier (SKU)", ["F1", "B1", "B2", "B3", "S1", "S2", "S3", "P1v2", "P2v2", "P3v2"])
                    os_type = st.selectbox("Operating System", ["Windows", "Linux"])
                    runtime_stack = st.selectbox("Runtime Stack", [".NET", "Node", "Python", "Java", "PHP", "Ruby"])
                    additional_input = f"Resource Group: {resource_group}\nApp Service Name: {app_service_name}\nRegion: {region}\nPricing Tier: {sku}\nOperating System: {os_type}\nRuntime Stack: {runtime_stack}"
                elif service == "Networking":
                    st.markdown("### Azure Networking Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    vnet_name = st.text_input("VNet Name", "my-vnet")
                    address_space = st.text_input("Address Space", "10.0.0.0/16")
                    subnet_name = st.text_input("Subnet Name", "my-subnet")
                    subnet_address = st.text_input("Subnet Address", "10.0.1.0/24")
                    nsg_name = st.text_input("Network Security Group (NSG) Name", "my-nsg")
                    additional_input = f"Resource Group: {resource_group}\nVNet Name: {vnet_name}\nAddress Space: {address_space}\nSubnet Name: {subnet_name}\nSubnet Address: {subnet_address}\nNSG Name: {nsg_name}"
                elif service == "IAM":
                    st.markdown("### Azure IAM Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    role_assignment_name = st.text_input("Role Assignment Name", "my-role-assignment")
                    role_definition = st.selectbox("Role Definition", ["Owner", "Contributor", "Reader", "User Access Administrator"])
                    principal_id = st.text_input("Principal ID (User/Service Principal ID)", "user-or-sp-id")
                    scope = st.text_input("Scope", "/subscriptions/{subscription-id}/resourceGroups/{resource-group}")
                    additional_input = f"Resource Group: {resource_group}\nRole Assignment Name: {role_assignment_name}\nRole Definition: {role_definition}\nPrincipal ID: {principal_id}\nScope: {scope}"
                elif service == "Database":
                    st.markdown("### Azure Database Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    db_type = st.selectbox("Database Type", ["SQL Database", "Cosmos DB", "MySQL", "PostgreSQL", "MariaDB"])
                    if db_type == "SQL Database":
                        db_name = st.text_input("Database Name", "my-sql-db")
                        server_name = st.text_input("Server Name", "my-sql-server")
                        collation = st.text_input("Collation", "SQL_Latin1_General_CP1_CI_AS")
                        additional_input = f"Resource Group: {resource_group}\nDatabase Type: SQL Database\nDatabase Name: {db_name}\nServer Name: {server_name}\nCollation: {collation}"
                    elif db_type == "Cosmos DB":
                        account_name = st.text_input("Account Name", "my-cosmos-account")
                        consistency_level = st.selectbox("Consistency Level", ["Strong", "Bounded Staleness", "Session", "Consistent Prefix", "Eventual"])
                        additional_input = f"Resource Group: {resource_group}\nDatabase Type: Cosmos DB\nAccount Name: {account_name}\nConsistency Level: {consistency_level}"
                    elif db_type == "MySQL":
                        server_name = st.text_input("Server Name", "my-mysql-server")
                        version = st.selectbox("Version", ["5.6", "5.7", "8.0"])
                        additional_input = f"Resource Group: {resource_group}\nDatabase Type: MySQL\nServer Name: {server_name}\nVersion: {version}"
                    elif db_type == "PostgreSQL":
                        server_name = st.text_input("Server Name", "my-postgresql-server")
                        version = st.selectbox("Version", ["9.6", "10", "11", "12", "13"])
                        additional_input = f"Resource Group: {resource_group}\nDatabase Type: PostgreSQL\nServer Name: {server_name}\nVersion: {version}"
                    elif db_type == "MariaDB":
                        server_name = st.text_input("Server Name", "my-mariadb-server")
                        version = st.selectbox("Version", ["10.2", "10.3", "10.4", "10.5"])
                        additional_input = f"Resource Group: {resource_group}\nDatabase Type: MariaDB\nServer Name: {server_name}\nVersion: {version}"
                elif service == "Storage":
                    st.markdown("### Azure Storage Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    storage_account_name = st.text_input("Storage Account Name", "mystorageaccount")
                    sku = st.selectbox("SKU", ["Standard_LRS", "Standard_GRS", "Standard_RAGRS", "Premium_LRS"])
                    access_tier = st.selectbox("Access Tier", ["Hot", "Cool"])
                    additional_input = f"Resource Group: {resource_group}\nStorage Account Name: {storage_account_name}\nSKU: {sku}\nAccess Tier: {access_tier}"
                elif service == "DevOps":
                    st.markdown("### Azure DevOps Configuration")
                    project_name = st.text_input("Project Name", "my-devops-project")
                    repo_name = st.text_input("Repository Name", "my-repo")
                    pipeline_name = st.text_input("Pipeline Name", "my-pipeline")
                    additional_input = f"Project Name: {project_name}\nRepository Name: {repo_name}\nPipeline Name: {pipeline_name}"
                elif service == "AI & Machine Learning":
                    st.markdown("### Azure AI & Machine Learning Configuration")
                    workspace_name = st.text_input("Workspace Name", "my-ml-workspace")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    region = st.text_input("Region", "East US")
                    additional_input = f"Workspace Name: {workspace_name}\nResource Group: {resource_group}\nRegion: {region}"
                elif service == "Monitoring":
                    st.markdown("### Azure Monitoring Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    log_analytics_workspace = st.text_input("Log Analytics Workspace", "my-log-analytics")
                    alert_rules = st.text_area("Alert Rules (comma separated)", "High CPU,Low Memory")
                    additional_input = f"Resource Group: {resource_group}\nLog Analytics Workspace: {log_analytics_workspace}\nAlert Rules: {alert_rules}"
                elif service == "Security":
                    st.markdown("### Azure Security Configuration")
                    resource_group = st.text_input("Resource Group", "my-resource-group")
                    security_center_policy = st.text_area("Security Center Policy", "Enable all security recommendations")
                    additional_input = f"Resource Group: {resource_group}\nSecurity Center Policy: {security_center_policy}"
            
            # AWS Config   
            elif feature == "AWS Configuration":
                service = st.selectbox(
                    "Select AWS Service",
                    [
                        "Select Service",  # Default option
                        "Hosting",
                        "Networking",
                        "IAM",
                        "Database",
                        "Storage",
                        "DevOps",
                        "AI & Machine Learning",
                        "Monitoring",
                        "Security"
                    ]
                )
                if service == "Hosting":
                    st.markdown("### AWS Hosting Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    ec2_instance_type = st.text_input("EC2 Instance Type", "t2.micro")
                    region = st.text_input("Region", "us-east-1")
                    additional_input = f"Stack Name: {stack_name}\nEC2 Instance Type: {ec2_instance_type}\nRegion: {region}"
                elif service == "Networking":
                    st.markdown("### AWS Networking Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    vpc_id = st.text_input("VPC ID", "vpc-123456")
                    subnet_id = st.text_input("Subnet ID", "subnet-123456")
                    security_group_id = st.text_input("Security Group ID", "sg-123456")
                    additional_input = f"Stack Name: {stack_name}\nVPC ID: {vpc_id}\nSubnet ID: {subnet_id}\nSecurity Group ID: {security_group_id}"
                elif service == "IAM":
                    st.markdown("### AWS IAM Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    role_name = st.text_input("Role Name", "my-role")
                    policy_arn = st.text_input("Policy ARN", "arn:aws:iam::aws:policy/AdministratorAccess")
                    additional_input = f"Stack Name: {stack_name}\nRole Name: {role_name}\nPolicy ARN: {policy_arn}"
                elif service == "Database":
                    st.markdown("### AWS Database Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    db_type = st.selectbox("Database Type", ["RDS", "DynamoDB", "Aurora", "Redshift", "DocumentDB"])
                    if db_type == "RDS":
                        db_instance_identifier = st.text_input("DB Instance Identifier", "my-rds-instance")
                        db_instance_class = st.text_input("DB Instance Class", "db.t2.micro")
                        db_engine = st.selectbox("DB Engine", ["MySQL", "PostgreSQL", "MariaDB", "Oracle", "SQL Server"])
                        additional_input = f"Stack Name: {stack_name}\nDatabase Type: RDS\nDB Instance Identifier: {db_instance_identifier}\nDB Instance Class: {db_instance_class}\nDB Engine: {db_engine}"
                    elif db_type == "DynamoDB":
                        table_name = st.text_input("Table Name", "my-dynamodb-table")
                        read_capacity_units = st.number_input("Read Capacity Units", 1)
                        write_capacity_units = st.number_input("Write Capacity Units", 1)
                        additional_input = f"Stack Name: {stack_name}\nDatabase Type: DynamoDB\nTable Name: {table_name}\nRead Capacity Units: {read_capacity_units}\nWrite Capacity Units: {write_capacity_units}"
                    elif db_type == "Aurora":
                        cluster_identifier = st.text_input("Cluster Identifier", "my-aurora-cluster")
                        db_instance_class = st.text_input("DB Instance Class", "db.r5.large")
                        engine_mode = st.selectbox("Engine Mode", ["provisioned", "serverless"])
                        additional_input = f"Stack Name: {stack_name}\nDatabase Type: Aurora\nCluster Identifier: {cluster_identifier}\nDB Instance Class: {db_instance_class}\nEngine Mode: {engine_mode}"
                    elif db_type == "Redshift":
                        cluster_identifier = st.text_input("Cluster Identifier", "my-redshift-cluster")
                        node_type = st.text_input("Node Type", "dc2.large")
                        number_of_nodes = st.number_input("Number of Nodes", 1)
                        additional_input = f"Stack Name: {stack_name}\nDatabase Type: Redshift\nCluster Identifier: {cluster_identifier}\nNode Type: {node_type}\nNumber of Nodes: {number_of_nodes}"
                    elif db_type == "DocumentDB":
                        cluster_identifier = st.text_input("Cluster Identifier", "my-docdb-cluster")
                        db_instance_class = st.text_input("DB Instance Class", "db.r5.large")
                        additional_input = f"Stack Name: {stack_name}\nDatabase Type: DocumentDB\nCluster Identifier: {cluster_identifier}\nDB Instance Class: {db_instance_class}"
                elif service == "Storage":
                    st.markdown("### AWS Storage Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    bucket_name = st.text_input("Bucket Name", "my-bucket")
                    storage_class = st.selectbox("Storage Class", ["STANDARD", "INTELLIGENT_TIERING", "STANDARD_IA", "ONEZONE_IA", "GLACIER", "DEEP_ARCHIVE"])
                    additional_input = f"Stack Name: {stack_name}\nBucket Name: {bucket_name}\nStorage Class: {storage_class}"
                elif service == "DevOps":
                    st.markdown("### AWS DevOps Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    pipeline_name = st.text_input("Pipeline Name", "my-pipeline")
                    repository_name = st.text_input("Repository Name", "my-repo")
                    additional_input = f"Stack Name: {stack_name}\nPipeline Name: {pipeline_name}\nRepository Name: {repository_name}"
                elif service == "AI & Machine Learning":
                    st.markdown("### AWS AI & Machine Learning Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    sagemaker_notebook_instance_name = st.text_input("SageMaker Notebook Instance Name", "my-notebook")
                    instance_type = st.text_input("Instance Type", "ml.t2.medium")
                    additional_input = f"Stack Name: {stack_name}\nSageMaker Notebook Instance Name: {sagemaker_notebook_instance_name}\nInstance Type: {instance_type}"
                elif service == "Monitoring":
                    st.markdown("### AWS Monitoring Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    cloudwatch_alarm_name = st.text_input("CloudWatch Alarm Name", "my-alarm")
                    metric_name = st.text_input("Metric Name", "CPUUtilization")
                    threshold = st.number_input("Threshold", 80)
                    additional_input = f"Stack Name: {stack_name}\nCloudWatch Alarm Name: {cloudwatch_alarm_name}\nMetric Name: {metric_name}\nThreshold: {threshold}"
                elif service == "Security":
                    st.markdown("### AWS Security Configuration")
                    stack_name = st.text_input("Stack Name", "my-stack")
                    kms_key_id = st.text_input("KMS Key ID", "my-kms-key")
                    security_policy_name = st.text_input("Security Policy Name", "my-security-policy")
                    additional_input = f"Stack Name: {stack_name}\nKMS Key ID: {kms_key_id}\nSecurity Policy Name: {security_policy_name}"

                # Add more services as needed

            # Add GCP Configuration options           
            elif feature == "GCP Configuration":
                service = st.selectbox(
                    "Select GCP Service",
                    [
                        "Select Service",  # Default option
                        "Hosting",
                        "Networking",
                        "IAM",
                        "Database",
                        "Storage",
                        "DevOps",
                        "AI & Machine Learning",
                        "Monitoring",
                        "Security"
                    ]
                )
                if service == "Hosting":
                    st.markdown("### GCP Hosting Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    instance_name = st.text_input("Instance Name", "my-instance")
                    zone = st.text_input("Zone", "us-central1-a")
                    machine_type = st.text_input("Machine Type", "n1-standard-1")
                    additional_input = f"Project ID: {project_id}\nInstance Name: {instance_name}\nZone: {zone}\nMachine Type: {machine_type}"
                elif service == "Networking":
                    st.markdown("### GCP Networking Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    vpc_name = st.text_input("VPC Name", "my-vpc")
                    subnet_name = st.text_input("Subnet Name", "my-subnet")
                    region = st.text_input("Region", "us-central1")
                    additional_input = f"Project ID: {project_id}\nVPC Name: {vpc_name}\nSubnet Name: {subnet_name}\nRegion: {region}"
                elif service == "IAM":
                    st.markdown("### GCP IAM Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    role_assignment_name = st.text_input("Role Assignment Name", "my-role-assignment")
                    role_definition = st.selectbox("Role Definition", ["Owner", "Editor", "Viewer", "Custom Role"])
                    principal_id = st.text_input("Principal ID (User/Service Account ID)", "user-or-service-account-id")
                    additional_input = f"Project ID: {project_id}\nRole Assignment Name: {role_assignment_name}\nRole Definition: {role_definition}\nPrincipal ID: {principal_id}"
                elif service == "Database":
                    st.markdown("### GCP Database Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    db_type = st.selectbox("Database Type", ["Cloud SQL", "Firestore", "Bigtable", "Spanner"])
                    if db_type == "Cloud SQL":
                        instance_id = st.text_input("Instance ID", "my-cloud-sql-instance")
                        db_version = st.selectbox("Database Version", ["MySQL 5.7", "MySQL 8.0", "PostgreSQL 11", "PostgreSQL 12"])
                        additional_input = f"Project ID: {project_id}\nDatabase Type: Cloud SQL\nInstance ID: {instance_id}\nDatabase Version: {db_version}"
                    elif db_type == "Firestore":
                        mode = st.selectbox("Mode", ["Native Mode", "Datastore Mode"])
                        additional_input = f"Project ID: {project_id}\nDatabase Type: Firestore\nMode: {mode}"
                    elif db_type == "Bigtable":
                        instance_id = st.text_input("Instance ID", "my-bigtable-instance")
                        cluster_id = st.text_input("Cluster ID", "my-cluster")
                        additional_input = f"Project ID: {project_id}\nDatabase Type: Bigtable\nInstance ID: {instance_id}\nCluster ID: {cluster_id}"
                    elif db_type == "Spanner":
                        instance_id = st.text_input("Instance ID", "my-spanner-instance")
                        config = st.text_input("Instance Config", "regional-us-central1")
                        additional_input = f"Project ID: {project_id}\nDatabase Type: Spanner\nInstance ID: {instance_id}\nInstance Config: {config}"
                elif service == "Storage":
                    st.markdown("### GCP Storage Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    bucket_name = st.text_input("Bucket Name", "my-storage-bucket")
                    location = st.text_input("Location", "US")
                    storage_class = st.selectbox("Storage Class", ["Standard", "Nearline", "Coldline", "Archive"])
                    additional_input = f"Project ID: {project_id}\nBucket Name: {bucket_name}\nLocation: {location}\nStorage Class: {storage_class}"
                elif service == "DevOps":
                    st.markdown("### GCP DevOps Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    repo_name = st.text_input("Repository Name", "my-repo")
                    pipeline_name = st.text_input("Pipeline Name", "my-pipeline")
                    additional_input = f"Project ID: {project_id}\nRepository Name: {repo_name}\nPipeline Name: {pipeline_name}"
                elif service == "AI & Machine Learning":
                    st.markdown("### GCP AI & Machine Learning Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    region = st.text_input("Region", "us-central1")
                    ml_engine = st.text_input("ML Engine", "AI Platform")
                    additional_input = f"Project ID: {project_id}\nRegion: {region}\nML Engine: {ml_engine}"
                elif service == "Monitoring":
                    st.markdown("### GCP Monitoring Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    workspace_name = st.text_input("Workspace Name", "my-monitoring-workspace")
                    alert_policies = st.text_area("Alert Policies (comma separated)", "High CPU,Low Memory")
                    additional_input = f"Project ID: {project_id}\nWorkspace Name: {workspace_name}\nAlert Policies: {alert_policies}"
                elif service == "Security":
                    st.markdown("### GCP Security Configuration")
                    project_id = st.text_input("Project ID", "my-gcp-project")
                    security_policies = st.text_area("Security Policies", "Enable all security recommendations")
                    additional_input = f"Project ID: {project_id}\nSecurity Policies: {security_policies}"

            elif feature == "Firebase Configuration":
                project_name = st.text_input("Project Name", "my-firebase-project")
                features = st.text_area("Features to enable", "Authentication, Firestore")
                additional_input = f"Project Name: {project_name}\nFeatures: {features}"
            elif feature == "Supabase Configuration":
                service = st.selectbox("Select Supabase Service", ["Select Service", "Hosting", "Authentication", "Storage", "Database"])
                if service == "Hosting":
                    project_name = st.text_input("Project Name", "my-supabase-project")
                    region = st.text_input("Region", "us-west-1")
                    additional_input = f"Project Name: {project_name}\nRegion: {region}"
                elif service == "Authentication":
                    project_name = st.text_input("Project Name", "my-supabase-project")
                    auth_providers = st.text_input("Authentication Providers", "Email, Google")
                    additional_input = f"Project Name: {project_name}\nAuthentication Providers: {auth_providers}"
                # Add more services as needed
            elif feature == "Cloudflare Configuration":
                service = st.selectbox("Select Cloudflare Service", ["Select Service", "DNS", "Security", "Workers"])
                if service == "DNS":
                    project_name = st.text_input("Project Name", "my-cloudflare-project")
                    dns_records = st.text_area("DNS Records", "A, CNAME, TXT")
                    additional_input = f"Project Name: {project_name}\nDNS Records: {dns_records}"
                elif service == "Security":
                    project_name = st.text_input("Project Name", "my-cloudflare-project")
                    security_features = st.text_area("Security Features", "WAF, DDoS Protection")
                    additional_input = f"Project Name: {project_name}\nSecurity Features: {security_features}"

            elif feature == "Developer Configuration":
                language = st.selectbox(
                    "Select a Language",
                    [
                        "Select a Language",  # Default option
                        "Python",
                        "Node.js",
                        "Java",
                        "Rust",
                        "Go",
                        "C#",
                        "Ruby",
                        "PHP",
                        "C++"
                    ]
                )

                if language == "Python":
                    st.markdown("### Python Development Environment")
                    st.write("Configure your Python development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Python Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "ms-python.python, ms-toolsai.jupyter")
                    settings = st.text_area("VS Code Settings", "{\n    \"python.pythonPath\": \"/usr/bin/python3\",\n    \"python.linting.enabled\": true\n}")
                    additional_input = f"Language: Python\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "Node.js":
                    st.markdown("### Node.js Development Environment")
                    st.write("Configure your Node.js development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Node.js Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "dbaeumer.vscode-eslint, esbenp.prettier-vscode")
                    settings = st.text_area("VS Code Settings", "{\n    \"javascript.format.enable\": true,\n    \"eslint.enable\": true\n}")
                    additional_input = f"Language: Node.js\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "Java":
                    st.markdown("### Java Development Environment")
                    st.write("Configure your Java development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Java Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "vscjava.vscode-java-pack")
                    settings = st.text_area("VS Code Settings", "{\n    \"java.home\": \"/usr/lib/jvm/java-11-openjdk-amd64\",\n    \"java.errors.incompleteClasspath.severity\": \"warning\"\n}")
                    additional_input = f"Language: Java\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "Rust":
                    st.markdown("### Rust Development Environment")
                    st.write("Configure your Rust development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Rust Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "rust-lang.rust, matklad.rust-analyzer")
                    settings = st.text_area("VS Code Settings", "{\n    \"rust-client.channel\": \"stable\",\n    \"rust-analyzer.cargo.allFeatures\": true\n}")
                    additional_input = f"Language: Rust\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "Go":
                    st.markdown("### Go Development Environment")
                    st.write("Configure your Go development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Go Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "golang.go")
                    settings = st.text_area("VS Code Settings", "{\n    \"go.useLanguageServer\": true,\n    \"go.lintOnSave\": \"package\"\n}")
                    additional_input = f"Language: Go\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "C#":
                    st.markdown("### C# Development Environment")
                    st.write("Configure your C# development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "C# Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "ms-dotnettools.csharp")
                    settings = st.text_area("VS Code Settings", "{\n    \"csharp.suppressDotnetRestoreNotification\": true\n}")
                    additional_input = f"Language: C#\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "Ruby":
                    st.markdown("### Ruby Development Environment")
                    st.write("Configure your Ruby development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "Ruby Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "rebornix.ruby")
                    settings = st.text_area("VS Code Settings", "{\n    \"ruby.useLanguageServer\": true,\n    \"ruby.lint\": {\n        \"rubocop\": true\n    }\n}")
                    additional_input = f"Language: Ruby\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "PHP":
                    st.markdown("### PHP Development Environment")
                    st.write("Configure your PHP development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "PHP Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "felixfbecker.php-intellisense, bmewburn.vscode-intelephense-client")
                    settings = st.text_area("VS Code Settings", "{\n    \"php.executablePath\": \"/usr/bin/php\",\n    \"php.validate.executablePath\": \"/usr/bin/php\"\n}")
                    additional_input = f"Language: PHP\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

                elif language == "C++":
                    st.markdown("### C++ Development Environment")
                    st.write("Configure your C++ development environment with VS Code settings.")
                    config_name = st.text_input("Configuration Name", "C++ Dev Environment")
                    extensions = st.text_area("VS Code Extensions", "ms-vscode.cpptools")
                    settings = st.text_area("VS Code Settings", "{\n    \"C_Cpp.updateChannel\": \"Insiders\",\n    \"C_Cpp.intelliSenseEngine\": \"Default\"\n}")
                    additional_input = f"Language: C++\nConfiguration Name: {config_name}\nVS Code Extensions: {extensions}\nVS Code Settings: {settings}"

            if st.button("Start") and feature != "Select a Feature":
                self.start_feature(feature, additional_input, service)

            self.do_add_to_chat()
            self.do_recent_msgs()
            self.do_clear_chat_history()

            st.warning(
                "This browser version of Agentic Devops is experimental. Please share feedback in [GitHub"
                " issues](https://github.com/ruvnet/agentic-devops/issues)."
            )

    def start_feature(self, feature, additional_input, service):
        internal_guidance = ""

        if feature == "Agentic Development":
            internal_guidance = "Guide the development over several steps, including planning, design, implementation, and testing. Ensure to create complete and well-documented applications."
            self.prompt = f"Agentic Development:\n{additional_input}\n{internal_guidance}"
        elif feature == "Create Dockerfile":
            internal_guidance = "Ensure to include best practices for Dockerfile creation, such as minimizing layers, using a small base image, and cleaning up unnecessary files."
            self.prompt = f"Create a Dockerfile with options: {additional_input}. {internal_guidance}"
        elif feature == "Create Bash Script":
            internal_guidance = "The script should handle errors gracefully, use descriptive comments, and include execution permissions."
            self.prompt = f"Create a basic deployment script with details: {additional_input}. {internal_guidance}"
        elif feature == "Create Kubernetes Configuration":
            internal_guidance = "Ensure the configuration includes resource limits, readiness and liveness probes, and follows Kubernetes best practices."
            self.prompt = f"Create a Kubernetes config for a web application with details: {additional_input}. {internal_guidance}"
        elif feature == "Create CI/CD Pipeline":
            internal_guidance = "The pipeline should include stages for building, testing, and deploying the application, and should support rollback mechanisms."
            self.prompt = f"Create a CI/CD pipeline for a Python project with details: {additional_input}. {internal_guidance}"
        elif feature == "Azure Configuration":
            internal_guidance = "Include detailed resource definitions, dependencies, and parameterized templates for flexibility."
            self.prompt = f"Create an Azure Resource Manager template for {service} with details: {additional_input}. {internal_guidance}"

        elif feature == "Azure Configuration":
            service = st.selectbox(
                "Select Azure Service",
                [
                    "Select Service",  # Default option
                    "Hosting",
                    "Networking",
                    "IAM",
                    "Database",
                    "Storage",
                    "DevOps",
                    "AI & Machine Learning",
                    "Monitoring",
                    "Security"
                ]
            )
            if service == "Hosting":
                st.markdown("### Azure Hosting Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                app_service_name = st.text_input("App Service Name", "my-app-service")
                region = st.text_input("Region", "East US")
                sku = st.selectbox("Pricing Tier (SKU)", ["F1", "B1", "B2", "B3", "S1", "S2", "S3", "P1v2", "P2v2", "P3v2"])
                os_type = st.selectbox("Operating System", ["Windows", "Linux"])
                runtime_stack = st.selectbox("Runtime Stack", [".NET", "Node", "Python", "Java", "PHP", "Ruby"])
                additional_input = f"Resource Group: {resource_group}\nApp Service Name: {app_service_name}\nRegion: {region}\nPricing Tier: {sku}\nOperating System: {os_type}\nRuntime Stack: {runtime_stack}"
            elif service == "Networking":
                st.markdown("### Azure Networking Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                vnet_name = st.text_input("VNet Name", "my-vnet")
                address_space = st.text_input("Address Space", "10.0.0.0/16")
                subnet_name = st.text_input("Subnet Name", "my-subnet")
                subnet_address = st.text_input("Subnet Address", "10.0.1.0/24")
                nsg_name = st.text_input("Network Security Group (NSG) Name", "my-nsg")
                additional_input = f"Resource Group: {resource_group}\nVNet Name: {vnet_name}\nAddress Space: {address_space}\nSubnet Name: {subnet_name}\nSubnet Address: {subnet_address}\nNSG Name: {nsg_name}"
            elif service == "IAM":
                st.markdown("### Azure IAM Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                role_assignment_name = st.text_input("Role Assignment Name", "my-role-assignment")
                role_definition = st.selectbox("Role Definition", ["Owner", "Contributor", "Reader", "User Access Administrator"])
                principal_id = st.text_input("Principal ID (User/Service Principal ID)", "user-or-sp-id")
                scope = st.text_input("Scope", "/subscriptions/{subscription-id}/resourceGroups/{resource-group}")
                additional_input = f"Resource Group: {resource_group}\nRole Assignment Name: {role_assignment_name}\nRole Definition: {role_definition}\nPrincipal ID: {principal_id}\nScope: {scope}"
            elif service == "Database":
                st.markdown("### Azure Database Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                db_type = st.selectbox("Database Type", ["SQL Database", "Cosmos DB", "MySQL", "PostgreSQL", "MariaDB"])
                if db_type == "SQL Database":
                    db_name = st.text_input("Database Name", "my-sql-db")
                    server_name = st.text_input("Server Name", "my-sql-server")
                    collation = st.text_input("Collation", "SQL_Latin1_General_CP1_CI_AS")
                    additional_input = f"Resource Group: {resource_group}\nDatabase Type: SQL Database\nDatabase Name: {db_name}\nServer Name: {server_name}\nCollation: {collation}"
                elif db_type == "Cosmos DB":
                    account_name = st.text_input("Account Name", "my-cosmos-account")
                    consistency_level = st.selectbox("Consistency Level", ["Strong", "Bounded Staleness", "Session", "Consistent Prefix", "Eventual"])
                    additional_input = f"Resource Group: {resource_group}\nDatabase Type: Cosmos DB\nAccount Name: {account_name}\nConsistency Level: {consistency_level}"
                elif db_type == "MySQL":
                    server_name = st.text_input("Server Name", "my-mysql-server")
                    version = st.selectbox("Version", ["5.6", "5.7", "8.0"])
                    additional_input = f"Resource Group: {resource_group}\nDatabase Type: MySQL\nServer Name: {server_name}\nVersion: {version}"
                elif db_type == "PostgreSQL":
                    server_name = st.text_input("Server Name", "my-postgresql-server")
                    version = st.selectbox("Version", ["9.6", "10", "11", "12", "13"])
                    additional_input = f"Resource Group: {resource_group}\nDatabase Type: PostgreSQL\nServer Name: {server_name}\nVersion: {version}"
                elif db_type == "MariaDB":
                    server_name = st.text_input("Server Name", "my-mariadb-server")
                    version = st.selectbox("Version", ["10.2", "10.3", "10.4", "10.5"])
                    additional_input = f"Resource Group: {resource_group}\nDatabase Type: MariaDB\nServer Name: {server_name}\nVersion: {version}"
            elif service == "Storage":
                st.markdown("### Azure Storage Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                storage_account_name = st.text_input("Storage Account Name", "mystorageaccount")
                sku = st.selectbox("SKU", ["Standard_LRS", "Standard_GRS", "Standard_RAGRS", "Premium_LRS"])
                access_tier = st.selectbox("Access Tier", ["Hot", "Cool"])
                additional_input = f"Resource Group: {resource_group}\nStorage Account Name: {storage_account_name}\nSKU: {sku}\nAccess Tier: {access_tier}"
            elif service == "DevOps":
                st.markdown("### Azure DevOps Configuration")
                project_name = st.text_input("Project Name", "my-devops-project")
                repo_name = st.text_input("Repository Name", "my-repo")
                pipeline_name = st.text_input("Pipeline Name", "my-pipeline")
                additional_input = f"Project Name: {project_name}\nRepository Name: {repo_name}\nPipeline Name: {pipeline_name}"
            elif service == "AI & Machine Learning":
                st.markdown("### Azure AI & Machine Learning Configuration")
                workspace_name = st.text_input("Workspace Name", "my-ml-workspace")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                region = st.text_input("Region", "East US")
                additional_input = f"Workspace Name: {workspace_name}\nResource Group: {resource_group}\nRegion: {region}"
            elif service == "Monitoring":
                st.markdown("### Azure Monitoring Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                log_analytics_workspace = st.text_input("Log Analytics Workspace", "my-log-analytics")
                alert_rules = st.text_area("Alert Rules (comma separated)", "High CPU,Low Memory")
                additional_input = f"Resource Group: {resource_group}\nLog Analytics Workspace: {log_analytics_workspace}\nAlert Rules: {alert_rules}"
            elif service == "Security":
                st.markdown("### Azure Security Configuration")
                resource_group = st.text_input("Resource Group", "my-resource-group")
                security_center_policy = st.text_area("Security Center Policy", "Enable all security recommendations")
                additional_input = f"Resource Group: {resource_group}\nSecurity Center Policy: {security_center_policy}"

            if st.button("Start") and service != "Select Service":
                self.start_feature(feature, additional_input)


        elif feature == "AWS Configuration":
            internal_guidance = "Ensure the template includes IAM roles and policies, and follows AWS best practices for security and scalability."
            self.prompt = f"Create a CloudFormation template for {service} with details: {additional_input}. {internal_guidance}"
        elif feature == "GCP Configuration":
            internal_guidance = "Include configurations for IAM, networking, and resource management according to Google Cloud best practices."
            self.prompt = f"Create a Google Cloud Deployment Manager template for {service} with details: {additional_input}. {internal_guidance}"

        elif feature == "Firebase Configuration":
            internal_guidance = "Ensure the configuration includes authentication, database rules, and hosting settings."
            self.prompt = f"Create a Firebase configuration with details: {additional_input}. {internal_guidance}"
        elif feature == "Supabase Configuration":
            internal_guidance = "Ensure the configuration includes database settings, authentication, and storage settings."
            self.prompt = f"Create a Supabase configuration for {service} with details: {additional_input}. {internal_guidance}"
        elif feature == "Cloudflare Configuration":
            internal_guidance = "Ensure the configuration includes DNS settings, security settings, and workers settings."
            self.prompt = f"Create a Cloudflare configuration for {service} with details: {additional_input}. {internal_guidance}"
        elif feature == "Developer Configuration":
            internal_guidance = "Include common development tools and configurations, ensuring they follow best practices for development environments."
            self.prompt = f"Create a .nix configuration with details: {additional_input}. {internal_guidance}"

        if self.prompt:
            # Save the output to the ./output folder
            output_dir = "./output/"
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f"{feature.lower().replace(' ', '_')}.txt"), "w") as f:
                f.write(self.prompt)

            self.state.prompt = self.prompt
            self.process_chat()


    def do_settings_tab(self):
        pass

    def do_recommended_actions(self):
        with st.expander("Recommended actions", expanded=True):
            with st.popover("Create a git repo to track changes"):
                st.write(
                    "Aider works best when your code is stored in a git repo.  \n[See the FAQ"
                    " for more info](https://aider.chat/docs/faq.html#how-does-aider-use-git)"
                )
                self.button("Create git repo", key=random.random(), help="?")

            with st.popover("Update your `.gitignore` file"):
                st.write("It's best to keep aider's internal files out of your git repo.")
                self.button("Add `.aider*` to `.gitignore`", key=random.random(), help="?")

    def do_add_to_chat(self):
        self.do_add_files()
        self.do_add_web_page()

    def do_add_files(self):
        fnames = st.multiselect(
            "Add files to the chat",
            self.coder.get_all_relative_files(),
            default=self.state.initial_inchat_files,
            placeholder="Files to edit",
            disabled=self.prompt_pending(),
            help=(
                "Only add the files that need to be *edited* for the task you are working"
                " on. Aider will pull in other relevant code to provide context to the LLM."
            ),
        )

        for fname in fnames:
            if fname not in self.coder.get_inchat_relative_files():
                self.coder.add_rel_fname(fname)
                self.info(f"Added {fname} to the chat")

        for fname in self.coder.get_inchat_relative_files():
            if fname not in fnames:
                self.coder.drop_rel_fname(fname)
                self.info(f"Removed {fname} from the chat")

    def do_add_web_page(self):
        with st.popover("Add a web page to the chat"):
            self.do_web()

    def do_add_image(self):
        with st.popover("Add image"):
            st.markdown("Hello World 👋")
            st.file_uploader("Image file", disabled=self.prompt_pending())

    def do_run_shell(self):
        with st.popover("Run shell commands, tests, etc"):
            st.markdown(
                "Run a shell command and optionally share the output with the LLM. This is"
                " a great way to run your program or run tests and have the LLM fix bugs."
            )
            st.text_input("Command:")
            st.radio(
                "Share the command output with the LLM?",
                [
                    "Review the output and decide whether to share",
                    "Automatically share the output on non-zero exit code (ie, if any tests fail)",
                ],
            )
            st.selectbox(
                "Recent commands",
                [
                    "my_app.py --doit",
                    "my_app.py --cleanup",
                ],
                disabled=self.prompt_pending(),
            )

    def do_tokens_and_cost(self):
        with st.expander("Tokens and costs", expanded=True):
            pass

    def do_show_token_usage(self):
        with st.popover("Show token usage"):
            st.write("hi")

    def do_clear_chat_history(self):
        text = "Saves tokens, reduces confusion"
        if self.button("Clear chat history", help=text):
            self.coder.done_messages = []
            self.coder.cur_messages = []
            self.info("Cleared chat history. Now the LLM can't see anything before this line.")

    def do_show_metrics(self):
        st.metric("Cost of last message send & reply", "$0.0019", help="foo")
        st.metric("Cost to send next message", "$0.0013", help="foo")
        st.metric("Total cost this session", "$0.22")

    def do_git(self):
        with st.expander("Git", expanded=False):
            self.button("Commit any pending changes")
            with st.popover("Run git command"):
                st.markdown("## Run git command")
                st.text_input("git", value="git ")
                self.button("Run")
                st.selectbox(
                    "Recent git commands",
                    [
                        "git checkout -b experiment",
                        "git stash",
                    ],
                    disabled=self.prompt_pending(),
                )

    def do_recent_msgs(self):
        if not self.recent_msgs_empty:
            self.recent_msgs_empty = st.empty()

        if self.prompt_pending():
            self.recent_msgs_empty.empty()
            self.state.recent_msgs_num += 1

        with self.recent_msgs_empty:
            self.old_prompt = st.selectbox(
                "Resend a recent chat message",
                self.state.input_history,
                placeholder="Choose a recent chat message",
                index=None,
                key=f"recent_msgs_{self.state.recent_msgs_num}",
                disabled=self.prompt_pending(),
            )
            if self.old_prompt:
                self.prompt = self.old_prompt

    def do_messages_container(self):
        self.messages = st.container()

        with self.messages:
            for msg in self.state.messages:
                role = msg["role"]

                if role == "edit":
                    self.show_edit_info(msg)
                elif role == "info":
                    st.info(msg["content"])
                elif role == "text":
                    text = msg["content"]
                    line = text.splitlines()[0]
                    with self.messages.expander(line):
                        st.text(text)
                elif role in ("user", "assistant"):
                    with st.chat_message(role):
                        st.write(msg["content"])
                else:
                    st.dict(msg)

    def initialize_state(self):
        messages = [
            dict(role="info", content=self.announce()),
            dict(role="assistant", content="How can I help you?"),
        ]

        self.state.init("messages", messages)
        self.state.init("last_aider_commit_hash", self.coder.last_aider_commit_hash)
        self.state.init("last_undone_commit_hash")
        self.state.init("recent_msgs_num", 0)
        self.state.init("web_content_num", 0)
        self.state.init("prompt")
        self.state.init("scraper")

        self.state.init("initial_inchat_files", self.coder.get_inchat_relative_files())

        if "input_history" not in self.state.keys:
            input_history = list(self.coder.io.get_input_history())
            seen = set()
            input_history = [x for x in input_history if not (x in seen or seen.add(x))]
            self.state.input_history = input_history
            self.state.keys.add("input_history")

    def button(self, args, **kwargs):
        "Create a button, disabled if prompt pending"
        if self.prompt_pending():
            kwargs["disabled"] = True
        return st.button(args, **kwargs)

    def __init__(self):
        self.coder = get_coder()
        self.state = get_state()

        self.coder.yield_stream = True
        self.coder.stream = True
        self.coder.pretty = False

        self.initialize_state()

        self.do_messages_container()
        self.do_sidebar()

        user_inp = st.chat_input("Say something")
        if user_inp:
            self.prompt = user_inp

        if self.prompt_pending():
            self.process_chat()

        if not self.prompt:
            return

        self.state.prompt = self.prompt

        if self.prompt_as == "user":
            self.coder.io.add_to_input_history(self.prompt)

        self.state.input_history.append(self.prompt)

        if self.prompt_as:
            self.state.messages.append({"role": self.prompt_as, "content": self.prompt})
        if self.prompt_as == "user":
            with self.messages.chat_message("user"):
                st.write(self.prompt)
        elif self.prompt_as == "text":
            line = self.prompt.splitlines()[0]
            line += "??"
            with self.messages.expander(line):
                st.text(self.prompt)

        st.rerun()

    def prompt_pending(self):
        return self.state.prompt is not None

    def cost(self):
        cost = random.random() * 0.003 + 0.001
        st.caption(f"${cost:0.4f}")

    def process_chat(self):
        prompt = self.state.prompt
        self.state.prompt = None

        while prompt:
            with self.messages.chat_message("assistant"):
                res = st.write_stream(self.coder.run_stream(prompt))
                self.state.messages.append({"role": "assistant", "content": res})
            if self.coder.reflected_message:
                self.info(self.coder.reflected_message)
            prompt = self.coder.reflected_message

        with self.messages:
            edit = dict(
                role="edit",
                fnames=self.coder.aider_edited_files,
            )
            if self.state.last_aider_commit_hash != self.coder.last_aider_commit_hash:
                edit["commit_hash"] = self.coder.last_aider_commit_hash
                edit["commit_message"] = self.coder.last_aider_commit_message
                commits = f"{self.coder.last_aider_commit_hash}~1"
                diff = self.coder.repo.diff_commits(
                    self.coder.pretty,
                    commits,
                    self.coder.last_aider_commit_hash,
                )
                edit["diff"] = diff
                self.state.last_aider_commit_hash = self.coder.last_aider_commit_hash

            self.state.messages.append(edit)
            self.show_edit_info(edit)

        st.rerun()

    def info(self, message, echo=True):
        info = dict(role="info", content=message)
        self.state.messages.append(info)
        if echo:
            self.messages.info(message)

    def do_web(self):
        st.markdown("Add the text content of a web page to the chat")

        if not self.web_content_empty:
            self.web_content_empty = st.empty()

        if self.prompt_pending():
            self.web_content_empty.empty()
            self.state.web_content_num += 1

        with self.web_content_empty:
            self.web_content = st.text_input(
                "URL",
                placeholder="https://...",
                key=f"web_content_{self.state.web_content_num}",
            )

        if not self.web_content:
            return

        url = self.web_content

        if not self.state.scraper:
            self.scraper = Scraper(print_error=self.info)

        instructions = self.scraper.get_playwright_instructions()
        if instructions:
            self.info(instructions)

        content = self.scraper.scrape(url) or ""
        if content.strip():
            content = f"{url}\n\n" + content
            self.prompt = content
            self.prompt_as = "text"
        else:
            self.info(f"No web content found for `{url}`.")
            self.web_content = None

    def do_undo(self, commit_hash):
        self.last_undo_empty.empty()

        if (
            self.state.last_aider_commit_hash != commit_hash
            or self.coder.last_aider_commit_hash != commit_hash
        ):
            self.info(f"Commit `{commit_hash}` is not the latest commit.")
            return

        self.coder.commands.io.get_captured_lines()
        reply = self.coder.commands.cmd_undo(None)
        lines = self.coder.commands.io.get_captured_lines()

        lines = "\n".join(lines)
        lines = lines.splitlines()
        lines = "  \n".join(lines)
        self.info(lines, echo=False)

        self.state.last_undone_commit_hash = commit_hash

        if reply:
            self.prompt_as = None
            self.prompt = reply

def gui_main():
    st.set_page_config(
        layout="wide",
        page_title="Agentic Devops",
        page_icon="https://aider.chat/assets/favicon-32x32.png",
        menu_items={
            "Get Help": "https://aider.chat/docs/faq.html",
            "Report a bug": "https://github.com/paul-gauthier/aider/issues",
            "About": "# Aider\nAI pair programming in your browser.",
        },
    )

    GUI()

if __name__ == "__main__":
    status = gui_main()
    sys.exit(status)
