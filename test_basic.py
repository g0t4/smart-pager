#!/usr/bin/env python3
"""Basic test to verify the pager loads correctly."""

import sys
sys.path.insert(0, '.')

from smart_pager.pager import SmartPager

def test_basic():
    """Test basic functionality."""
    pager = SmartPager('examples/sample_logs.txt')
    print(f"Loaded {len(pager.lines)} lines")
    
    # Test JSON detection
    json_lines = []
    for i, line in enumerate(pager.lines):
        is_json, parsed = pager._is_json_line(line)
        if is_json:
            json_lines.append(i)
            print(f"Line {i+1}: JSON detected")
    
    print(f"Found {len(json_lines)} JSON lines")
    
    # Test formatting
    if pager.lines:
        formatted = pager._format_line(0, pager.lines[0])
        print(f"First line formatted: {formatted.plain}")

if __name__ == '__main__':
    test_basic()
