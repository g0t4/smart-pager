"""Simplified main entry point for debugging."""

import sys
from pathlib import Path

from .pager import SmartPager
from .simple_renderer import SimpleRenderer
from .input_handler import InputHandler


def main():
    """Simplified main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python -m smart_pager.main_simple <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not Path(filename).exists():
        print(f"File not found: {filename}")
        sys.exit(1)
    
    # Create pager and renderer
    pager = SmartPager(filename)
    renderer = SimpleRenderer(pager)
    
    try:
        # Enter alternate screen
        print("\x1b[?1049h", end="")
        
        def refresh_display():
            """Refresh the display."""
            print("\x1b[2J\x1b[H", end="")  # Clear and home
            print(renderer.render_simple())
        
        # Initial display
        refresh_display()
        
        with InputHandler() as input_handler:
            while True:
                try:
                    key = input_handler.get_key(timeout=0.1)
                    
                    if key is None:
                        continue
                        
                    # Handle vim-like navigation
                    if key.lower() == 'q' or key == '\x03':  # q or Ctrl+C
                        break
                    elif key == 'j' or key == '\x1b[B':  # j or down arrow
                        pager.move_down()
                        refresh_display()
                    elif key == 'k' or key == '\x1b[A':  # k or up arrow  
                        pager.move_up()
                        refresh_display()
                    elif key == 'g':
                        # Handle 'gg' for top - wait for second 'g'
                        next_key = input_handler.get_key(timeout=0.5)
                        if next_key == 'g':
                            pager.move_to_top()
                            refresh_display()
                    elif key.upper() == 'G':
                        pager.move_to_bottom()
                        refresh_display()
                    elif key == '\x04':  # Ctrl+D
                        pager.page_down()
                        refresh_display()
                    elif key == '\x15':  # Ctrl+U
                        pager.page_up()
                        refresh_display()
                    elif key in ['\n', '\r', ' ']:  # Enter or Space
                        pager.toggle_expansion()
                        refresh_display()
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"\x1b[2J\x1b[H", end="")
                    print(f"Error: {e}")
                    refresh_display()
                    
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        # Always restore normal screen
        print("\x1b[?1049l", end="")


if __name__ == "__main__":
    main()
