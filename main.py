#!/usr/bin/env python3
"""
Roblox Group Auto-Joiner
Automatically joins Roblox groups using account cookies and the Roblox API
"""

import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class RobloxGroupJoiner:
    """Main class for joining Roblox groups"""
    
    def __init__(self, group_id: int, cookies: List[str], proxies: Optional[List[str]] = None):
        self.group_id = group_id
        self.cookies = cookies
        self.proxies = proxies if proxies else []
        self.success_count = 0
        self.fail_count = 0
        
        # Roblox API endpoints
        self.group_join_url = f"https://groups.roblox.com/v1/groups/{group_id}/users"
        self.user_info_url = "https://users.roblox.com/v1/users/authenticated"
        
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Get a random proxy from the list"""
        if not self.proxies:
            return None
        
        proxy = random.choice(self.proxies)
        return {
            'http': proxy,
            'https': proxy
        }
    
    def get_csrf_token(self, cookie: str, max_retries: int = 5) -> Optional[str]:
        """Get CSRF token from Roblox with retry logic"""
        for attempt in range(max_retries):
            # Use proxy for first 3 attempts, then try without proxy
            proxy = self.get_proxy() if (attempt < 3 and self.proxies) else None
            
            try:
                headers = {
                    'Cookie': f'.ROBLOSECURITY={cookie}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.roblox.com/',
                    'Origin': 'https://www.roblox.com'
                }
                
                response = requests.post(
                    self.group_join_url,
                    headers=headers,
                    json={},  # Empty JSON body
                    proxies=proxy,
                    timeout=20
                )
                
                # CSRF token is returned in the response header when we make a POST without it
                if 'x-csrf-token' in response.headers:
                    return response.headers['x-csrf-token']
                
                # If we didn't get a token, retry
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                    
                return None
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    # Retry with different proxy
                    time.sleep(0.3)
                    continue
                else:
                    # Last attempt failed
                    return None
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.3)
                    continue
                return None
        
        return None
    
    def get_user_info(self, cookie: str, max_retries: int = 5) -> Optional[Dict]:
        """Get authenticated user information with retry logic"""
        for attempt in range(max_retries):
            # Use proxy for first 3 attempts, then try without proxy
            proxy = self.get_proxy() if (attempt < 3 and self.proxies) else None
            
            try:
                headers = {
                    'Cookie': f'.ROBLOSECURITY={cookie}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(
                    self.user_info_url,
                    headers=headers,
                    proxies=proxy,
                    timeout=20
                )
                
                if response.status_code == 200:
                    return response.json()
                
                # If not successful, retry
                if attempt < max_retries - 1:
                    time.sleep(0.3)
                    continue
                    
                return None
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    # Retry with different proxy
                    time.sleep(0.3)
                    continue
                else:
                    # Last attempt failed, return None silently
                    return None
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.3)
                    continue
                return None
        
        return None
    
    def join_group(self, cookie: str, username: str = "Unknown") -> bool:
        """Join a Roblox group using cookie with retry logic"""
        max_retries = 5
        
        # Get CSRF token with retry
        print(f"{Colors.CYAN}[{username}] Getting CSRF token...{Colors.RESET}")
        csrf_token = self.get_csrf_token(cookie, max_retries)
        
        if not csrf_token:
            print(f"{Colors.RED}[{username}] Failed to get CSRF token{Colors.RESET}")
            return False
        
        # Try to join group with retry logic
        for attempt in range(max_retries):
            # Use proxy for first 3 attempts, then try without proxy
            proxy = self.get_proxy() if (attempt < 3 and self.proxies) else None
            
            try:
                # Prepare headers with CSRF token
                headers = {
                    'Cookie': f'.ROBLOSECURITY={cookie}',
                    'X-CSRF-TOKEN': csrf_token,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': f'https://www.roblox.com/groups/{self.group_id}',
                    'Origin': 'https://www.roblox.com'
                }
                
                # Join the group with empty body
                if attempt == 0:
                    print(f"{Colors.YELLOW}[{username}] Joining group {self.group_id}...{Colors.RESET}")
                elif attempt >= 3:
                    print(f"{Colors.YELLOW}[{username}] Retrying without proxy (attempt {attempt + 1}/{max_retries})...{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}[{username}] Retrying (attempt {attempt + 1}/{max_retries})...{Colors.RESET}")
                
                response = requests.post(
                    self.group_join_url,
                    headers=headers,
                    json={},  # Empty JSON body
                    proxies=proxy,
                    timeout=20
                )
                
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[{username}] ✓ Successfully joined group {self.group_id}!{Colors.RESET}")
                    return True
                elif response.status_code == 400:
                    # User might already be in the group
                    try:
                        error_data = response.json()
                        if 'errors' in error_data:
                            error_msg = error_data['errors'][0].get('message', 'Unknown error')
                            if 'already' in error_msg.lower() or 'member' in error_msg.lower():
                                print(f"{Colors.YELLOW}[{username}] Already in group{Colors.RESET}")
                                return True
                            elif 'captcha' in error_msg.lower():
                                print(f"{Colors.RED}[{username}] Captcha required - try with fewer threads{Colors.RESET}")
                                return False
                            print(f"{Colors.RED}[{username}] Error: {error_msg}{Colors.RESET}")
                    except:
                        pass
                    return False
                elif response.status_code == 401:
                    print(f"{Colors.RED}[{username}] Invalid cookie - unauthorized{Colors.RESET}")
                    return False
                elif response.status_code == 403:
                    # Could be CSRF token issue or banned
                    if attempt < max_retries - 1:
                        # Try to get new CSRF token
                        time.sleep(1)
                        csrf_token = self.get_csrf_token(cookie, 2)
                        if csrf_token:
                            continue
                    print(f"{Colors.RED}[{username}] Access forbidden (403){Colors.RESET}")
                    return False
                else:
                    # Retry on other status codes
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    print(f"{Colors.RED}[{username}] Failed with status code: {response.status_code}{Colors.RESET}")
                    return False
                    
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    # Retry with different settings
                    time.sleep(0.5)
                    continue
                else:
                    # Last attempt failed
                    print(f"{Colors.RED}[{username}] Connection failed{Colors.RESET}")
                    return False
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                print(f"{Colors.RED}[{username}] Error: {str(e)[:80]}{Colors.RESET}")
                return False
        
        return False
    
    def process_account(self, cookie: str, index: int) -> bool:
        """Process a single account"""
        # Get user info first (with retry logic built in)
        user_info = self.get_user_info(cookie)
        
        if user_info:
            username = user_info.get('name', f'Account_{index}')
            user_id = user_info.get('id', 'Unknown')
            print(f"{Colors.BLUE}[INFO] Processing: {username} (ID: {user_id}){Colors.RESET}")
        else:
            username = f'Account_{index}'
            print(f"{Colors.YELLOW}[WARN] Could not get user info, using {username}{Colors.RESET}")
        
        # Join the group (with retry logic built in)
        success = self.join_group(cookie, username)
        
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        
        return success
    
    def run(self, threads: int = 5):
        """Run the group joiner with multiple threads"""
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}Roblox Group Auto-Joiner{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}Group ID: {self.group_id}{Colors.RESET}")
        print(f"{Colors.GREEN}Total Accounts: {len(self.cookies)}{Colors.RESET}")
        print(f"{Colors.GREEN}Threads: {threads}{Colors.RESET}")
        print(f"{Colors.GREEN}Proxies Loaded: {len(self.proxies)}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        start_time = time.time()
        
        # Process accounts with thread pool
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.process_account, cookie, i+1): i 
                for i, cookie in enumerate(self.cookies)
            }
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"{Colors.RED}[ERROR] Thread exception: {e}{Colors.RESET}")
        
        # Print summary
        elapsed = time.time() - start_time
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}SUMMARY{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Success: {self.success_count}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed: {self.fail_count}{Colors.RESET}")
        print(f"{Colors.YELLOW}Total Processed: {len(self.cookies)}{Colors.RESET}")
        print(f"{Colors.CYAN}Time Elapsed: {elapsed:.2f} seconds{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")

def load_cookies(filename: str = 'accounts.txt') -> List[str]:
    """Load cookies from file"""
    try:
        with open(filename, 'r') as f:
            cookies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return cookies
    except FileNotFoundError:
        print(f"{Colors.RED}[ERROR] {filename} not found!{Colors.RESET}")
        print(f"{Colors.YELLOW}[INFO] Please add your .ROBLOSECURITY cookies to {filename} (one per line){Colors.RESET}")
        return []

def load_proxies(filename: str = 'proxies.txt') -> List[str]:
    """Load proxies from file"""
    try:
        with open(filename, 'r') as f:
            proxies = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Handle different proxy formats
                if line.startswith('http://') or line.startswith('https://') or line.startswith('socks5://'):
                    proxies.append(line)
                elif '@' in line and ':' in line:
                    # Format: IP:PORT@USER:PASS -> socks5://USER:PASS@IP:PORT
                    parts = line.split('@')
                    if len(parts) == 2:
                        ip_port = parts[0]
                        user_pass = parts[1]
                        proxies.append(f'socks5://{user_pass}@{ip_port}')
                else:
                    # Assume http proxy
                    proxies.append(f'http://{line}')
            
            return proxies
    except FileNotFoundError:
        print(f"{Colors.YELLOW}[WARN] {filename} not found, running without proxies{Colors.RESET}")
        return []

def main():
    """Main function"""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║           Roblox Group Auto-Joiner v1.0                         ║")
    print("║           Fast group joining using Roblox API                   ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    # Get group ID from user
    try:
        group_id = int(input(f"{Colors.CYAN}Enter Roblox Group ID: {Colors.RESET}"))
    except ValueError:
        print(f"{Colors.RED}[ERROR] Invalid group ID!{Colors.RESET}")
        return
    
    # Get number of threads
    try:
        threads = int(input(f"{Colors.CYAN}Enter number of threads (default 5): {Colors.RESET}") or "5")
    except ValueError:
        threads = 5
    
    # Load cookies from accounts.txt
    print(f"\n{Colors.YELLOW}[INFO] Loading account cookies from 'accounts.txt'...{Colors.RESET}")
    cookies = load_cookies('accounts.txt')
    
    if not cookies:
        print(f"{Colors.RED}[ERROR] No cookies loaded!{Colors.RESET}")
        print(f"{Colors.YELLOW}[INFO] Create an 'accounts.txt' file with one .ROBLOSECURITY cookie per line{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}[SUCCESS] Loaded {len(cookies)} cookies{Colors.RESET}")
    
    # Load proxies from proxies.txt
    print(f"{Colors.YELLOW}[INFO] Loading proxies from 'proxies.txt'...{Colors.RESET}")
    proxies = load_proxies('proxies.txt')
    
    if proxies:
        print(f"{Colors.GREEN}[SUCCESS] Loaded {len(proxies)} proxies{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}[WARN] No proxies loaded, using direct connection{Colors.RESET}")
    
    # Create joiner and run
    joiner = RobloxGroupJoiner(group_id, cookies, proxies)
    joiner.run(threads)
    
    input(f"\n{Colors.CYAN}Press Enter to exit...{Colors.RESET}")

if __name__ == "__main__":
    main()
