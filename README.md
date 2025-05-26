# Smart Pager

A vim-like terminal pager with JSON syntax highlighting and expansion for log file analysis.

## Features

- 🚀 **Vim-style navigation** - j/k, gg/G, Ctrl+d/Ctrl+u
- 🖱️ **Mouse support** for cursor positioning  
- 🎨 **Automatic JSON detection** and syntax highlighting
- 📖 **Interactive JSON expansion/collapse** - see pretty-printed JSON inline
- 📏 **Dynamic terminal resizing** support
- ⚡ **Fast and lightweight** - built with Rich for beautiful terminal UI

## Demo

Load up a log file with JSON entries and navigate through it like vim:

```bash
smart-pager /var/log/app.log
```

JSON lines are automatically highlighted, and you can press Enter to expand them into pretty-printed format.

## Installation

### Development Setup

```bash
git clone <repo-url>
cd smart-pager
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Install as Package

```bash
pip install -e .  # Install in development mode
# OR
pip install .     # Install normally
```

## Usage

### Command Line

```bash
# Using the script directly
python smart_pager.py <filename>

# Using as a module
python -m smart_pager <filename>

# If installed as package
smart-pager <filename>
```

### Key Bindings

| Key | Action |
|-----|--------|
| `j` or `↓` | Move down one line |
| `k` or `↑` | Move up one line |
| `gg` | Go to top of file |
| `G` | Go to bottom of file |
| `Ctrl+d` | Page down (half screen) |
| `Ctrl+u` | Page up (half screen) |
| `Enter` or `Space` | Toggle JSON expansion on current line |
| `q` | Quit |
| Mouse click | Position cursor |

### JSON Features

- **Auto-detection**: Lines starting with `{` or `[` are checked for valid JSON
- **Syntax highlighting**: Valid JSON is highlighted in color
- **Error indication**: Invalid JSON that looks like JSON shows a ⚠ symbol
- **Expansion**: Current line JSON can be toggled between compact and pretty-printed
- **Smart navigation**: Moving cursor automatically collapses expanded JSON

## Examples

The `examples/` directory contains sample log files:

```bash
python smart_pager.py examples/sample_logs.txt
```

## Development

### Running Tests

```bash
# Test basic functionality
python test_basic.py

# Test rendering
python test_render.py

# Test input handling
python test_interactive.py
```

### Project Structure

```
smart-pager/
├── smart_pager/           # Main package
│   ├── __init__.py
│   ├── main.py           # Entry point and event loop
│   ├── pager.py          # Core pager logic
│   └── input_handler.py  # Terminal input handling
├── examples/             # Sample files
├── tests/               # Test files
├── SPEC.md              # Feature specification
└── README.md
```

## Contributing

See `SPEC.md` for the full feature roadmap. Phase 1 features are complete, Phase 2 features are planned for future releases.

## License

MIT License - see LICENSE file for details.
