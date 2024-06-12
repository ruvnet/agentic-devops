#!/bin/bash

# Function to display the menu
show_menu() {
    echo "1) Install ./chat"
    echo "2) Exit"
}

# Function to install ./chat
install_chat() {
    echo "Installing ./chat..."
    cd ./chat || exit
    npm install
    echo "./chat installed successfully."
}

# Main script logic
while true; do
    show_menu
    read -rp "Enter your choice: " choice
    case $choice in
        1)
            install_chat
            ;;
        2)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice, please try again."
            ;;
    esac
done
