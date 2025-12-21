"""
Improved Roblox Account Creator
Based on proven working reference implementation.
Uses exact API flow with proper CSRF, auth intent, and challenge handling.
"""

import requests
import json
import time
from base64 import b64encode, b64decode
from datetime import datetime
from typing import Dict, Optional, Tuple
from roblox_profile import RobloxProfile
from auth_intent import AuthIntent
from output_logger import Output


class ImprovedRobloxCreator:
    """
    Roblox account creator using proven API flow.
    Based on reference implementation with working signup process.
    """
    
    def __init__(self, proxy: Optional[str] = None, debug: bool = True):
        """
        Initialize creator with optional proxy.
        
        Args:
            proxy: Proxy URL (e.g., http://user:pass@host:port)
            debug: Enable debug logging
        """
        self.session = requests.Session()
        self.proxy = proxy
        self.debug = debug
        self.last_error = None
        
        # Set proxy if provided
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        # Initialize headers (will be updated during flow)
        self.session.headers = self._get_initial_headers()
    
    def _get_initial_headers(self) -> Dict:
        """Get initial headers for page requests."""
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Google Chrome";v="120", "Not?A_Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def _set_api_headers(self):
        """Update headers for API requests."""
        self.session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.roblox.com',
            'referer': 'https://www.roblox.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        })
        # Remove page-specific headers
        self.session.headers.pop('upgrade-insecure-requests', None)
        self.session.headers.pop('sec-fetch-user', None)
    
    def _log(self, level: str, message: str):
        """Log message using Output logger."""
        if self.debug:
            Output(level).log(message)
    
    def create_account(self) -> Optional[Dict]:
        """
        Create a Roblox account using the proven API flow.
        
        Returns:
            Account info dict if successful, None otherwise
        """
        try:
            # Generate credentials
            username = RobloxProfile.get_username()
            password = RobloxProfile.get_password()
            birthday = RobloxProfile.get_birth_day()
            
            self._log("INFO", f"Generating {username}")
            
            # Step 1: Visit Roblox homepage to get session
            resp = self.session.get("https://www.roblox.com/", timeout=15)
            
            if resp.status_code == 429:
                self._log("ERROR", "Rate limited")
                self.last_error = "RATE LIMITED"
                return None
            
            # Extract CSRF token from page
            if 'data-token="' in resp.text:
                csrf_token = resp.text.split('data-token="')[1].split('"')[0]
                self.session.headers['x-csrf-token'] = csrf_token
                self._log("CAPTCHA", "CSRF token acquired")
            else:
                self._log("ERROR", "Could not extract CSRF token")
                self.last_error = "CSRF ERROR"
                return None
            
            # Step 2: Update headers for API requests
            self._set_api_headers()
            
            # Step 3: Validate username
            payload = {
                'username': username,
                'context': 'Signup',
                'birthday': birthday,
            }
            
            resp = self.session.post(
                "https://auth.roblox.com/v1/usernames/validate",
                json=payload,
                timeout=15
            )
            
            if resp.status_code == 429:
                self._log("ERROR", "Rate limited on username validation")
                self.last_error = "RATE LIMITED"
                return None
            
            # Keep trying new usernames until we find one available
            max_attempts = 5
            attempt = 0
            
            while resp.status_code != 200 or resp.json().get("code") != 0:
                if attempt >= max_attempts:
                    self._log("ERROR", "Failed to find available username after 5 attempts")
                    self.last_error = "USERNAME ERROR"
                    return None
                
                username = RobloxProfile.get_username()
                payload["username"] = username
                
                resp = self.session.post(
                    "https://auth.roblox.com/v1/usernames/validate",
                    json=payload,
                    timeout=15
                )
                
                # Update CSRF if provided
                csrf = resp.headers.get("x-csrf-token")
                if csrf:
                    self.session.headers['x-csrf-token'] = csrf
                
                if resp.status_code == 429:
                    self._log("ERROR", "Rate limited")
                    self.last_error = "RATE LIMITED"
                    return None
                
                attempt += 1
            
            self._log("INFO", f"Username validated: {username}")
            
            # Step 4: Validate password
            password_payload = {
                'username': username,
                'password': password
            }
            
            self.session.post(
                "https://auth.roblox.com/v2/passwords/validate",
                json=password_payload,
                timeout=15
            )
            
            # Step 5: Get auth intent (ECDSA signature)
            auth_intent = AuthIntent.get_auth_intent(self.session)
            
            if not auth_intent:
                self._log("ERROR", "Failed to get auth intent")
                self.last_error = "AUTH INTENT ERROR"
                return None
            
            # Step 6: Prepare signup payload
            signup_payload = {
                'username': username,
                'password': password,
                'birthday': birthday,
                'gender': RobloxProfile.get_gender(),
                'isTosAgreementBoxChecked': True,
                'agreementIds': [
                    "306cc852-3717-4996-93e7-086daafd42f6",
                    "2ba6b930-4ba8-4085-9e8c-24b919701f15",
                ],
                'secureAuthenticationIntent': auth_intent
            }
            
            # Step 7: Initial signup (will return captcha challenge)
            resp = self.session.post(
                "https://auth.roblox.com/v2/signup",
                json=signup_payload,
                timeout=15
            )
            
            if resp.status_code == 429:
                self._log("ERROR", "Rate limited on signup")
                self.last_error = "RATE LIMITED"
                return None
            
            if resp.status_code != 200:
                # Should get challenge headers
                challenge_id = resp.headers.get("rblx-challenge-id")
                metadata_b64 = resp.headers.get("rblx-challenge-metadata")
                
                if not challenge_id or not metadata_b64:
                    self._log("ERROR", f"Signup failed: {resp.status_code}")
                    self.last_error = "API ERROR"
                    return None
                
                # Decode challenge metadata
                metadata = json.loads(b64decode(metadata_b64.encode("utf-8")).decode("utf-8"))
                blob = metadata.get("dataExchangeBlob")
                captcha_id = metadata.get("unifiedCaptchaId")
                
                # Step 8: Solve FunCaptcha
                self._log("CAPTCHA", "Solving Captcha...")
                
                # Use ML solver here
                from ml_captcha_solver import MLCaptchaSolver
                
                solver = MLCaptchaSolver(
                    session=self.session,
                    public_key="A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
                    page_url="https://www.roblox.com/",
                    blob=blob,
                    proxy=self.proxy,
                    debug=False
                )
                
                solution = solver.solve()
                
                if not solution:
                    self._log("ERROR", "Failed to solve captcha")
                    self.last_error = "CAPTCHA SOLVE FAILED"
                    return None
                
                self._log("CAPTCHA", "Captcha solved")
                
                # Step 9: Continue with captcha solution
                challenge_metadata = json.dumps({
                    "unifiedCaptchaId": captcha_id,
                    "captchaToken": solution,
                    "actionType": "Signup"
                }, separators=(',', ':'))
                
                continue_payload = json.dumps({
                    "challengeId": challenge_id,
                    "challengeType": "captcha",
                    "challengeMetadata": challenge_metadata
                }, separators=(',', ':'))
                
                resp = self.session.post(
                    "https://apis.roblox.com/challenge/v1/continue",
                    data=continue_payload.encode("utf-8"),
                    timeout=15
                )
                
                if resp.status_code != 200:
                    self._log("ERROR", f"Continue API rejected: {resp.status_code}")
                    self.last_error = "CAPTCHA REJECTED"
                    return None
                
                # Step 10: Add challenge headers for final signup
                self.session.headers.update({
                    "rblx-challenge-id": challenge_id,
                    "rblx-challenge-metadata": b64encode(challenge_metadata.encode("utf-8")).decode("utf-8"),
                    "rblx-challenge-type": "captcha"
                })
                
                # Step 11: Final signup with challenge headers
                resp = self.session.post(
                    "https://auth.roblox.com/v2/signup",
                    json=signup_payload,
                    timeout=15
                )
                
                if resp.status_code != 200:
                    self._log("ERROR", f"Final signup failed: {resp.status_code}")
                    self.last_error = "SIGNUP ERROR"
                    return None
            
            # Step 12: Complete registration
            self.session.headers = self._get_initial_headers()
            self.session.get("https://www.roblox.com/home?nu=true", timeout=15)
            
            # Get account cookie
            account_cookie = self.session.cookies.get('.ROBLOSECURITY', '')
            
            self._log("SUCCESS", f"Successfully created account | {username}")
            
            # Save account
            self._save_account(username, password, account_cookie)
            
            return {
                'username': username,
                'password': password,
                'cookie': account_cookie
            }
            
        except requests.exceptions.ProxyError:
            self._log("ERROR", "PROXY ERROR: Failed to connect through proxy")
            self.last_error = "PROXY ERROR"
            return None
        except requests.exceptions.Timeout:
            self._log("ERROR", "TIMEOUT: Request timed out")
            self.last_error = "TIMEOUT"
            return None
        except requests.exceptions.ConnectionError:
            self._log("ERROR", "CONNECTION ERROR: Cannot reach Roblox servers")
            self.last_error = "CONNECTION ERROR"
            return None
        except Exception as e:
            self._log("ERROR", f"Exception: {str(e)}")
            self.last_error = f"EXCEPTION: {type(e).__name__}"
            return None
    
    def _save_account(self, username: str, password: str, cookie: str):
        """Save account to file."""
        try:
            with open("accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write(f"COOKIES: {{'.ROBLOSECURITY': '{cookie}'}}\n")
                f.write(f"\n")
        except Exception as e:
            self._log("ERROR", f"Failed to save account: {str(e)}")
