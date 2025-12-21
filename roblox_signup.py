#!/usr/bin/env python3
"""
Roblox Account Creator with FunCaptcha Solver
Automatically creates Roblox accounts by solving FunCaptcha challenges.
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
    """Automates Roblox account creation with FunCaptcha solving."""
    
    # Roblox API endpoints
    SIGNUP_URL = "https://auth.roblox.com/v2/signup"
    USERNAME_VALIDATION_URL = "https://auth.roblox.com/v1/usernames/validate"
    FUNCAPTCHA_URL = "https://client-api.arkoselabs.com"
    
    # Roblox FunCaptcha public key
    ROBLOX_PUBLIC_KEY = "476068BF-9607-4799-B53D-966BE98E2B81"
    
    def __init__(self, proxy: Optional[str] = None):
        """
        Initialize the Roblox account creator.
        
        Args:
            proxy: Optional proxy server URL
        """
        self.session = requests.Session()
        self.proxy = proxy
        
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        # User agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
        })
    
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
            payload = {
                "username": username,
                "birthday": "2000-01-01T00:00:00.000Z",
                "context": "Signup"
            }
            
            response = self.session.post(
                self.USERNAME_VALIDATION_URL,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('code') == 0  # 0 means username is valid
            
            return False
            
        except Exception as e:
            print(f'[!] Error validating username: {e}')
            return False
    
    def get_funcaptcha_token(self) -> str:
        """
        Solve FunCaptcha and get the token.
        
        Returns:
            FunCaptcha solution token
        """
        print('[+] Solving FunCaptcha...')
        
        solver = FunCaptchaSolver(
            public_key=self.ROBLOX_PUBLIC_KEY,
            service_url=self.FUNCAPTCHA_URL,
            page_url="https://www.roblox.com",
            proxy=self.proxy
        )
        
        try:
            token = solver.solve()
            print('[+] FunCaptcha solved successfully!')
            return token
        except Exception as e:
            print(f'[!] FunCaptcha solving failed: {e}')
            raise
    
    def create_account(self, username: str, password: str, birthday: Tuple[int, int, int], 
                      captcha_token: str) -> Dict:
        """
        Create a Roblox account.
        
        Args:
            username: Desired username
            password: Account password
            birthday: Tuple of (day, month, year)
            captcha_token: FunCaptcha solution token
            
        Returns:
            Dictionary containing account creation response
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
                timeout=30
            )
            
            return {
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text,
                'cookies': self.session.cookies.get_dict()
            }
            
        except Exception as e:
            print(f'[!] Error creating account: {e}')
            raise
    
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
                f.write(f"{'=' * 60}\n")
                f.write(f"Account Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'=' * 60}\n")
                f.write(f"User: {username}\n")
                f.write(f"Pass: {password}\n")
                f.write(f"COOKIES: {json.dumps(cookies, indent=2)}\n")
                f.write(f"{'=' * 60}\n\n")
            
            print(f'[+] Account saved to {filename}')
            
        except Exception as e:
            print(f'[!] Error saving account: {e}')
    
    def create_random_account(self) -> Optional[Dict]:
        """
        Create a random Roblox account with all automated steps.
        
        Returns:
            Dictionary with account info if successful, None otherwise
        """
        print('\n' + '=' * 60)
        print('ROBLOX ACCOUNT CREATOR')
        print('=' * 60)
        
        # Generate credentials
        print('\n[+] Generating random credentials...')
        username = self.generate_username()
        password = self.generate_password()
        birthday = self.generate_birthday()
        
        print(f'[+] Username: {username}')
        print(f'[+] Password: {password}')
        print(f'[+] Birthday: {birthday[1]:02d}/{birthday[0]:02d}/{birthday[2]}')
        
        # Validate username
        print('\n[+] Validating username...')
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            if self.validate_username(username):
                print(f'[+] Username "{username}" is available!')
                break
            else:
                print(f'[!] Username "{username}" is taken, generating new one...')
                username = self.generate_username()
                attempt += 1
        
        if attempt >= max_attempts:
            print('[!] Failed to find available username')
            return None
        
        # Solve FunCaptcha
        try:
            captcha_token = self.get_funcaptcha_token()
        except Exception as e:
            print(f'[!] Failed to solve FunCaptcha: {e}')
            return None
        
        # Create account
        print('\n[+] Creating account...')
        try:
            result = self.create_account(username, password, birthday, captcha_token)
            
            if result['status_code'] == 200:
                print('[+] Account created successfully!')
                
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
                print(f'[!] Account creation failed: {result["response"]}')
                return None
                
        except Exception as e:
            print(f'[!] Error during account creation: {e}')
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
