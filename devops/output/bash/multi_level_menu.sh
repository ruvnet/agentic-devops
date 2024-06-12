#!/bin/bash

# Function to display the main menu
main_menu() {
    echo "Main Menu"
    echo "1. Option 1"
    echo "2. Option 2"
    echo "3. Exit"
    read -p "Enter your choice: " choice
    case $choice in
        1) option1_menu ;;
        2) option2_menu ;;
        3) exit 0 ;;
        *) echo "Invalid choice" && main_menu ;;
    esac
}

# Function to display the Option 1 menu
option1_menu() {
    echo "Option 1 Menu"
    echo "1. Sub-option 1"
    echo "2. Sub-option 2"
    echo "3. Back to Main Menu"
    read -p "Enter your choice: " choice
    case $choice in
        1) echo "You selected Sub-option 1" && option1_menu ;;
        2) echo "You selected Sub-option 2" && option1_menu ;;
        3) main_menu ;;
        *) echo "Invalid choice" && option1_menu ;;
    esac
}

# Function to display the Option 2 menu
option2_menu() {
    echo "Option 2 Menu"
    echo "1. Sub-option 1"
    echo "2. Sub-option 2"
    echo "3. Back to Main Menu"
    read -p "Enter your choice: " choice
    case $choice in
        1) echo "You selected Sub-option 1" && option2_menu ;;
        2) echo "You selected Sub-option 2" && option2_menu ;;
        3) main_menu ;;
        *) echo "Invalid choice" && option2_menu ;;
    esac
}

# Start the script by displaying the main menu
main_menu
