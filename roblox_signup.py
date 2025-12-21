#!/usr/bin/env python3
"""
Roblox Account Creator with FunCaptcha Solver
Automatically creates Roblox accounts by solving FunCaptcha challenges.
Enhanced with comprehensive error handling and debugging.
"""

import requests
import json
import time
import random
import string
from datetime import datetime
from typing import Dict, Optional, Tuple
from funcaptcha_solver import FunCaptchaSolver


class RobloxAccountCreator:
    """Automates Roblox account creation with FunCaptcha solving and error handling."""
    
    # Roblox API endpoints
    SIGNUP_URL = "https://auth.roblox.com/v2/signup"
    USERNAME_VALIDATION_URL = "https://auth.roblox.com/v1/usernames/validate"
    FUNCAPTCHA_URL = "https://client-api.arkoselabs.com"
    
    # Roblox FunCaptcha public key
    ROBLOX_PUBLIC_KEY = "476068BF-9607-4799-B53D-966BE98E2B81"
    
    def __init__(self, proxy: Optional[str] = None, debug: bool = True):
        """
        Initialize the Roblox account creator.
        
        Args:
            proxy: Optional proxy server URL
            debug: Enable debug output
        """
        self.session = requests.Session()
        self.proxy = proxy
        self.debug = debug
        self.last_error = None
        self.csrf_token = None
        
        # Validate and set proxy
        if proxy:
            if not self._validate_proxy_format(proxy):
                self.last_error = "PROXY INVALID - Incorrect format"
                self._debug_print(f"ERROR: {self.last_error}")
                self.proxy = None
            else:
                self.session.proxies = {
                    'http': proxy,
                    'https': proxy
                }
                self._debug_print(f"Using proxy: {proxy}")
        
        # User agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
        })
    
    def _validate_proxy_format(self, proxy: str) -> bool:
        """
        Validate proxy format.
        
        Args:
            proxy: Proxy string to validate
            
        Returns:
            True if valid format
        """
        if not proxy or not isinstance(proxy, str):
            return False
        
        # Check for valid proxy format
        valid_prefixes = ['http://', 'https://', 'socks5://', 'socks4://']
        
        if not any(proxy.startswith(prefix) for prefix in valid_prefixes):
            return False
        
        # Basic validation - should contain : for port
        if ':' not in proxy.split('://')[-1]:
            return False
        
        return True
    
    def _debug_print(self, message: str):
        """Print debug message if debug mode is enabled."""
        if self.debug:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {message}")
    
    def get_csrf_token(self) -> bool:
        """
        Get CSRF token from Roblox.
        Required for all POST requests to Roblox API.
        
        Returns:
            True if token retrieved successfully
        """
        try:
            # First, visit Roblox homepage to establish session
            response = self.session.get("https://www.roblox.com/", timeout=10)
            
            # Trigger CSRF token by making a POST request
            # Roblox returns the token in the response header
            response = self.session.post(
                self.USERNAME_VALIDATION_URL,
                json={},
                timeout=10
            )
            
            # Extract CSRF token from response headers
            csrf_token = response.headers.get('x-csrf-token')
            
            if csrf_token:
                self.csrf_token = csrf_token
                self.session.headers['X-CSRF-TOKEN'] = csrf_token
                self._debug_print(f"CSRF token acquired")
                return True
            else:
                self._handle_error("CSRF ERROR", "Failed to get CSRF token")
                return False
                
        except Exception as e:
            self._handle_error("CSRF ERROR", f"Cannot retrieve CSRF token: {str(e)}")
            return False
    
    def _handle_error(self, error_type: str, details: str = "") -> None:
        """
        Handle and log errors without stopping execution.
        
        Args:
            error_type: Type of error (e.g., "PROXY", "CAPTCHA", "API")
            details: Additional error details
        """
        self.last_error = f"{error_type}: {details}" if details else error_type
        self._debug_print(f"ERROR: {self.last_error}")
    
    def generate_username(self) -> str:
        """
        Generate a random username for Roblox.
        
        Returns:
            Random username string
        """
        # Roblox usernames: 3-20 characters, alphanumeric + underscore
        # Common patterns for usernames
        patterns = [
            lambda: f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 12)))}_{random.randint(100, 9999)}",
            lambda: f"User_{''.join(random.choices(string.ascii_letters, k=random.randint(4, 8)))}_{random.randint(10, 999)}",
            lambda: f"{''.join(random.choices(string.ascii_letters, k=1)).upper()}{''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))}_{random.randint(1000, 9999)}",
            lambda: f"{''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 15)))}",
        ]
        
        username = random.choice(patterns)()
        
        # Ensure it meets Roblox requirements
        # Remove any invalid characters
        username = ''.join(c for c in username if c.isalnum() or c == '_')
        
        # Ensure length is within bounds
        if len(username) < 3:
            username = username + ''.join(random.choices(string.ascii_lowercase, k=3 - len(username)))
        elif len(username) > 20:
            username = username[:20]
        
        return username
    
    def generate_password(self) -> str:
        """
        Generate a secure random password for Roblox.
        
        Returns:
            Random password string
        """
        # Roblox password requirements: at least 8 characters
        # Include uppercase, lowercase, numbers for security
        length = random.randint(12, 16)
        
        # Ensure password has variety
        password = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.ascii_lowercase) +
            random.choice(string.digits) +
            ''.join(random.choices(string.ascii_letters + string.digits, k=length - 3))
        )
        
        # Shuffle the password
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)
        
        return password
    
    def generate_birthday(self) -> Tuple[int, int, int]:
        """
        Generate a random birthday (must be 13+ for Roblox).
        
        Returns:
            Tuple of (day, month, year)
        """
        current_year = datetime.now().year
        
        # Generate age between 13 and 25
        age = random.randint(13, 25)
        year = current_year - age
        
        month = random.randint(1, 12)
        
        # Generate appropriate day for the month
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:  # February
            day = random.randint(1, 28)
        
        return day, month, year
    
    def validate_username(self, username: str) -> bool:
        """
        Check if a username is available on Roblox.
        
        Args:
            username: Username to validate
            
        Returns:
            True if username is available, False otherwise
        """
        try:
            # Ensure we have CSRF token
            if not self.csrf_token:
                if not self.get_csrf_token():
                    return False
            
            payload = {
                "username": username,
                "birthday": "2000-01-01T00:00:00.000Z",
                "context": "Signup"
            }
            
            response = self.session.post(
                self.USERNAME_VALIDATION_URL,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                is_valid = data.get('code') == 0  # 0 means username is valid
                return is_valid
            elif response.status_code == 403:
                # CSRF token might be invalid, refresh it
                self._debug_print("Got 403, refreshing CSRF token...")
                if self.get_csrf_token():
                    # Retry with new token
                    response = self.session.post(
                        self.USERNAME_VALIDATION_URL,
                        json=payload,
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return data.get('code') == 0
                
                self._handle_error("API ERROR", f"Username validation returned 403 (Access Denied)")
                return False
            elif response.status_code == 429:
                self._handle_error("RATE LIMITED", "Username validation")
                return False
            else:
                self._handle_error("API ERROR", f"Username validation returned {response.status_code}")
                return False
            
        except requests.exceptions.ProxyError as e:
            self._handle_error("PROXY ERROR", "Failed to connect through proxy")
            return False
        except requests.exceptions.Timeout:
            self._handle_error("TIMEOUT", "Username validation timed out")
            return False
        except requests.exceptions.ConnectionError:
            self._handle_error("CONNECTION ERROR", "Cannot reach Roblox servers")
            return False
        except Exception as e:
            self._handle_error("UNKNOWN ERROR", f"Username validation: {str(e)}")
            return False
    
    def get_funcaptcha_token(self) -> Optional[str]:
        """
        Solve FunCaptcha and get the token.
        
        Returns:
            FunCaptcha solution token or None on failure
        """
        try:
            solver = FunCaptchaSolver(
                public_key=self.ROBLOX_PUBLIC_KEY,
                service_url=self.FUNCAPTCHA_URL,
                page_url="https://www.roblox.com",
                proxy=self.proxy,
                debug=False  # Disable solver debug output for cleaner logs
            )
            
            token = solver.solve()
            
            if token:
                return token
            else:
                self._handle_error("CAPTCHA SOLVE FAILED", "Solver returned no token")
                return None
                
        except requests.exceptions.ProxyError:
            self._handle_error("PROXY ERROR", "FunCaptcha solver cannot connect through proxy")
            return None
        except requests.exceptions.Timeout:
            self._handle_error("TIMEOUT", "FunCaptcha solving timed out")
            return None
        except requests.exceptions.ConnectionError:
            self._handle_error("CONNECTION ERROR", "Cannot reach FunCaptcha servers")
            return None
        except Exception as e:
            self._handle_error("CAPTCHA ERROR", f"Solver failed: {str(e)}")
            return None
    
    def create_account(self, username: str, password: str, birthday: Tuple[int, int, int], 
                      captcha_token: str) -> Optional[Dict]:
        """
        Create a Roblox account.
        
        Args:
            username: Desired username
            password: Account password
            birthday: Tuple of (day, month, year)
            captcha_token: FunCaptcha solution token
            
        Returns:
            Dictionary containing account creation response or None on failure
        """
        day, month, year = birthday
        
        # Format birthday as ISO string
        birthday_str = f"{year}-{month:02d}-{day:02d}T00:00:00.000Z"
        
        payload = {
            "username": username,
            "password": password,
            "birthday": birthday_str,
            "gender": random.choice([2, 3]),  # 2 = Male, 3 = Female
            "isTosAgreementBoxChecked": True,
            "captchaToken": captcha_token,
            "captchaProvider": "PROVIDER_ARKOSE_LABS"
        }
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        try:
            response = self.session.post(
                self.SIGNUP_URL,
                json=payload,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                return {
                    'status_code': response.status_code,
                    'response': response.json(),
                    'cookies': self.session.cookies.get_dict()
                }
            elif response.status_code == 429:
                self._handle_error("RATE LIMITED", "Too many account creation requests")
                return None
            elif response.status_code == 400:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('errors', [{}])[0].get('message', 'Bad request')
                self._handle_error("INVALID REQUEST", error_msg)
                return None
            elif response.status_code == 403:
                self._handle_error("CAPTCHA REJECTED", "FunCaptcha token was invalid or expired")
                return None
            else:
                self._handle_error("API ERROR", f"Account creation returned {response.status_code}")
                return None
                
        except requests.exceptions.ProxyError:
            self._handle_error("PROXY ERROR", "Failed to connect through proxy")
            return None
        except requests.exceptions.Timeout:
            self._handle_error("TIMEOUT", "Account creation timed out")
            return None
        except requests.exceptions.ConnectionError:
            self._handle_error("CONNECTION ERROR", "Cannot reach Roblox servers")
            return None
        except Exception as e:
            self._handle_error("UNKNOWN ERROR", f"Account creation: {str(e)}")
            return None
    
    def save_account(self, username: str, password: str, cookies: Dict, filename: str = "accounts.txt"):
        """
        Save account information to a file.
        
        Args:
            username: Account username
            password: Account password
            cookies: Session cookies dictionary
            filename: Output filename
        """
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write(f"COOKIES: {json.dumps(cookies, indent=2)}\n")
                f.write(f"\n")
            
            self._debug_print(f'Account saved to {filename}')
            
        except Exception as e:
            self._handle_error("FILE ERROR", f"Cannot save account: {str(e)}")
    
    def create_random_account(self) -> Optional[Dict]:
        """
        Create a random Roblox account with all automated steps.
        Continues on errors, returning detailed error information.
        
        Returns:
            Dictionary with account info if successful, None otherwise
        """
        self.last_error = None
        
        # Generate credentials
        username = self.generate_username()
        password = self.generate_password()
        birthday = self.generate_birthday()
        
        self._debug_print(f'Generating {username}')
        
        # Validate username
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            if self.validate_username(username):
                break
            else:
                if self.last_error and ("RATE LIMITED" in self.last_error or "CONNECTION ERROR" in self.last_error):
                    # Don't retry on rate limit or connection errors
                    return None
                
                username = self.generate_username()
                attempt += 1
        
        if attempt >= max_attempts:
            self._handle_error("USERNAME ERROR", "Failed to find available username after 5 attempts")
            return None
        
        # Solve FunCaptcha
        self._debug_print('Solving Captcha...')
        captcha_token = self.get_funcaptcha_token()
        
        if not captcha_token:
            # Error already logged in get_funcaptcha_token
            return None
        
        # Create account
        result = self.create_account(username, password, birthday, captcha_token)
        
        if result and result['status_code'] == 200:
            self._debug_print('[SUCCESS]')
            
            account_info = {
                'username': username,
                'password': password,
                'cookies': result['cookies'],
                'created_at': datetime.now().isoformat()
            }
            
            # Save to file
            self.save_account(username, password, result['cookies'])
            
            return account_info
        else:
            # Error already logged in create_account
            return None


def create_multiple_accounts(count: int, proxy: Optional[str] = None, delay: int = 5):
    """
    Create multiple Roblox accounts.
    
    Args:
        count: Number of accounts to create
        proxy: Optional proxy server
        delay: Delay between account creations (seconds)
    """
    creator = RobloxAccountCreator(proxy=proxy)
    
    successful = 0
    failed = 0
    
    print(f'\n[*] Starting creation of {count} accounts...\n')
    
    for i in range(count):
        print(f'\n[*] Creating account {i + 1}/{count}...')
        
        result = creator.create_random_account()
        
        if result:
            successful += 1
            print(f'[+] Progress: {successful} successful, {failed} failed')
        else:
            failed += 1
            print(f'[!] Progress: {successful} successful, {failed} failed')
        
        # Delay between creations
        if i < count - 1:
            print(f'\n[*] Waiting {delay} seconds before next account...')
            time.sleep(delay)
    
    print('\n' + '=' * 60)
    print('SUMMARY')
    print('=' * 60)
    print(f'Total Attempted: {count}')
    print(f'Successful: {successful}')
    print(f'Failed: {failed}')
    print(f'Success Rate: {(successful/count)*100:.1f}%')
    print('=' * 60)


def main():
    """Main function."""
    import sys
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║      ROBLOX ACCOUNT CREATOR WITH FUNCAPTCHA SOLVER     ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Parse arguments
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print('[!] Invalid count. Usage: python roblox_signup.py [count] [proxy]')
            return
    else:
        count = 1
    
    proxy = sys.argv[2] if len(sys.argv) > 2 else None
    
    if proxy:
        print(f'[*] Using proxy: {proxy}')
    
    # Create accounts
    create_multiple_accounts(count, proxy=proxy, delay=5)


if __name__ == '__main__':
    main()
