import click

settings = {
    "model": "gpt-4o",
    "weak_model": "gpt-3.5-turbo",
    "max_tokens": 1024
}

def update_settings():
    click.echo("\n🛠️ Update Settings")
    settings["model"] = click.prompt("Enter model to use", default=settings["model"])
    settings["weak_model"] = click.prompt("Enter weak model to use", default=settings["weak_model"])
    settings["max_tokens"] = click.prompt("Enter max tokens", default=settings["max_tokens"], type=int)
    click.echo("✅ Settings updated successfully.")
    settings_menu()

def view_settings():
    click.echo("\n🔧 Current Settings")
    for key, value in settings.items():
        click.echo(f"{key}: {value}")
    settings_menu()

def settings_menu():
    click.echo("\n📋 Settings Menu")
    click.echo("1. View Settings")
    click.echo("2. Update Settings")
    click.echo("3. Back to Main Menu")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        view_settings()
    elif choice == 2:
        update_settings()
    elif choice == 3:
        from ..coder import coder_menu
        coder_menu()
    else:
        click.echo("\n❌ Invalid choice. Please try again.")
        settings_menu()
