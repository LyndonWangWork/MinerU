#!/usr/bin/env python
"""
MinerU Entry Point for PyInstaller
This wrapper script avoids relative import issues in PyInstaller
"""

import sys
import os

# Ensure mineru package is importable
if __name__ == '__main__':
    # Import the main function using absolute imports
    from mineru.cli.client import main

    # Run the CLI
    main()
