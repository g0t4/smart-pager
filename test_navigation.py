#!/usr/bin/env python3
"""Test navigation rendering."""

import sys
sys.path.insert(0, '.')

from smart_pager.pager import SmartPager
from rich.console import Console

def test_navigation():
    """Test navigation and rendering."""
    pager = SmartPager('examples/sample_logs.txt')
    console = Console()
    
    print("=== Initial State ===")
    console.print(pager.render())
    
    print("\n=== After moving down 2 lines ===")
    pager.move_down()
    pager.move_down()
    console.print(pager.render())
    
    print("\n=== After expanding JSON ===")
    # Find a JSON line and expand it
    for i in range(len(pager.lines)):
        is_json, _ = pager._is_json_line(pager.lines[i])
        if is_json:
            pager.current_line = i
            pager.toggle_expansion()
            break
    
    console.print(pager.render())

if __name__ == '__main__':
    test_navigation()
