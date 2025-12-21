"""
Main Account Generator with Threading and CPM Tracking
Multi-threaded Roblox account generator with real-time statistics.
"""

import sys
import os
import ctypes
from time import sleep
from threading import Thread, Event
from colorama import init, Fore, Style
from generate_counter import generate_counter
from generate import Generate
from util import Util

# Initialize colorama
init(autoreset=True)

# Load configuration
config = Util.get_config()

THREAD_AMOUNT = config.get("threads", 5)
USE_PROXIES = config.get("use_proxies", True)

# Global stop event
stop_event = Event()


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def set_console_title(title: str):
    """
    Set the console window title.
    
    Args:
        title: Title string
    """
    try:
        if os.name == 'nt':  # Windows
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:  # Linux/Mac
            sys.stdout.write(f"\x1b]2;{title}\x07")
    except:
        pass


def cpm_checker() -> None:
    """Monitor and update console title with statistics."""
    while not stop_event.is_set():
        elapsed = generate_counter.get_elapsed_seconds()
        generated = generate_counter.get_generated()
        failed = generate_counter.get_failed()
        cpm = generate_counter.get_cpm()
        
        # Format time
        time_str = Util.format_time(elapsed)
        
        # Update console title
        title = f"Elapsed: {time_str} | Generated: {generated} | Failed: {failed} | CPM: {cpm}"
        set_console_title(title)
        
        sleep(1)


def print_header():
    """Print application header."""
    clear_screen()
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║        ROBLOX ACCOUNT GENERATOR - MULTI-THREADED                 ║")
    print("║                                                                   ║")
    print("║              Ultra-Fast FunCaptcha Bypass + Threading            ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")


def print_config():
    """Print current configuration."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}CONFIGURATION{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Threads:       {Fore.WHITE}{THREAD_AMOUNT}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Proxies:       {Fore.WHITE}{'Enabled' if USE_PROXIES else 'Disabled'}{Style.RESET_ALL}")
    
    if USE_PROXIES:
        proxies = Util.load_proxies()
        print(f"{Fore.CYAN}Proxy Count:   {Fore.WHITE}{len(proxies)}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Output File:   {Fore.WHITE}{config.get('output_file', 'accounts.txt')}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*70}{Style.RESET_ALL}\n")


def print_stats():
    """Print live statistics."""
    generated = generate_counter.get_generated()
    failed = generate_counter.get_failed()
    total = generate_counter.get_total()
    success_rate = generate_counter.get_success_rate()
    cpm = generate_counter.get_cpm()
    elapsed = generate_counter.get_elapsed_seconds()
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}                         LIVE STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✓ Generated:      {generated}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ Failed:         {failed}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Total Attempts:   {total}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Success Rate:     {success_rate:.1f}%{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}CPM:              {cpm}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Elapsed:          {Util.format_time(elapsed)}{Style.RESET_ALL}")
    
    # Show error breakdown
    errors = generate_counter.get_errors()
    if errors:
        print(f"\n{Fore.YELLOW}Error Breakdown:{Style.RESET_ALL}")
        for error_type, count in sorted(errors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {Fore.RED}• {error_type}: {count}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}\n")


def display_realtime_stats():
    """Display real-time statistics in a loop."""
    while not stop_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header()
        print_config()
        print_stats()
        
        print(f"{Fore.YELLOW}Press Ctrl+C to stop generation...{Style.RESET_ALL}")
        
        sleep(2)


def main() -> None:
    """Main function with multi-threading support."""
    print_header()
    print_config()
    
    # Get target number of accounts
    try:
        target_str = input(f"{Fore.CYAN}How many accounts would you like to generate? {Style.RESET_ALL}").strip()
        target = int(target_str)
        
        if target <= 0:
            print(f"{Fore.RED}Invalid number. Must be greater than 0.{Style.RESET_ALL}")
            return
        
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        return
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Cancelled.{Style.RESET_ALL}")
        return
    
    # Load proxies if enabled
    proxies = []
    if USE_PROXIES:
        proxies = Util.load_proxies()
        
        if not proxies:
            print(f"{Fore.YELLOW}[!] Warning: Proxies enabled but no proxies loaded{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Add proxies to 'proxies.txt' or disable in config.json{Style.RESET_ALL}")
            
            use_anyway = input(f"{Fore.CYAN}Continue without proxies? (y/n): {Style.RESET_ALL}").strip().lower()
            if use_anyway != 'y':
                return
    
    print(f"\n{Fore.GREEN}[+] Starting generation with {THREAD_AMOUNT} threads...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Target: {target} accounts{Style.RESET_ALL}\n")
    
    sleep(2)
    
    # Start counter
    generate_counter.reset()
    generate_counter.start()
    
    # Start worker threads
    threads = []
    
    for i in range(THREAD_AMOUNT):
        # Assign proxy if available
        proxy = None
        if proxies:
            proxy = proxies[i % len(proxies)]
        
        # Create thread
        t = Thread(
            target=Generate.gen_with_target,
            args=(generate_counter, target, proxy, stop_event)
        )
        threads.append(t)
        t.daemon = True
        t.start()
    
    # Start CPM checker thread
    cpm_thread = Thread(target=cpm_checker)
    cpm_thread.daemon = True
    cpm_thread.start()
    
    # Start stats display thread
    stats_thread = Thread(target=display_realtime_stats)
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        # Wait for target to be reached or user interrupt
        while generate_counter.get_generated() < target:
            sleep(0.5)
        
        # Target reached
        print(f"\n{Fore.GREEN}{Style.BRIGHT}[+] TARGET REACHED!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Stopping generation...{Style.RESET_ALL}")
    
    finally:
        # Signal threads to stop
        stop_event.set()
        
        # Wait a moment for threads to finish
        sleep(2)
        
        # Print final statistics
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header()
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}                      FINAL STATISTICS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}")
        
        generated = generate_counter.get_generated()
        failed = generate_counter.get_failed()
        total = generate_counter.get_total()
        success_rate = generate_counter.get_success_rate()
        elapsed = generate_counter.get_elapsed_seconds()
        
        print(f"{Fore.GREEN}✓ Generated:      {generated}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Failed:         {failed}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Total Attempts:   {total}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Success Rate:     {success_rate:.1f}%{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total Time:       {Util.format_time(elapsed)}{Style.RESET_ALL}")
        
        if generated > 0:
            avg_time = elapsed / generated
            print(f"{Fore.MAGENTA}Avg per Account:  {avg_time:.1f} seconds{Style.RESET_ALL}")
        
        # Show error breakdown
        errors = generate_counter.get_errors()
        if errors:
            print(f"\n{Fore.YELLOW}Error Breakdown:{Style.RESET_ALL}")
            for error_type, count in sorted(errors.items(), key=lambda x: x[1], reverse=True):
                print(f"  {Fore.RED}• {error_type}: {count}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*70}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}All accounts saved to '{config.get('output_file', 'accounts.txt')}'{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Thank you for using Roblox Account Generator!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
