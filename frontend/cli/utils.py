# utils.py

import requests
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown

# Shared console object
console = Console()

# Token file path (same behavior as original CLI)
TOKEN_FILE = Path(__file__).parent / '.devlog_token'
