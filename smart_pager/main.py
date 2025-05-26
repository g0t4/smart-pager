"""Main entry point for Smart Pager."""

import sys
from pathlib import Path

from rich.console import Console
from rich.live import Live

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
    
    # Create pager
    pager = SmartPager(filename)
    console = Console()
    
    try:
        with Live(pager.render(), refresh_per_second=4, screen=True, console=console) as live:
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
                        elif key == 'k' or key == '\x1b[A':  # k or up arrow  
                            pager.move_up()
                        elif key == 'g':
                            # Handle 'gg' for top - wait for second 'g'
                            next_key = input_handler.get_key(timeout=0.5)
                            if next_key == 'g':
                                pager.move_to_top()
                        elif key.upper() == 'G':
                            pager.move_to_bottom()
                        elif key == '\x04':  # Ctrl+D
                            pager.page_down()
                        elif key == '\x15':  # Ctrl+U
                            pager.page_up()
                        elif key in ['\n', '\r', ' ']:  # Enter or Space
                            pager.toggle_expansion()
                        
                        # Update display
                        live.update(pager.render())
                        
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        # Handle any other errors gracefully
                        continue
                        
    except Exception as e:
        console = Console()
        console.print(f"Error: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
