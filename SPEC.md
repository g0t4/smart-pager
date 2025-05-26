# Smart Pager Specification

A vim-like pager with JSON syntax highlighting and expansion capabilities for log file analysis.

## Phase 1 (MVP)

### Core Features
- [x] Load files into memory (assume reasonable file sizes)
- [x] Vim-style navigation:
  - `j/k` - line up/down
  - `gg/G` - top/bottom of file
  - `Ctrl+d/Ctrl+u` - half-page scroll
- [x] Mouse support:
  - Click to position cursor
- [x] JSON detection and highlighting:
  - Try-parse each line for valid JSON
  - Syntax highlight valid JSON lines
  - Show indicator for invalid JSON that looked like JSON
- [x] Current line expansion:
  - Toggle expand/collapse JSON on current line only
  - Pretty-printed with proper indentation
- [x] Dynamic terminal resize handling
- [x] Clean exit with `q`

### Assumptions
- Single JSON object per line
- Files small enough to fit in memory
- Users have pre-filtered large log files

## Phase 2 (Future Features)

### Enhanced Navigation
- [ ] Line numbering display
- [ ] Search functionality (`/` and `?`)
- [ ] Jump to line (`:123`)
- [ ] Horizontal scrolling for wide content

### JSON Enhancements
- [ ] Nested/escaped JSON detection
- [ ] Multiple JSON objects per line
- [ ] Persistent expansion state when scrolling
- [ ] Expand multiple lines simultaneously

### Performance & Scale
- [ ] Memory mapping for large files
- [ ] Lazy loading and parsing
- [ ] Streaming mode for real-time log following

### Advanced Features
- [ ] Custom syntax highlighting themes
- [ ] Export expanded JSON to file
- [ ] Bookmark frequently viewed lines
- [ ] Split view (raw vs formatted)

## Technical Notes

### Architecture
- Python + Rich for terminal UI
- JSON parsing with built-in `json` module
- Event-driven cursor and display management

### Key Bindings
- `j/k` - Navigate up/down
- `gg/G` - Go to top/bottom
- `Ctrl+d/Ctrl+u` - Page up/down
- `Enter` or `Space` - Toggle JSON expansion
- `q` - Quit
- Mouse click - Position cursor

### Error Handling
- Graceful handling of invalid JSON
- Terminal resize events
- File read errors
- Keyboard interrupts
