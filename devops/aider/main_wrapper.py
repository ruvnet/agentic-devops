import click
import subprocess
import os
import yaml

def sanitize_config(config):
    sanitized = {}
    for k, v in config.items():
        if isinstance(v, dict):
            sanitized_sub = sanitize_config(v)
            if sanitized_sub:  # Only add non-empty dictionaries
                sanitized[k] = sanitized_sub
        elif v:  # Only add non-empty values
            sanitized[k] = v
    return sanitized

def save_config(config, file_path):
    sanitized_config = sanitize_config(config)
    with open(file_path, 'w') as file:
        yaml.dump(sanitized_config, file)

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def remove_config_file():
    config_file_path = "config.yml"
    if os.path.exists(config_file_path):
        os.remove(config_file_path)
        click.echo(f"Removed configuration file: {config_file_path}")
    else:
        click.echo(f"Configuration file not found: {config_file_path}")

def start_webui(config):
    args = ["agentic-devops-cli", "--gui"]
    for key, value in config.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                args.append(f"--{sub_key.replace('_', '-')}={sub_value}")
        else:
            args.append(f"--{key.replace('_', '-')}={value}")

    click.echo("Starting WebUI...")
    subprocess.run(args)

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

def start_webui():
    click.echo("🚀 Starting WebUI...")
    args = ["agentic-devops-cli", "--gui"]
    subprocess.run(args)


def show_settings():
    config = load_config()
    while True:
        click.echo(r"""
        Settings Menu:
        1. General Settings
        2. Model Settings
        3. History Settings
        4. Output Settings
        5. Git Settings
        6. Other Settings
        7. Back to Main Menu
        """)
        choice = click.prompt("Please choose a setting to configure", type=int)
        if choice == 1:
            configure_general_settings(config)
        elif choice == 2:
            configure_model_settings(config)
        elif choice == 3:
            configure_history_settings(config)
        elif choice == 4:
            configure_output_settings(config)
        elif choice == 5:
            configure_git_settings(config)
        elif choice == 6:
            configure_other_settings(config)
        elif choice == 7:
            save_config(config)
            break
        else:
            click.echo("Invalid choice. Please try again.")

def configure_general_settings(config):
    click.echo("\nMain Settings")
    while True:
        click.echo("""
        Main Settings:
        1. File
        2. OpenAI API Key
        3. Anthropic API Key
        4. Model
        5. Opus Model
        6. Sonnet Model
        7. GPT-4 Model
        8. GPT-4o Model
        9. GPT-4 Turbo Model
        10. GPT-3.5 Turbo Model
        11. Save and Return
        12. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['general']['file'] = click.prompt("Enter files to edit with an LLM (optional)", default=config.get('general', {}).get('file', 'example.py'))
        elif choice == 2:
            config['general']['openai_api_key'] = click.prompt("Specify the OpenAI API key", default=config.get('general', {}).get('openai_api_key', 'your-openai-api-key'))
        elif choice == 3:
            config['general']['anthropic_api_key'] = click.prompt("Specify the Anthropic API key", default=config.get('general', {}).get('anthropic_api_key', 'your-anthropic-api-key'))
        elif choice == 4:
            config['general']['model'] = click.prompt("Specify the model to use for the main chat (default: gpt-4o)", default=config.get('general', {}).get('model', 'gpt-4o'))
        elif choice == 5:
            config['general']['opus'] = click.prompt("Use claude-3-opus-20240229 model for the main chat", default=config.get('general', {}).get('opus', 'False'))
        elif choice == 6:
            config['general']['sonnet'] = click.prompt("Use claude-3-sonnet-20240229 model for the main chat", default=config.get('general', {}).get('sonnet', 'False'))
        elif choice == 7:
            config['general']['4'] = click.prompt("Use gpt-4-0613 model for the main chat", default=config.get('general', {}).get('4', 'False'))
        elif choice == 8:
            config['general']['4o'] = click.prompt("Use gpt-4o model for the main chat", default=config.get('general', {}).get('4o', 'False'))
        elif choice == 9:
            config['general']['4_turbo'] = click.prompt("Use gpt-4-1106-preview model for the main chat", default=config.get('general', {}).get('4_turbo', 'False'))
        elif choice == 10:
            config['general']['35turbo'] = click.prompt("Use gpt-3.5-turbo model for the main chat", default=config.get('general', {}).get('35turbo', 'False'))
        elif choice == 11:
            # Save and return to the previous menu
            break
        elif choice == 12:
            # Cancel and return to the previous menu without saving
            config['general'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")
def configure_model_settings(config):
    # Ensure 'model_settings' key exists in config
    if 'model_settings' not in config:
        config['model_settings'] = {}

    click.echo("\nModel Settings")
    while True:
        click.echo("""
        Model Settings:
        1. List Known Models
        2. API Base URL
        3. API Type
        4. API Version
        5. API Deployment ID
        6. Organization ID
        7. Edit Format
        8. Weak Model
        9. Show Model Warnings
        10. Max Tokens for Repo Map
        11. Max Chat History Tokens
        12. Env File
        13. Save and Return
        14. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['model_settings']['models'] = click.prompt("List known models which match the (partial) MODEL name", default=config.get('model_settings', {}).get('models', 'gpt-4o'))
        elif choice == 2:
            config['model_settings']['openai_api_base'] = click.prompt("Specify the API base URL", default=config.get('model_settings', {}).get('openai_api_base', 'https://api.openai.com'))
        elif choice == 3:
            config['model_settings']['openai_api_type'] = click.prompt("Specify the API type", default=config.get('model_settings', {}).get('openai_api_type', 'openai'))
        elif choice == 4:
            config['model_settings']['openai_api_version'] = click.prompt("Specify the API version", default=config.get('model_settings', {}).get('openai_api_version', 'v1'))
        elif choice == 5:
            config['model_settings']['openai_api_deployment_id'] = click.prompt("Specify the deployment ID", default=config.get('model_settings', {}).get('openai_api_deployment_id', 'deployment_id'))
        elif choice == 6:
            config['model_settings']['openai_organization_id'] = click.prompt("Specify the OpenAI organization ID", default=config.get('model_settings', {}).get('openai_organization_id', 'organization_id'))
        elif choice == 7:
            config['model_settings']['edit_format'] = click.prompt("Specify what edit format the LLM should use", default=config.get('model_settings', {}).get('edit_format', 'default'))
        elif choice == 8:
            config['model_settings']['weak_model'] = click.prompt("Specify the model to use for commit messages and chat history summarization", default=config.get('model_settings', {}).get('weak_model', 'default'))
        elif choice == 9:
            config['model_settings']['show_model_warnings'] = click.prompt("Only work with models that have meta-data available (True/False)", default=config.get('model_settings', {}).get('show_model_warnings', 'True'))
        elif choice == 10:
            config['model_settings']['map_tokens'] = click.prompt("Max number of tokens to use for repo map", default=config.get('model_settings', {}).get('map_tokens', '1024'))
        elif choice == 11:
            config['model_settings']['max_chat_history_tokens'] = click.prompt("Maximum number of tokens to use for chat history", default=config.get('model_settings', {}).get('max_chat_history_tokens', '4096'))
        elif choice == 12:
            config['model_settings']['env_file'] = click.prompt("Specify the .env file to load", default=config.get('model_settings', {}).get('env_file', '.env'))
        elif choice == 13:
            # Save and return to the previous menu
            break
        elif choice == 14:
            # Cancel and return to the previous menu without saving
            config['model_settings'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")


def configure_history_settings(config):
    # Ensure 'history_settings' key exists in config
    if 'history_settings' not in config:
        config['history_settings'] = {}

    click.echo("\nHistory Settings")
    while True:
        click.echo("""
        History Settings:
        1. Chat Input History File
        2. Chat History File
        3. Restore Chat History
        4. Save and Return
        5. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['history_settings']['input_history_file'] = click.prompt("Specify the chat input history file", default=config.get('history_settings', {}).get('input_history_file', '.aider.input.history'))
        elif choice == 2:
            config['history_settings']['chat_history_file'] = click.prompt("Specify the chat history file", default=config.get('history_settings', {}).get('chat_history_file', '.aider.chat.history.md'))
        elif choice == 3:
            config['history_settings']['restore_chat_history'] = click.prompt("Restore the previous chat history messages (True/False)", default=config.get('history_settings', {}).get('restore_chat_history', 'False'))
        elif choice == 4:
            # Save and return to the previous menu
            break
        elif choice == 5:
            # Cancel and return to the previous menu without saving
            config['history_settings'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")


def configure_output_settings(config):
    # Ensure 'output_settings' key exists in config
    if 'output_settings' not in config:
        config['output_settings'] = {}

    click.echo("\nOutput Settings")
    while True:
        click.echo("""
        Output Settings:
        1. Dark Mode
        2. Light Mode
        3. Pretty Output
        4. Streaming Responses
        5. User Input Color
        6. Tool Output Color
        7. Tool Error Color
        8. Assistant Output Color
        9. Code Theme
        10. Show Diffs
        11. Save and Return
        12. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['output_settings']['dark_mode'] = click.prompt("Use colors suitable for a dark terminal background (True/False)", default=config.get('output_settings', {}).get('dark_mode', 'False'))
        elif choice == 2:
            config['output_settings']['light_mode'] = click.prompt("Use colors suitable for a light terminal background (True/False)", default=config.get('output_settings', {}).get('light_mode', 'False'))
        elif choice == 3:
            config['output_settings']['pretty'] = click.prompt("Enable/disable pretty, colorized output (True/False)", default=config.get('output_settings', {}).get('pretty', 'True'))
        elif choice == 4:
            config['output_settings']['stream'] = click.prompt("Enable/disable streaming responses (True/False)", default=config.get('output_settings', {}).get('stream', 'True'))
        elif choice == 5:
            config['output_settings']['user_input_color'] = click.prompt("Set the color for user input", default=config.get('output_settings', {}).get('user_input_color', '#00cc00'))
        elif choice == 6:
            config['output_settings']['tool_output_color'] = click.prompt("Set the color for tool output", default=config.get('output_settings', {}).get('tool_output_color', None))
        elif choice == 7:
            config['output_settings']['tool_error_color'] = click.prompt("Set the color for tool error messages", default=config.get('output_settings', {}).get('tool_error_color', 'red'))
        elif choice == 8:
            config['output_settings']['assistant_output_color'] = click.prompt("Set the color for assistant output", default=config.get('output_settings', {}).get('assistant_output_color', '#0088ff'))
        elif choice == 9:
            config['output_settings']['code_theme'] = click.prompt("Set the markdown code theme", default=config.get('output_settings', {}).get('code_theme', 'default'))
        elif choice == 10:
            config['output_settings']['show_diffs'] = click.prompt("Show diffs when committing changes (True/False)", default=config.get('output_settings', {}).get('show_diffs', 'False'))
        elif choice == 11:
            # Save and return to the previous menu
            break
        elif choice == 12:
            # Cancel and return to the previous menu without saving
            config['output_settings'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")

def configure_git_settings(config):
    # Ensure 'git_settings' key exists in config
    if 'git_settings' not in config:
        config['git_settings'] = {}

    click.echo("\nGit Settings")
    while True:
        click.echo("""
        Git Settings:
        1. Enable/Disable Git Repo
        2. Enable/Disable .aider* in .gitignore
        3. Specify Aider Ignore File
        4. Enable/Disable Auto Commits
        5. Enable/Disable Commits When Repo is Dirty
        6. Perform a Dry Run Without Modifying Files
        7. Save and Return
        8. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['git_settings']['git'] = click.prompt("Enable/disable looking for a git repo (True/False)", default=config.get('git_settings', {}).get('git', 'True'))
        elif choice == 2:
            config['git_settings']['gitignore'] = click.prompt("Enable/disable adding .aider* to .gitignore (True/False)", default=config.get('git_settings', {}).get('gitignore', 'True'))
        elif choice == 3:
            config['git_settings']['aiderignore'] = click.prompt("Specify the aider ignore file", default=config.get('git_settings', {}).get('aiderignore', '.aiderignore'))
        elif choice == 4:
            config['git_settings']['auto_commits'] = click.prompt("Enable/disable auto commit of LLM changes (True/False)", default=config.get('git_settings', {}).get('auto_commits', 'True'))
        elif choice == 5:
            config['git_settings']['dirty_commits'] = click.prompt("Enable/disable commits when repo is found dirty (True/False)", default=config.get('git_settings', {}).get('dirty_commits', 'True'))
        elif choice == 6:
            config['git_settings']['dry_run'] = click.prompt("Perform a dry run without modifying files (True/False)", default=config.get('git_settings', {}).get('dry_run', 'False'))
        elif choice == 7:
            # Save and return to the previous menu
            break
        elif choice == 8:
            # Cancel and return to the previous menu without saving
            config['git_settings'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")


def configure_other_settings(config):
    # Ensure 'other_settings' key exists in config
    if 'other_settings' not in config:
        config['other_settings'] = {}

    click.echo("\nOther Settings")
    while True:
        click.echo("""
        Other Settings:
        1. Voice Language
        2. Version
        3. Check for Updates
        4. Skip Update Check
        5. Apply Changes from File
        6. Always Say Yes to Every Confirmation
        7. Save and Return
        8. Cancel
        """)
        choice = click.prompt("Please choose an option", type=int)
        
        if choice == 1:
            config['other_settings']['voice_language'] = click.prompt("Specify the language for voice using ISO 639-1 code", default=config.get('other_settings', {}).get('voice_language', 'auto'))
        elif choice == 2:
            config['other_settings']['version'] = click.prompt("Show the version number and exit", default=config.get('other_settings', {}).get('version', '0.0.5'))
        elif choice == 3:
            config['other_settings']['check_update'] = click.prompt("Check for updates and return status in the exit code (True/False)", default=config.get('other_settings', {}).get('check_update', 'True'))
        elif choice == 4:
            config['other_settings']['skip_check_update'] = click.prompt("Skips checking for the update when the program runs (True/False)", default=config.get('other_settings', {}).get('skip_check_update', 'False'))
        elif choice == 5:
            config['other_settings']['apply'] = click.prompt("Apply the changes from the given file instead of running the chat (debug)", default=config.get('other_settings', {}).get('apply', None))
        elif choice == 6:
            config['other_settings']['yes'] = click.prompt("Always say yes to every confirmation (True/False)", default=config.get('other_settings', {}).get('yes', 'False'))
        elif choice == 7:
            # Save and return to the previous menu
            break
        elif choice == 8:
            # Cancel and return to the previous menu without saving
            config['other_settings'] = {}  # Clear changes
            break
        else:
            click.echo("Invalid choice. Please try again.")

def main_menu():
    while True:
        click.echo(r"""
        Main Menu:
        1. Start WebUI 🌐
        2. Settings ⚙️
        3. Exit ❌
        """)
        choice = click.prompt("Please choose an option", type=int)
        if choice == 1:
            start_webui()
        elif choice == 2:
            show_settings()
        elif choice == 3:
            click.echo("Exiting... Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")

def main():
    import sys
    if '--gui' not in sys.argv:
        sys.argv.append('--gui')
    welcome()
    main_menu()

if __name__ == "__main__":
    main()
