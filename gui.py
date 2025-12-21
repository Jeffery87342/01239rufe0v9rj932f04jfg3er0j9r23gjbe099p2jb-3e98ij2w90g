#!/usr/bin/env python3
"""
Roblox Account Creator - Advanced GUI with Proxy Support
Clean UI with Start/Stop controls and proxy rotation from file.
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from typing import Optional, List
from colorama import init, Fore, Back, Style
from roblox_signup import RobloxAccountCreator

# Initialize colorama for Windows color support
init(autoreset=True)


class ProxyManager:
    """Manages proxy rotation from proxies.txt file."""
    
    def __init__(self, proxy_file: str = "proxies.txt"):
        """
        Initialize proxy manager.
        
        Args:
            proxy_file: Path to file containing proxies (one per line)
        """
        self.proxy_file = proxy_file
        self.proxies = []
        self.current_index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file."""
        if os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r', encoding='utf-8') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                
                if self.proxies:
                    print(f"{Fore.GREEN}[+] Loaded {len(self.proxies)} proxies from {self.proxy_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] No proxies found in {self.proxy_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error loading proxies: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Proxy file '{self.proxy_file}' not found. Running without proxies.{Style.RESET_ALL}")
            # Create empty proxy file for user
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                f.write("# Add your proxies here, one per line\n")
                f.write("# Format: http://ip:port or http://user:pass@ip:port\n")
                f.write("# Example: http://127.0.0.1:8080\n")
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Get the next proxy from the rotation.
        
        Returns:
            Proxy URL or None if no proxies available
        """
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def has_proxies(self) -> bool:
        """Check if any proxies are loaded."""
        return len(self.proxies) > 0


class AccountGenerator:
    """Manages account generation with start/stop controls."""
    
    def __init__(self):
        """Initialize the account generator."""
        self.is_running = False
        self.should_stop = False
        self.thread = None
        self.target_count = 0
        self.generated_count = 0
        self.failed_count = 0
        self.proxy_manager = ProxyManager()
        self.start_time = None
    
    def start_generation(self, count: int):
        """
        Start account generation in a separate thread.
        
        Args:
            count: Number of accounts to generate
        """
        if self.is_running:
            print(f"{Fore.YELLOW}[!] Generation already in progress!{Style.RESET_ALL}")
            return
        
        self.target_count = count
        self.generated_count = 0
        self.failed_count = 0
        self.should_stop = False
        self.start_time = time.time()
        
        # Start generation in background thread
        self.thread = threading.Thread(target=self._generate_accounts)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_generation(self):
        """Stop the account generation process."""
        if self.is_running:
            print(f"\n{Fore.YELLOW}[!] Stopping generation... Please wait.{Style.RESET_ALL}")
            self.should_stop = True
        else:
            print(f"{Fore.YELLOW}[!] No generation in progress.{Style.RESET_ALL}")
    
    def _generate_accounts(self):
        """Internal method to generate accounts (runs in thread)."""
        self.is_running = True
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}[+] Starting generation of {self.target_count} account(s)...{Style.RESET_ALL}\n")
        
        for i in range(self.target_count):
            if self.should_stop:
                print(f"\n{Fore.YELLOW}[!] Generation stopped by user.{Style.RESET_ALL}")
                break
            
            # Get proxy for this account
            proxy = self.proxy_manager.get_next_proxy() if self.proxy_manager.has_proxies() else None
            
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT}[*] Account {i+1}/{self.target_count}{Style.RESET_ALL}")
            if proxy:
                print(f"{Fore.BLUE}[*] Using proxy: {proxy}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            
            # Create account
            creator = RobloxAccountCreator(proxy=proxy)
            result = creator.create_random_account()
            
            if result:
                self.generated_count += 1
                print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ SUCCESS #{self.generated_count}{Style.RESET_ALL}")
            else:
                self.failed_count += 1
                print(f"\n{Fore.RED}{Style.BRIGHT}✗ FAILED #{self.failed_count}{Style.RESET_ALL}")
            
            # Show progress
            total_processed = self.generated_count + self.failed_count
            success_rate = (self.generated_count / total_processed * 100) if total_processed > 0 else 0
            
            print(f"\n{Fore.YELLOW}━━━ Progress: {total_processed}/{self.target_count} ━━━{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Successful: {self.generated_count}{Style.RESET_ALL}")
            print(f"{Fore.RED}✗ Failed: {self.failed_count}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Success Rate: {success_rate:.1f}%{Style.RESET_ALL}")
            
            # Check if we've reached the target
            if self.generated_count >= self.target_count:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}[+] Target reached! {self.generated_count} accounts generated.{Style.RESET_ALL}")
                break
            
            # Delay between accounts (only if not last account)
            if i < self.target_count - 1 and not self.should_stop:
                delay = 3
                print(f"\n{Fore.BLUE}[*] Waiting {delay} seconds before next account...{Style.RESET_ALL}\n")
                time.sleep(delay)
        
        # Final summary
        self._print_summary()
        self.is_running = False
    
    def _print_summary(self):
        """Print final generation summary."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}                        GENERATION COMPLETE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Target:           {self.target_count} accounts{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Generated:      {self.generated_count} accounts{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Failed:         {self.failed_count} accounts{Style.RESET_ALL}")
        
        total = self.generated_count + self.failed_count
        if total > 0:
            success_rate = (self.generated_count / total) * 100
            print(f"{Fore.CYAN}Success Rate:     {success_rate:.1f}%{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}Time Elapsed:     {elapsed:.1f} seconds{Style.RESET_ALL}")
        
        if self.generated_count > 0:
            avg_time = elapsed / self.generated_count
            print(f"{Fore.MAGENTA}Avg per Account:  {avg_time:.1f} seconds{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header."""
    clear_screen()
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║        ROBLOX ACCOUNT CREATOR - FUNCAPTCHA BYPASS                ║")
    print("║                                                                   ║")
    print("║              Ultra-Fast API-Based Account Generation             ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")


def print_controls(generator: AccountGenerator):
    """Print control interface."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}CONTROLS{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}")
    
    if generator.is_running:
        print(f"{Fore.RED}[S] STOP Generation{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Status: {Style.BRIGHT}RUNNING{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Progress: {generator.generated_count}/{generator.target_count} accounts{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[Enter] START Generation{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Status: {Style.BRIGHT}IDLE{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}[Q] Quit Program{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}\n")


def get_account_count() -> int:
    """Get the number of accounts to generate from user."""
    while True:
        try:
            print(f"{Fore.CYAN}{Style.BRIGHT}How many accounts would you like to generate?{Style.RESET_ALL}")
            count_str = input(f"{Fore.YELLOW}Enter number: {Style.RESET_ALL}").strip()
            
            count = int(count_str)
            
            if count <= 0:
                print(f"{Fore.RED}[!] Please enter a positive number.{Style.RESET_ALL}\n")
                continue
            
            if count > 100:
                confirm = input(f"{Fore.YELLOW}[!] You want to create {count} accounts. Continue? (y/n): {Style.RESET_ALL}").strip().lower()
                if confirm != 'y':
                    continue
            
            return count
            
        except ValueError:
            print(f"{Fore.RED}[!] Invalid input. Please enter a number.{Style.RESET_ALL}\n")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Input cancelled.{Style.RESET_ALL}")
            return 0


def show_proxy_status(proxy_manager: ProxyManager):
    """Display proxy configuration status."""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}PROXY CONFIGURATION{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}")
    
    if proxy_manager.has_proxies():
        print(f"{Fore.GREEN}✓ Proxies Loaded: {len(proxy_manager.proxies)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  File: {proxy_manager.proxy_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Rotation: Enabled{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ No proxies loaded{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  File: {proxy_manager.proxy_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Add proxies to '{proxy_manager.proxy_file}' to enable proxy rotation{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}\n")


def main():
    """Main application with GUI controls."""
    generator = AccountGenerator()
    
    print_header()
    show_proxy_status(generator.proxy_manager)
    
    print(f"{Fore.CYAN}{Style.BRIGHT}Ready to generate Roblox accounts!{Style.RESET_ALL}\n")
    
    # Main control loop
    while True:
        print_controls(generator)
        
        if not generator.is_running:
            # Get number of accounts to generate
            count = get_account_count()
            
            if count == 0:
                continue
            
            print(f"\n{Fore.GREEN}[+] Configuration:{Style.RESET_ALL}")
            print(f"    Accounts to generate: {Fore.CYAN}{count}{Style.RESET_ALL}")
            print(f"    Proxies enabled: {Fore.CYAN}{'Yes' if generator.proxy_manager.has_proxies() else 'No'}{Style.RESET_ALL}")
            
            confirm = input(f"\n{Fore.YELLOW}[?] Start generation? (y/n): {Style.RESET_ALL}").strip().lower()
            
            if confirm == 'y':
                generator.start_generation(count)
                
                # Wait for generation to complete or user to stop
                while generator.is_running:
                    time.sleep(0.5)
                    
                    # Check for stop command
                    # Note: In a real GUI this would be button-based
                
                print(f"\n{Fore.GREEN}[+] Generation session ended.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                print_header()
                show_proxy_status(generator.proxy_manager)
            
        else:
            # Generation is running
            choice = input(f"\n{Fore.YELLOW}Command (S=Stop, Q=Quit): {Style.RESET_ALL}").strip().upper()
            
            if choice == 'S':
                generator.stop_generation()
                # Wait for thread to finish
                while generator.is_running:
                    time.sleep(0.1)
            elif choice == 'Q':
                if generator.is_running:
                    generator.stop_generation()
                    while generator.is_running:
                        time.sleep(0.1)
                break
    
    print(f"\n{Fore.CYAN}Thank you for using Roblox Account Creator!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}All accounts saved to 'accounts.txt'{Style.RESET_ALL}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program interrupted by user.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
        sys.exit(1)
