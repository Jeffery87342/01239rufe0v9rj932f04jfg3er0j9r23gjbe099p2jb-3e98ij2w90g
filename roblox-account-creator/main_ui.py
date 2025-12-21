#!/usr/bin/env python3
"""
Roblox Account Creator - Interactive UI
Clean and functional interface for automated Roblox account creation.
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Optional
from roblox_signup import RobloxAccountCreator, create_multiple_accounts


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the application header."""
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║        ROBLOX ACCOUNT CREATOR WITH FUNCAPTCHA SOLVER             ║")
    print("║                                                                   ║")
    print("║                  Automatic Account Generation                     ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")


def print_menu():
    """Print the main menu."""
    print(f"\n{Colors.BOLD}MAIN MENU{Colors.ENDC}")
    print("─" * 50)
    print(f"{Colors.GREEN}[1]{Colors.ENDC} Create Single Account")
    print(f"{Colors.GREEN}[2]{Colors.ENDC} Create Multiple Accounts")
    print(f"{Colors.GREEN}[3]{Colors.ENDC} View Created Accounts")
    print(f"{Colors.GREEN}[4]{Colors.ENDC} Settings")
    print(f"{Colors.GREEN}[5]{Colors.ENDC} Help")
    print(f"{Colors.FAIL}[6]{Colors.ENDC} Exit")
    print("─" * 50)


def print_settings_menu():
    """Print the settings menu."""
    print(f"\n{Colors.BOLD}SETTINGS{Colors.ENDC}")
    print("─" * 50)
    print(f"{Colors.GREEN}[1]{Colors.ENDC} Configure Proxy")
    print(f"{Colors.GREEN}[2]{Colors.ENDC} Set Creation Delay")
    print(f"{Colors.GREEN}[3]{Colors.ENDC} View Current Settings")
    print(f"{Colors.GREEN}[4]{Colors.ENDC} Back to Main Menu")
    print("─" * 50)


def get_input(prompt: str, input_type=str, default=None):
    """
    Get user input with type validation.
    
    Args:
        prompt: Input prompt message
        input_type: Expected type (str, int, etc.)
        default: Default value if user presses Enter
        
    Returns:
        User input converted to the specified type
    """
    while True:
        try:
            if default is not None:
                user_input = input(f"{Colors.CYAN}{prompt} [{default}]: {Colors.ENDC}").strip()
                if not user_input:
                    return default
            else:
                user_input = input(f"{Colors.CYAN}{prompt}: {Colors.ENDC}").strip()
            
            if input_type == int:
                return int(user_input)
            elif input_type == bool:
                return user_input.lower() in ['y', 'yes', 'true', '1']
            else:
                return user_input
        except ValueError:
            print(f"{Colors.FAIL}Invalid input. Please try again.{Colors.ENDC}")


def create_single_account(proxy: Optional[str] = None):
    """Create a single account with UI feedback."""
    print_header()
    print(f"\n{Colors.BOLD}CREATE SINGLE ACCOUNT{Colors.ENDC}")
    print("─" * 50)
    
    creator = RobloxAccountCreator(proxy=proxy)
    
    print(f"\n{Colors.BLUE}Initializing account creation...{Colors.ENDC}")
    time.sleep(0.5)
    
    result = creator.create_random_account()
    
    if result:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ SUCCESS!{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Account Details:{Colors.ENDC}")
        print("─" * 50)
        print(f"Username: {Colors.CYAN}{result['username']}{Colors.ENDC}")
        print(f"Password: {Colors.CYAN}{result['password']}{Colors.ENDC}")
        print(f"Created:  {Colors.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print("─" * 50)
        print(f"\n{Colors.GREEN}Account saved to 'accounts.txt'{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}✗ FAILED{Colors.ENDC}")
        print(f"{Colors.WARNING}Account creation was unsuccessful. Please try again.{Colors.ENDC}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


def create_multiple_accounts_ui(proxy: Optional[str] = None, delay: int = 5):
    """Create multiple accounts with UI feedback."""
    print_header()
    print(f"\n{Colors.BOLD}CREATE MULTIPLE ACCOUNTS{Colors.ENDC}")
    print("─" * 50)
    
    count = get_input("How many accounts to create?", int)
    
    if count <= 0:
        print(f"{Colors.FAIL}Invalid number. Must be greater than 0.{Colors.ENDC}")
        time.sleep(2)
        return
    
    print(f"\n{Colors.BLUE}Starting creation of {count} account(s)...{Colors.ENDC}")
    print(f"{Colors.WARNING}This may take several minutes. Please wait...{Colors.ENDC}\n")
    
    time.sleep(1)
    
    create_multiple_accounts(count, proxy=proxy, delay=delay)
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


def view_accounts():
    """View created accounts from the file."""
    print_header()
    print(f"\n{Colors.BOLD}CREATED ACCOUNTS{Colors.ENDC}")
    print("─" * 50)
    
    accounts_file = "accounts.txt"
    
    if not os.path.exists(accounts_file):
        print(f"\n{Colors.WARNING}No accounts file found.{Colors.ENDC}")
        print(f"{Colors.BLUE}Create some accounts first!{Colors.ENDC}")
    else:
        try:
            with open(accounts_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if content.strip():
                # Count accounts
                account_count = content.count("User:")
                
                print(f"\n{Colors.GREEN}Total Accounts: {account_count}{Colors.ENDC}\n")
                print(content)
            else:
                print(f"\n{Colors.WARNING}Accounts file is empty.{Colors.ENDC}")
                
        except Exception as e:
            print(f"\n{Colors.FAIL}Error reading accounts: {e}{Colors.ENDC}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


def settings_menu():
    """Settings configuration menu."""
    config = load_config()
    
    while True:
        print_header()
        print_settings_menu()
        
        choice = get_input("Select an option", str)
        
        if choice == '1':
            # Configure proxy
            print(f"\n{Colors.BOLD}PROXY CONFIGURATION{Colors.ENDC}")
            print("─" * 50)
            use_proxy = get_input("Use proxy? (y/n)", str, "n")
            
            if use_proxy.lower() in ['y', 'yes']:
                proxy = get_input("Enter proxy URL (e.g., http://proxy.com:8080)", str)
                config['proxy'] = proxy
                print(f"{Colors.GREEN}Proxy configured!{Colors.ENDC}")
            else:
                config['proxy'] = None
                print(f"{Colors.GREEN}Proxy disabled.{Colors.ENDC}")
            
            save_config(config)
            time.sleep(1.5)
            
        elif choice == '2':
            # Set creation delay
            print(f"\n{Colors.BOLD}CREATION DELAY{Colors.ENDC}")
            print("─" * 50)
            delay = get_input("Delay between account creations (seconds)", int, 5)
            config['delay'] = delay
            save_config(config)
            print(f"{Colors.GREEN}Delay set to {delay} seconds!{Colors.ENDC}")
            time.sleep(1.5)
            
        elif choice == '3':
            # View settings
            print(f"\n{Colors.BOLD}CURRENT SETTINGS{Colors.ENDC}")
            print("─" * 50)
            print(f"Proxy: {Colors.CYAN}{config.get('proxy', 'Not configured')}{Colors.ENDC}")
            print(f"Delay: {Colors.CYAN}{config.get('delay', 5)} seconds{Colors.ENDC}")
            print("─" * 50)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == '4':
            # Back to main menu
            break
        else:
            print(f"{Colors.FAIL}Invalid option. Please try again.{Colors.ENDC}")
            time.sleep(1)


def show_help():
    """Display help information."""
    print_header()
    print(f"\n{Colors.BOLD}HELP & INFORMATION{Colors.ENDC}")
    print("─" * 50)
    print(f"""
{Colors.CYAN}What does this tool do?{Colors.ENDC}
This tool automatically creates Roblox accounts by:
  • Generating random usernames and passwords
  • Solving FunCaptcha challenges automatically
  • Creating accounts through Roblox signup API
  • Saving account details to 'accounts.txt'

{Colors.CYAN}How to use:{Colors.ENDC}
  1. Select option 1 to create a single account
  2. Select option 2 to create multiple accounts
  3. View created accounts with option 3
  4. Configure proxy and settings with option 4

{Colors.CYAN}Account Information:{Colors.ENDC}
All created accounts are saved in 'accounts.txt' with:
  • Username
  • Password
  • Session cookies
  • Creation timestamp

{Colors.CYAN}Requirements:{Colors.ENDC}
  • Python 3.7+
  • Internet connection
  • All dependencies installed (see requirements.txt)

{Colors.CYAN}Tips:{Colors.ENDC}
  • Use a delay of at least 5 seconds between account creations
  • Proxy usage is optional but recommended for bulk creation
  • Keep the accounts.txt file secure

{Colors.CYAN}Troubleshooting:{Colors.ENDC}
  • If FunCaptcha fails, try again or increase delay
  • Check your internet connection
  • Ensure all dependencies are installed
    """)
    print("─" * 50)
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


def load_config():
    """Load configuration from file."""
    config_file = "config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Default config
    return {
        'proxy': None,
        'delay': 5
    }


def save_config(config):
    """Save configuration to file."""
    config_file = "config.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"{Colors.FAIL}Error saving config: {e}{Colors.ENDC}")


def main():
    """Main application loop."""
    config = load_config()
    
    while True:
        print_header()
        print_menu()
        
        choice = get_input("Select an option", str)
        
        if choice == '1':
            create_single_account(proxy=config.get('proxy'))
            
        elif choice == '2':
            create_multiple_accounts_ui(
                proxy=config.get('proxy'),
                delay=config.get('delay', 5)
            )
            
        elif choice == '3':
            view_accounts()
            
        elif choice == '4':
            settings_menu()
            config = load_config()  # Reload config after settings
            
        elif choice == '5':
            show_help()
            
        elif choice == '6':
            print(f"\n{Colors.CYAN}Thank you for using Roblox Account Creator!{Colors.ENDC}")
            print(f"{Colors.GREEN}Goodbye!{Colors.ENDC}\n")
            sys.exit(0)
            
        else:
            print(f"{Colors.FAIL}Invalid option. Please try again.{Colors.ENDC}")
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Program interrupted by user.{Colors.ENDC}")
        print(f"{Colors.CYAN}Goodbye!{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}An error occurred: {e}{Colors.ENDC}")
        input(f"\n{Colors.CYAN}Press Enter to exit...{Colors.ENDC}")
        sys.exit(1)
