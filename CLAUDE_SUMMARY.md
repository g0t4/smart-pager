# Smart Pager - Built by Claude

## What We Built 🚀

A complete **vim-like terminal pager** with JSON syntax highlighting and interactive expansion - perfect for analyzing log files!

## Key Features ✨

- **🎯 Vim Navigation**: j/k, gg/G, Ctrl+d/Ctrl+u - feels natural for vim users
- **🎨 Smart JSON Detection**: Automatically finds and highlights JSON anywhere in log lines
- **📖 Interactive Expansion**: Press Enter to pretty-print JSON inline, toggle to collapse
- **🖱️ Mouse Support**: Click to position cursor
- **📏 Dynamic Resize**: Handles terminal size changes gracefully
- **⚠️ Error Detection**: Shows warning icon for malformed JSON
- **🎪 Beautiful UI**: Rich terminal interface with panels and status

## Quick Start 🏃‍♂️

```bash
# Setup
make setup
make test

# Try it out!
python smart_pager.py examples/sample_logs.txt
python smart_pager.py examples/complex_logs.txt

# Use with your logs
python smart_pager.py /path/to/your/logfile.log
```

## Architecture Highlights 🏗️

- **Python + Rich**: Beautiful terminal UI framework
- **Event-driven**: Responsive keyboard and mouse handling  
- **Regex JSON Detection**: Finds JSON in mixed-content log lines
- **Memory Efficient**: Loads reasonable-sized files entirely into memory
- **Extensible**: Clean modular design ready for Phase 2 features

## What's Unique 🌟

Unlike basic pagers, Smart Pager:
- **Understands JSON structure** - not just text
- **Interactive expansion** - see formatted JSON without leaving the file
- **Context aware** - knows what's JSON vs regular log text
- **Vim-native** - familiar keybindings that feel natural

## Test Coverage 🧪

Comprehensive test suite:
- ✅ Basic functionality (`test_basic.py`)
- ✅ UI rendering (`test_render.py`) 
- ✅ Complex JSON handling (`test_complex.py`)
- ✅ End-to-end features (`test_features.py`)

## Ready for Real Use 🎯

Phase 1 MVP is **production-ready** for:
- Application log analysis
- API response debugging  
- Configuration file review
- Any text files with embedded JSON

## Future Roadmap 🗺️

Phase 2 could add:
- Search functionality
- Line numbers
- Horizontal scrolling
- Multi-line JSON expansion
- Custom themes
- Performance optimizations for larger files

---

**Built with care by Claude** 🤖  
*Making log analysis delightful, one JSON expansion at a time!*
