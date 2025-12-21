"""
Utility Module
Helper functions for configuration and proxy management.
"""

import json
import os
from typing import Dict, List, Optional


class Util:
    """Utility functions for the account generator."""
    
    @staticmethod
    def get_config() -> Dict:
        """
        Load configuration from config.json.
        
        Returns:
            Configuration dictionary with default values
        """
        config_file = "config.json"
        
        # Default configuration
        default_config = {
            "threads": 5,
            "delay": 3,
            "proxy_file": "proxies.txt",
            "output_file": "accounts.txt",
            "use_proxies": True,
            "debug": True
        }
        
        # Load from file if exists
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"[!] Error loading config: {e}")
        else:
            # Create default config file
            Util.save_config(default_config)
        
        return default_config
    
    @staticmethod
    def save_config(config: Dict) -> None:
        """
        Save configuration to config.json.
        
        Args:
            config: Configuration dictionary to save
        """
        config_file = "config.json"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"[!] Error saving config: {e}")
    
    @staticmethod
    def load_proxies(proxy_file: str = "proxies.txt") -> List[str]:
        """
        Load proxies from file.
        
        Args:
            proxy_file: Path to proxy file
            
        Returns:
            List of valid proxy URLs (filtered and converted)
        """
        proxies = []
        
        if os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            # Try to convert alternate format first
                            converted = Util.convert_proxy_format(line)
                            
                            # Validate proxy format before adding
                            if Util.validate_proxy(converted):
                                proxies.append(converted)
                            else:
                                print(f"[!] Skipping invalid proxy: {line}")
            except Exception as e:
                print(f"[!] Error loading proxies: {e}")
        
        return proxies
    
    @staticmethod
    def convert_proxy_format(proxy: str) -> str:
        """
        Convert alternate proxy format to standard format.
        
        Supports conversion from:
        - IP:PORT@USERNAME:PASSWORD  →  socks5://USERNAME:PASSWORD@IP:PORT
        - IP:PORT                     →  socks5://IP:PORT
        
        Args:
            proxy: Proxy string (any format)
            
        Returns:
            Converted proxy string in standard format
        """
        if not proxy or not isinstance(proxy, str):
            return proxy
        
        # If already has protocol, return as-is
        valid_prefixes = ['http://', 'https://', 'socks5://', 'socks4://']
        if any(proxy.startswith(prefix) for prefix in valid_prefixes):
            return proxy
        
        # Check for alternate format: IP:PORT@USERNAME:PASSWORD
        if '@' in proxy:
            parts = proxy.split('@')
            if len(parts) == 2:
                # parts[0] = IP:PORT
                # parts[1] = USERNAME:PASSWORD
                ip_port = parts[0]
                user_pass = parts[1]
                
                # Convert to: socks5://USERNAME:PASSWORD@IP:PORT
                return f"socks5://{user_pass}@{ip_port}"
        
        # If no @ but has :, assume it's IP:PORT format
        if ':' in proxy and not proxy.startswith('//'):
            # Convert to: socks5://IP:PORT
            return f"socks5://{proxy}"
        
        # Return as-is if no conversion needed
        return proxy
    
    @staticmethod
    def validate_proxy(proxy: str) -> bool:
        """
        Validate proxy format.
        
        Args:
            proxy: Proxy string to validate
            
        Returns:
            True if valid
        """
        if not proxy or not isinstance(proxy, str):
            return False
        
        valid_prefixes = ['http://', 'https://', 'socks5://', 'socks4://']
        
        if not any(proxy.startswith(prefix) for prefix in valid_prefixes):
            return False
        
        if ':' not in proxy.split('://')[-1]:
            return False
        
        return True
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """
        Format seconds as HH:MM:SS.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
