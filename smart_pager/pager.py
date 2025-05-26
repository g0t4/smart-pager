"""Core pager functionality."""

import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich import box


class SmartPager:
    """A vim-like pager with JSON highlighting capabilities."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.console = Console()
        self.lines = []
        self.current_line = 0
        self.scroll_offset = 0
        self.expanded_line = None  # Track which line is expanded
        self.terminal_height = self.console.size.height - 4  # Leave room for status and borders
        
        # Load file
        self._load_file()
        
    def _load_file(self):
        """Load file content into memory."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.lines = [line.rstrip('\n\r') for line in f.readlines()]
        except Exception as e:
            self.console.print(f"Error reading file: {e}", style="red")
            sys.exit(1)
            
    def _is_json_line(self, line: str) -> Tuple[bool, Optional[dict]]:
        """Check if line contains valid JSON."""
        line = line.strip()
        if not line or not (line.startswith('{') or line.startswith('[')):
            return False, None
            
        try:
            parsed = json.loads(line)
            return True, parsed
        except (json.JSONDecodeError, ValueError):
            return False, None
            
    def _looks_like_json(self, line: str) -> bool:
        """Check if line looks like JSON but might be invalid."""
        line = line.strip()
        return bool(line and (line.startswith('{') or line.startswith('[')) and 
                   ('"' in line or "'" in line))
    
    def _colorize_json(self, line: str) -> Text:
        """Simple JSON colorization."""
        text = Text()
        
        # Use Rich's JSON syntax highlighting
        try:
            # Create syntax object but extract just the text with styles
            syntax = Syntax(line, "json", theme="monokai", line_numbers=False, background_color=None)
            # For now, just return styled text - Rich will handle the coloring
            return Text(line, style="bright_green")
        except:
            return Text(line, style="green")
    
    def _format_line(self, line_num: int, line: str) -> Text:
        """Format a line with appropriate styling."""
        is_json, parsed_json = self._is_json_line(line)
        is_current = line_num == self.current_line
        
        # Create base text
        text = Text()
        
        if is_current:
            text.append("► ", style="bright_yellow")
        else:
            text.append("  ")
            
        if is_json:
            # Colorize JSON
            text.append(self._colorize_json(line))
        elif self._looks_like_json(line):
            # Invalid JSON that looks like JSON
            text.append("⚠ ", style="red")
            text.append(line, style="dim red")
        else:
            # Regular line
            if is_current:
                text.append(line, style="white")
            else:
                text.append(line, style="dim white")
            
        return text
    
    def _get_expanded_json(self, line: str) -> Optional[Text]:
        """Get pretty-printed JSON for a line."""
        is_json, parsed_json = self._is_json_line(line)
        if not is_json:
            return None
            
        try:
            pretty_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
            return Text(pretty_json, style="bright_cyan")
        except:
            return None
    
    def _get_visible_lines(self) -> List[Tuple[int, str]]:
        """Get lines that should be visible on screen."""
        start = self.scroll_offset
        end = min(start + self.terminal_height, len(self.lines))
        return [(i, self.lines[i]) for i in range(start, end)]
    
    def _update_scroll_offset(self):
        """Update scroll offset to keep current line visible."""
        if self.current_line < self.scroll_offset:
            self.scroll_offset = self.current_line
        elif self.current_line >= self.scroll_offset + self.terminal_height:
            self.scroll_offset = self.current_line - self.terminal_height + 1
            
        # Keep scroll offset in bounds
        self.scroll_offset = max(0, min(self.scroll_offset, 
                                      max(0, len(self.lines) - self.terminal_height)))
    
    def _render_content(self) -> Panel:
        """Render the main content panel."""
        self._update_scroll_offset()
        
        content = Text()
        visible_lines = self._get_visible_lines()
        
        for i, (line_num, line) in enumerate(visible_lines):
            if i > 0:
                content.append("\n")
                
            formatted_line = self._format_line(line_num, line)
            content.append(formatted_line)
            
            # Show expanded JSON if this line is expanded
            if (self.expanded_line == line_num and 
                line_num == self.current_line):
                expanded = self._get_expanded_json(line)
                if expanded:
                    content.append("\n")
                    # Indent the expanded JSON
                    for exp_line in expanded.plain.split("\n"):
                        content.append("    " + exp_line + "\n", style="bright_cyan")
        
        return Panel(
            content,
            title=f"Smart Pager - {Path(self.filename).name}",
            box=box.ROUNDED,
            title_align="left"
        )
    
    def _render_status(self) -> Text:
        """Render status line."""
        status = Text()
        status.append(f"Line {self.current_line + 1}/{len(self.lines)} ", style="dim")
        
        if self.lines:
            current_line_text = self.lines[self.current_line]
            is_json, _ = self._is_json_line(current_line_text)
            
            if is_json:
                if self.expanded_line == self.current_line:
                    status.append("[JSON - Expanded] ", style="green")
                else:
                    status.append("[JSON - Press Enter to expand] ", style="cyan")
            elif self._looks_like_json(current_line_text):
                status.append("[Invalid JSON] ", style="red")
        
        status.append("Press 'q' to quit, 'j/k' to move, 'gg/G' for top/bottom", style="dim")
        return status
    
    def move_up(self):
        """Move cursor up."""
        if self.current_line > 0:
            self.current_line -= 1
            # Collapse any expanded line when moving
            self.expanded_line = None
            
    def move_down(self):
        """Move cursor down."""
        if self.current_line < len(self.lines) - 1:
            self.current_line += 1
            # Collapse any expanded line when moving
            self.expanded_line = None
    
    def move_to_top(self):
        """Move to first line."""
        self.current_line = 0
        self.expanded_line = None
        
    def move_to_bottom(self):
        """Move to last line."""
        if self.lines:
            self.current_line = len(self.lines) - 1
        self.expanded_line = None
    
    def page_down(self):
        """Move down half a page."""
        self.current_line = min(len(self.lines) - 1, 
                              self.current_line + self.terminal_height // 2)
        self.expanded_line = None
    
    def page_up(self):
        """Move up half a page."""
        self.current_line = max(0, self.current_line - self.terminal_height // 2)
        self.expanded_line = None
    
    def toggle_expansion(self):
        """Toggle JSON expansion for current line."""
        if not self.lines:
            return
            
        current_line_text = self.lines[self.current_line]
        is_json, _ = self._is_json_line(current_line_text)
        
        if is_json:
            if self.expanded_line == self.current_line:
                # Collapse
                self.expanded_line = None
            else:
                # Expand
                self.expanded_line = self.current_line
    
    def click_to_line(self, row: int):
        """Move cursor to clicked line."""
        # Convert screen row to line number
        clicked_line = self.scroll_offset + row - 1  # -1 for panel border
        if 0 <= clicked_line < len(self.lines):
            self.current_line = clicked_line
            self.expanded_line = None
    
    def render(self) -> Layout:
        """Render the complete interface."""
        layout = Layout()
        layout.split_column(
            Layout(self._render_content(), name="main", ratio=10),
            Layout(self._render_status(), name="status", size=1)
        )
        return layout
