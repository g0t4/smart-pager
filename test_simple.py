#!/usr/bin/env python3
"""Test the simple version interactively."""

import sys
sys.path.insert(0, '.')

from smart_pager.main_simple import main

if __name__ == '__main__':
    # Override sys.argv for testing
    sys.argv = ['test_simple.py', 'examples/sample_logs.txt']
    main()
