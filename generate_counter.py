"""
Account Generation Counter
Tracks statistics for account generation across threads.
"""

import threading
from datetime import datetime
from typing import Dict


class GenerateCounter:
    """Thread-safe counter for tracking account generation statistics."""
    
    def __init__(self):
        """Initialize the counter."""
        self._lock = threading.Lock()
        self._generated = 0
        self._failed = 0
        self._start_time = None
        self._errors = {}
        
    def start(self):
        """Start the timer."""
        self._start_time = datetime.now()
    
    def increment_generated(self):
        """Increment successful generation counter."""
        with self._lock:
            self._generated += 1
    
    def increment_failed(self, error_type: str = "UNKNOWN"):
        """
        Increment failed generation counter.
        
        Args:
            error_type: Type of error that occurred
        """
        with self._lock:
            self._failed += 1
            self._errors[error_type] = self._errors.get(error_type, 0) + 1
    
    def get_generated(self) -> int:
        """Get number of successfully generated accounts."""
        with self._lock:
            return self._generated
    
    def get_failed(self) -> int:
        """Get number of failed generation attempts."""
        with self._lock:
            return self._failed
    
    def get_total(self) -> int:
        """Get total number of attempts."""
        with self._lock:
            return self._generated + self._failed
    
    def get_success_rate(self) -> float:
        """Get success rate as percentage."""
        with self._lock:
            total = self._generated + self._failed
            if total == 0:
                return 0.0
            return (self._generated / total) * 100
    
    def get_elapsed_seconds(self) -> int:
        """Get elapsed time in seconds."""
        if self._start_time is None:
            return 0
        return int((datetime.now() - self._start_time).total_seconds())
    
    def get_cpm(self) -> int:
        """Get accounts per minute (CPM)."""
        elapsed = self.get_elapsed_seconds()
        if elapsed == 0:
            return 0
        
        with self._lock:
            return int((self._generated / elapsed) * 60)
    
    def get_errors(self) -> Dict[str, int]:
        """Get error counts by type."""
        with self._lock:
            return self._errors.copy()
    
    def reset(self):
        """Reset all counters."""
        with self._lock:
            self._generated = 0
            self._failed = 0
            self._start_time = None
            self._errors = {}


# Global counter instance
generate_counter = GenerateCounter()
