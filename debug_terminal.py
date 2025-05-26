#!/usr/bin/env python3
"""Debug terminal sizing issues."""

import sys
sys.path.insert(0, '.')

from rich.console import Console
from smart_pager.pager import SmartPager

def debug_terminal():
    """Debug terminal and rendering."""
    console = Console()
    
    print("🔍 Terminal Debug Info")
    print(f"Console size: {console.size}")
    print(f"Width: {console.size.width}, Height: {console.size.height}")
    
    # Test pager initialization
    pager = SmartPager('examples/sample_logs.txt')
    print(f"Calculated terminal height: {pager.terminal_height}")
    print(f"File lines: {len(pager.lines)}")
    print(f"Current line: {pager.current_line}")
    print(f"Scroll offset: {pager.scroll_offset}")
    
    # Test visible lines calculation
    visible = pager._get_visible_lines()
    print(f"Visible lines: {len(visible)}")
    for i, (line_num, line) in enumerate(visible[:3]):
        print(f"  {line_num}: {line[:50]}...")
    
    print("\n" + "="*50)
    print("Testing single render (no Live)...")
    
    # Test rendering without Live
    layout = pager.render()
    console.print(layout)

if __name__ == '__main__':
    debug_terminal()
