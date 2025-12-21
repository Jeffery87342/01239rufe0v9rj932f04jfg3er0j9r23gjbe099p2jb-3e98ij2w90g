"""
Generate Module
Handles account generation logic with threading support.
"""

from roblox_signup import RobloxAccountCreator
from generate_counter import GenerateCounter
from typing import Optional
import random


class Generate:
    """Account generation handler with thread support."""
    
    @staticmethod
    def gen(counter: GenerateCounter, proxy: Optional[str] = None, stop_event=None) -> None:
        """
        Generate accounts in a loop until stopped.
        
        Args:
            counter: GenerateCounter instance for tracking
            proxy: Optional proxy to use
            stop_event: Threading event to signal stop
        """
        while True:
            # Check if we should stop
            if stop_event and stop_event.is_set():
                break
            
            try:
                # Create account creator with error handling and debug enabled
                creator = RobloxAccountCreator(proxy=proxy, debug=True)
                
                # Attempt to create account
                result = creator.create_random_account()
                
                if result:
                    # Success
                    counter.increment_generated()
                else:
                    # Failed - record error type
                    error_type = creator.last_error.split(':')[0] if creator.last_error else "UNKNOWN"
                    counter.increment_failed(error_type)
                
            except KeyboardInterrupt:
                # Allow clean exit
                break
            except Exception as e:
                # Catch any unexpected errors
                counter.increment_failed(f"EXCEPTION: {type(e).__name__}")
    
    @staticmethod
    def gen_with_target(counter: GenerateCounter, target: int, proxy: Optional[str] = None, stop_event=None) -> None:
        """
        Generate accounts until target is reached.
        
        Args:
            counter: GenerateCounter instance for tracking
            target: Number of successful accounts to generate
            proxy: Optional proxy to use
            stop_event: Threading event to signal stop
        """
        while counter.get_generated() < target:
            # Check if we should stop
            if stop_event and stop_event.is_set():
                break
            
            try:
                # Create account creator with error handling and debug enabled
                creator = RobloxAccountCreator(proxy=proxy, debug=True)
                
                # Attempt to create account
                result = creator.create_random_account()
                
                if result:
                    # Success
                    counter.increment_generated()
                else:
                    # Failed - record error type
                    error_type = creator.last_error.split(':')[0] if creator.last_error else "UNKNOWN"
                    counter.increment_failed(error_type)
                
            except KeyboardInterrupt:
                # Allow clean exit
                break
            except Exception as e:
                # Catch any unexpected errors
                counter.increment_failed(f"EXCEPTION: {type(e).__name__}")
