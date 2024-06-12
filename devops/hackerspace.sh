#!/bin/bash

# Description: A multi-level menu BBS style Azure deployment script

function main_menu() {
    clear
    echo "===================="
    echo "  Hackerspace Menu  "
    echo "===================="
    echo "1. Deploy Resources"
    echo "2. Manage Resources"
    echo "3. Exit"
    echo "===================="
    read -p "Enter your choice [1-3]: " choice
    case $choice in
        1) deploy_menu ;;
        2) manage_menu ;;
        3) exit 0 ;;
        *) echo "Invalid choice!" && sleep 2 && main_menu ;;
    esac
}

function deploy_menu() {
    clear
    echo "===================="
    echo "  Deploy Resources  "
    echo "===================="
    echo "1. Create Resource Group"
    echo "2. Create Virtual Machine"
    echo "3. Back to Main Menu"
    echo "===================="
    read -p "Enter your choice [1-3]: " choice
    case $choice in
        1) create_resource_group ;;
        2) create_virtual_machine ;;
        3) main_menu ;;
        *) echo "Invalid choice!" && sleep 2 && deploy_menu ;;
    esac
}

function manage_menu() {
    clear
    echo "===================="
    echo "  Manage Resources  "
    echo "===================="
    echo "1. List Resource Groups"
    echo "2. List Virtual Machines"
    echo "3. Back to Main Menu"
    echo "===================="
    read -p "Enter your choice [1-3]: " choice
    case $choice in
        1) list_resource_groups ;;
        2) list_virtual_machines ;;
        3) main_menu ;;
        *) echo "Invalid choice!" && sleep 2 && manage_menu ;;
    esac
}

function create_resource_group() {
    read -p "Enter Resource Group Name: " rg_name
    read -p "Enter Location: " location
    az group create --name $rg_name --location $location
    echo "Resource Group $rg_name created."
    sleep 2
    deploy_menu
}

function create_virtual_machine() {
    read -p "Enter Resource Group Name: " rg_name
    read -p "Enter VM Name: " vm_name
    read -p "Enter Image (e.g., UbuntuLTS): " image
    az vm create --resource-group $rg_name --name $vm_name --image $image
    echo "Virtual Machine $vm_name created."
    sleep 2
    deploy_menu
}

function list_resource_groups() {
    az group list --output table
    sleep 2
    manage_menu
}

function list_virtual_machines() {
    az vm list --output table
    sleep 2
    manage_menu
}

# Start the script
main_menu
