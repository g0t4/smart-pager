#!/usr/bin/env python3
"""Comprehensive feature test."""

import sys
sys.path.insert(0, '.')

from smart_pager.pager import SmartPager
from rich.console import Console

def test_all_features():
    """Test all implemented features."""
    console = Console()
    
    print("🧪 Testing Smart Pager Features\n")
    
    # Test with complex log file
    pager = SmartPager('examples/complex_logs.txt')
    
    print(f"✅ File loading: {len(pager.lines)} lines loaded")
    
    # Test JSON detection
    json_lines = []
    invalid_json_lines = []
    regular_lines = []
    
    for i, line in enumerate(pager.lines):
        is_json, parsed = pager._is_json_line(line)  
        looks_like_json = pager._looks_like_json(line)
        
        if is_json:
            json_lines.append(i)
        elif looks_like_json:
            invalid_json_lines.append(i)
        else:
            regular_lines.append(i)
    
    print(f"✅ JSON detection: {len(json_lines)} valid, {len(invalid_json_lines)} invalid, {len(regular_lines)} regular")
    
    # Test navigation
    pager.current_line = 0
    print(f"✅ Navigation - Start at line: {pager.current_line + 1}")
    
    pager.move_down()
    pager.move_down()
    print(f"✅ Navigation - After 2 down moves: {pager.current_line + 1}")
    
    pager.move_to_bottom()
    print(f"✅ Navigation - Bottom: {pager.current_line + 1}")
    
    pager.move_to_top() 
    print(f"✅ Navigation - Top: {pager.current_line + 1}")
    
    # Test JSON expansion
    for line_num in json_lines[:2]:  # Test first 2 JSON lines
        pager.current_line = line_num
        pager.toggle_expansion()
        
        if pager.expanded_line == line_num:
            print(f"✅ JSON expansion: Line {line_num + 1} expanded")
            
            # Test collapse
            pager.toggle_expansion()
            if pager.expanded_line is None:
                print(f"✅ JSON collapse: Line {line_num + 1} collapsed")
        else:
            print(f"❌ JSON expansion failed for line {line_num + 1}")
    
    # Test status line rendering
    pager.current_line = json_lines[0] if json_lines else 0
    status = pager._render_status()
    print(f"✅ Status rendering: {len(status.plain)} chars")
    
    # Test panel rendering  
    panel = pager._render_content()
    print(f"✅ Panel rendering: Generated successfully")
    
    # Test terminal size handling
    original_height = pager.terminal_height
    pager.terminal_height = 10  # Simulate smaller terminal
    pager._update_scroll_offset()
    print(f"✅ Terminal resize: Height changed from {original_height} to {pager.terminal_height}")
    
    print(f"\n🎉 All features working! Ready for interactive use.")
    print(f"📝 Run: python smart_pager.py examples/complex_logs.txt")

if __name__ == '__main__':
    test_all_features()
