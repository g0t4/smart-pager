#!/usr/bin/env python3
"""Test rendering without input loop."""

import sys
sys.path.insert(0, '.')

from smart_pager.pager import SmartPager
from rich.console import Console

def test_render():
    """Test rendering."""
    pager = SmartPager('examples/sample_logs.txt')
    console = Console()
    
    # Print the layout to see how it looks
    console.print(pager.render())
    
    print("\n" + "="*50)
    print("Testing JSON expansion...")
    
    # Find first JSON line and expand it
    for i, line in enumerate(pager.lines):
        is_json, _ = pager._is_json_line(line)
        if is_json:
            pager.current_line = i
            pager.toggle_expansion()
            print(f"Expanded line {i+1}")
            break
    
    console.print(pager.render())

if __name__ == '__main__':
    test_render()
