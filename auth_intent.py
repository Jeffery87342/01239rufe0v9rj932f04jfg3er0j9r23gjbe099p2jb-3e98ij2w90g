#!/usr/bin/env python3
"""
Authentication Intent Module
Generates secure authentication signatures using ECDSA for Roblox signup.
"""

import requests
import time
from base64 import b64encode
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from typing import Optional, Dict


class AuthIntent:
    """Handles secure authentication intent generation for Roblox."""
    
    @staticmethod
    def string_to_bytes(raw_string: str) -> bytes:
        """Convert string to bytes."""
        return bytes(raw_string, 'utf-8')
    
    @staticmethod
    def export_public_key_as_spki(public_key) -> str:
        """
        Export public key in SPKI format.
        
        Args:
            public_key: EC public key object
            
        Returns:
            Base64-encoded SPKI public key
        """
        spki_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return b64encode(spki_bytes).decode('utf-8')
    
    @staticmethod
    def generate_signing_key_pair() -> tuple:
        """
        Generate ECDSA key pair using SECP256R1 curve.
        
        Returns:
            Tuple of (private_key, public_key)
        """
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def sign(private_key, data: bytes) -> str:
        """
        Sign data with private key using ECDSA-SHA256.
        
        Args:
            private_key: EC private key
            data: Data to sign
            
        Returns:
            Base64-encoded signature
        """
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return b64encode(signature).decode('utf-8')
    
    @staticmethod
    def get_auth_intent(session: requests.Session) -> Optional[Dict]:
        """
        Generate authentication intent for Roblox signup.
        
        Args:
            session: Requests session with proper headers and proxy
            
        Returns:
            Dictionary containing auth intent data or None on failure
        """
        try:
            # Generate key pair
            private_key, public_key = AuthIntent.generate_signing_key_pair()
            
            # Export public key
            client_public_key = AuthIntent.export_public_key_as_spki(public_key)
            
            # Get current timestamp
            client_epoch_timestamp = str(int(time.time()))
            
            # Get server nonce
            response = session.get(
                "https://apis.roblox.com/hba-service/v1/getServerNonce",
                timeout=10
            )
            
            if response.status_code != 200:
                return None
            
            server_nonce = response.text.strip('"')
            
            # Create payload for signing
            payload = f"{client_public_key}|{client_epoch_timestamp}|{server_nonce}"
            
            # Sign the payload
            sai_signature = AuthIntent.sign(
                private_key, 
                AuthIntent.string_to_bytes(payload)
            )
            
            # Return auth intent
            result = {
                "clientEpochTimestamp": client_epoch_timestamp,
                "clientPublicKey": client_public_key,
                "saiSignature": sai_signature,
                "serverNonce": server_nonce
            }
            
            return result
            
        except Exception as e:
            print(f"[!] Auth intent error: {e}")
            return None
