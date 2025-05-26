#!/usr/bin/env python3
"""Quick interactive test."""

import sys
sys.path.insert(0, '.')

from smart_pager.input_handler import InputHandler

def test_input():
    """Test input handling."""
    print("Press keys (q to quit):")
    
    try:
        with InputHandler() as handler:
            while True:
                key = handler.get_key(timeout=1.0)
                
                if key is None:
                    print(".", end="", flush=True)
                    continue
                    
                if key == 'q':
                    break
                    
                # Show key codes
                print(f"\nKey: '{key}' (codes: {[ord(c) for c in key]})")
                
                if key == 'j':
                    print("DOWN command")
                elif key == 'k':
                    print("UP command")
                elif key == '\x1b[B':
                    print("Arrow DOWN")
                elif key == '\x1b[A':
                    print("Arrow UP")
                    
    except KeyboardInterrupt:
        print("\nCaught interrupt")
    
    print("\nDone!")

if __name__ == '__main__':
    test_input()
