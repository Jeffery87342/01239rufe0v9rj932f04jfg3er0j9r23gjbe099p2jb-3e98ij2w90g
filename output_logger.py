#!/usr/bin/env python3
"""
Output Logger Module
Provides color-coded, thread-safe console output with timestamps.
"""

from datetime import datetime
from colorama import init, Fore, Style
from threading import Lock

# Initialize colorama
init(autoreset=True)

# Thread-safe lock for console output
_output_lock = Lock()


class Output:
    """Color-coded logger for console output."""
    
    # Color and icon mappings for different log levels
    COLOR_MAP = {
        "INFO": (Fore.LIGHTBLUE_EX, "ℹ"),
        "CAPTCHA": (Fore.WHITE, "🤖"),
        "ERROR": (Fore.LIGHTRED_EX, "❌"),
        "SUCCESS": (Fore.LIGHTGREEN_EX, "✅"),
        "WARNING": (Fore.YELLOW, "⚠"),
        "DEBUG": (Fore.MAGENTA, "🔍"),
        "PROXY": (Fore.CYAN, "🌐"),
        "ACCOUNT": (Fore.GREEN, "👤"),
    }
    
    def __init__(self, level: str = "INFO"):
        """
        Initialize output logger.
        
        Args:
            level: Log level (INFO, ERROR, SUCCESS, etc.)
        """
        self.level = level.upper()
    
    def log(self, *args, **kwargs):
        """
        Log a message with color coding and timestamp.
        
        Args:
            *args: Message components to log
            **kwargs: Additional keyword arguments
        """
        color, icon = self.COLOR_MAP.get(self.level, (Fore.WHITE, "•"))
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # Build message
        base = f"{Fore.LIGHTBLACK_EX}[{time_now}]{Fore.RESET} ({color}{icon}{Fore.RESET})"
        
        for arg in args:
            base += f"{color} {arg}{Fore.RESET}"
        
        # Thread-safe output
        with _output_lock:
            print(base)
    
    @staticmethod
    def print_header():
        """Print application header."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}    ROBLOX ACCOUNT GENERATOR - ML-POWERED FUNCAPTCHA SOLVER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═' * 70}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_stats(generated: int, failed: int, cpm: int, elapsed: str):
        """
        Print generation statistics.
        
        Args:
            generated: Number of successful accounts
            failed: Number of failures
            cpm: Captchas per minute
            elapsed: Elapsed time string
        """
        total = generated + failed
        success_rate = (generated / total * 100) if total > 0 else 0
        
        print(f"\n{Fore.CYAN}{'─' * 70}{Fore.RESET}")
        print(f"{Fore.GREEN}✓ Generated:{Fore.WHITE} {generated:>6}{Fore.RESET}  "
              f"{Fore.RED}✗ Failed:{Fore.WHITE} {failed:>6}{Fore.RESET}  "
              f"{Fore.YELLOW}Success:{Fore.WHITE} {success_rate:>5.1f}%{Fore.RESET}  "
              f"{Fore.MAGENTA}CPM:{Fore.WHITE} {cpm:>4}{Fore.RESET}  "
              f"{Fore.CYAN}Time:{Fore.WHITE} {elapsed}{Fore.RESET}")
        print(f"{Fore.CYAN}{'─' * 70}{Fore.RESET}\n")
