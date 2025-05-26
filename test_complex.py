#!/usr/bin/env python3
"""Test with complex log file."""

import sys
sys.path.insert(0, '.')

from smart_pager.pager import SmartPager
from rich.console import Console

def test_complex():
    """Test with complex log file."""
    pager = SmartPager('examples/complex_logs.txt')
    console = Console()
    
    print(f"Loaded {len(pager.lines)} lines")
    
    # Find and test different types of JSON
    json_count = 0
    invalid_json_count = 0
    
    for i, line in enumerate(pager.lines):
        is_json, parsed = pager._is_json_line(line)
        looks_like_json = pager._looks_like_json(line)
        
        if is_json:
            json_count += 1
            print(f"Line {i+1}: Valid JSON - {len(str(parsed))} chars")  
        elif looks_like_json:
            invalid_json_count += 1
            print(f"Line {i+1}: Invalid JSON detected")
    
    print(f"\nSummary: {json_count} valid JSON lines, {invalid_json_count} invalid JSON lines")
    
    # Test expansion of a complex JSON
    for i, line in enumerate(pager.lines):
        is_json, parsed = pager._is_json_line(line)
        if is_json and len(str(parsed)) > 200:  # Find a complex one
            pager.current_line = i
            pager.toggle_expansion()
            print(f"\n=== Expanded complex JSON from line {i+1} ===")
            console.print(pager.render())
            break

if __name__ == '__main__':
    test_complex()
