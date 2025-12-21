#!/usr/bin/env python3
"""
Example usage of the FunCaptcha Solver
Demonstrates how to use the solver with various configurations.
"""

from funcaptcha_solver import FunCaptchaSolver
import sys


def example_basic_usage():
    """Basic example of solving a FunCaptcha challenge."""
    
    print("=" * 60)
    print("FunCaptcha Solver - Basic Usage Example")
    print("=" * 60)
    
    # Configuration
    public_key = "YOUR_PUBLIC_KEY_HERE"  # Replace with actual public key
    service_url = "https://client-api.arkoselabs.com"
    page_url = "https://example.com"  # Replace with actual page URL
    
    # Create solver
    solver = FunCaptchaSolver(
        public_key=public_key,
        service_url=service_url,
        page_url=page_url
    )
    
    try:
        # Solve the challenge
        print("\n[*] Starting solver...")
        solution = solver.solve()
        
        print(f"\n[+] SUCCESS! Solution token: {solution}")
        print("\nYou can now use this token to verify the captcha on the website.")
        
        return solution
        
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        return None


def example_with_proxy():
    """Example using a proxy server."""
    
    print("=" * 60)
    print("FunCaptcha Solver - Proxy Usage Example")
    print("=" * 60)
    
    # Configuration with proxy
    public_key = "YOUR_PUBLIC_KEY_HERE"
    service_url = "https://client-api.arkoselabs.com"
    page_url = "https://example.com"
    proxy = "http://proxy.example.com:8080"  # Replace with actual proxy
    
    # Create solver with proxy
    solver = FunCaptchaSolver(
        public_key=public_key,
        service_url=service_url,
        page_url=page_url,
        proxy=proxy
    )
    
    try:
        print(f"\n[*] Using proxy: {proxy}")
        print("[*] Starting solver...")
        solution = solver.solve()
        
        print(f"\n[+] SUCCESS! Solution token: {solution}")
        return solution
        
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        return None


def example_step_by_step():
    """Example showing step-by-step solving process."""
    
    print("=" * 60)
    print("FunCaptcha Solver - Step-by-Step Example")
    print("=" * 60)
    
    public_key = "YOUR_PUBLIC_KEY_HERE"
    service_url = "https://client-api.arkoselabs.com"
    page_url = "https://example.com"
    
    solver = FunCaptchaSolver(
        public_key=public_key,
        service_url=service_url,
        page_url=page_url
    )
    
    try:
        # Step 1: Get session token
        print("\n[STEP 1] Getting session token...")
        session_token = solver.get_session_token()
        print(f"[+] Session token obtained: {session_token[:50]}...")
        
        # Step 2: Get challenge
        print("\n[STEP 2] Fetching challenge...")
        challenge = solver.get_challenge()
        print(f"[+] Challenge received")
        print(f"    Game Type: {solver.game_type}")
        
        # Step 3: Solve (automatic)
        print("\n[STEP 3] Solving challenge automatically...")
        solution = solver.solve()
        
        print(f"\n[+] COMPLETE! Solution: {solution}")
        return solution
        
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        return None


def display_help():
    """Display help information."""
    help_text = """
FunCaptcha Solver - Usage Examples

This script demonstrates different ways to use the FunCaptcha solver.

Available Examples:
  1. Basic usage - Simple solve operation
  2. Proxy usage - Solving through a proxy server
  3. Step-by-step - Detailed solving process

Configuration Required:
  - public_key: The FunCaptcha public key from target website
  - service_url: FunCaptcha API endpoint (usually https://client-api.arkoselabs.com)
  - page_url: URL of the page containing the captcha

Usage:
  python example.py [example_number]
  
  Examples:
    python example.py 1    # Run basic usage example
    python example.py 2    # Run proxy usage example
    python example.py 3    # Run step-by-step example
    
Note: Replace placeholder values (YOUR_PUBLIC_KEY_HERE, etc.) with actual values
before running the examples.
"""
    print(help_text)


def main():
    """Main function to run examples."""
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        if example_num == "1":
            example_basic_usage()
        elif example_num == "2":
            example_with_proxy()
        elif example_num == "3":
            example_step_by_step()
        else:
            print(f"Unknown example number: {example_num}")
            display_help()
    else:
        # Default: run basic usage
        print("Running basic usage example (use 'python example.py help' for more options)\n")
        example_basic_usage()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        display_help()
    else:
        main()
