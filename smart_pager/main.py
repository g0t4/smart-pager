"""Main entry point for Smart Pager."""

import sys
from pathlib import Path
import os

from rich.console import Console

from .pager import SmartPager
from .input_handler import InputHandler


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        console = Console()
        console.print("Usage: python -m smart_pager <filename>", style="red")
        console.print("   or: python smart_pager <filename>", style="red")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not Path(filename).exists():
        console = Console()
        console.print(f"File not found: {filename}", style="red")
        sys.exit(1)
    
    # Create pager and console
    pager = SmartPager(filename)
    console = Console()
    
    try:
        # Enter alternate screen
        console.print("\x1b[?1049h", end="")
        
        def refresh_display():
            """Refresh the display."""
            # Clear screen and move to top-left
            console.print("\x1b[2J\x1b[H", end="")
            console.print(pager.render())
        
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
                    # Show error and continue
                    console.print("\x1b[2J\x1b[H", end="")
                    console.print(f"[red]Error: {e}[/red]")
                    refresh_display()
                    
    except Exception as e:
        console.print(f"Fatal error: {e}", style="red")
    finally:
        # Always restore normal screen
        console.print("\x1b[?1049l", end="")


if __name__ == "__main__":
    main()
