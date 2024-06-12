#!/bin/bash

# Function to display the menu
show_menu() {
    echo "1) Install ./chat"
    echo "2) Run CLI"
    echo "3) Exit"
}

# Function to install ./chat
install_chat() {
    echo "Installing ./chat..."
    cd ./chat || exit
    npm install
    echo "./chat installed successfully."
}

# Function to run the CLI
run_cli() {
    echo "Running CLI..."
    python3 cli.py hello
}
while true; do
    show_menu
    read -rp "Enter your choice: " choice
    case $choice in
        1)
            install_chat
            ;;
        2)
            run_cli
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice, please try again."
            ;;
    esac
done
