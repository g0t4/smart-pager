"""Input handling utilities."""

import sys
import select
import termios
import tty


class InputHandler:
    """Handle terminal input in a cross-platform way."""
    
    def __init__(self):
        self.old_settings = None
        
    def __enter__(self):
        """Enter raw mode."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit raw mode."""
        if self.old_settings:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)
    
    def get_key(self, timeout=None):
        """Get a key with optional timeout."""
        if timeout is not None:
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if not ready:
                return None
        
        key = sys.stdin.read(1)
        
        # Handle escape sequences
        if key == '\x1b':
            # Try to read more characters for escape sequences
            try:
                if timeout is not None:
                    ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if ready:
                        key += sys.stdin.read(1)
                        ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if ready:
                            key += sys.stdin.read(1)
                else:
                    key += sys.stdin.read(2)
            except:
                pass
        
        return key
