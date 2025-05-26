"""Simple terminal renderer without Rich layouts."""

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from pathlib import Path


class SimpleRenderer:
    """Simple renderer that outputs plain text with minimal Rich styling."""
    
    def __init__(self, pager):
        self.pager = pager
        self.console = Console()
    
    def render_simple(self):
        """Render content as simple text without complex layouts."""
        lines = []
        
        # Title
        title = f"Smart Pager - {Path(self.pager.filename).name}"
        lines.append("=" * len(title))
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")
        
        # Content
        visible_lines = self.pager._get_visible_lines()
        
        for line_num, line in visible_lines:
            is_json, _ = self.pager._is_json_line(line)
            looks_like_json = self.pager._looks_like_json(line)
            is_current = line_num == self.pager.current_line
            
            # Create line prefix
            if is_current:
                prefix = "► "
            else:
                prefix = "  "
            
            # Add status indicators
            if is_json:
                prefix += "[JSON] "
            elif looks_like_json:
                prefix += "[!JSON] "
            else:
                prefix += ""
            
            # Add the line
            display_line = prefix + line
            lines.append(display_line)
            
            # Show expanded JSON if this line is expanded
            if (self.pager.expanded_line == line_num and 
                line_num == self.pager.current_line):
                expanded = self.pager._get_expanded_json(line)
                if expanded:
                    for exp_line in expanded.split("\n"):
                        lines.append("    " + exp_line)
        
        # Status line
        lines.append("")
        lines.append("-" * 60)
        
        status_parts = [f"Line {self.pager.current_line + 1}/{len(self.pager.lines)}"]
        
        if self.pager.lines:
            current_line_text = self.pager.lines[self.pager.current_line]
            is_json, _ = self.pager._is_json_line(current_line_text)
            looks_like_json = self.pager._looks_like_json(current_line_text)
            
            if is_json:
                if self.pager.expanded_line == self.pager.current_line:
                    status_parts.append("JSON - Expanded")
                else:
                    status_parts.append("JSON - Press Enter to expand")
            elif looks_like_json:
                status_parts.append("Invalid JSON")
        
        status_parts.append("Press 'q' to quit, 'j/k' to move")
        lines.append(" | ".join(status_parts))
        
        return "\n".join(lines)
