import os
import sys

# ANSI color codes
COLORS = {
    'reset': '\033[0m',
    'bright': '\033[1m',
    'dim': '\033[2m',
    'cyan': '\033[36m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'red': '\033[31m',
}

def header(text):
    print(f"\n{COLORS['bright']}{COLORS['cyan']}=== {text} ==={COLORS['reset']}\n")

def subheader(text):
    print(f"{COLORS['bright']}{text}{COLORS['reset']}")

def label(name, value):
    print(f"  {COLORS['dim']}{name}:{COLORS['reset']} {value}")

def list_item(text, indent=0):
    spaces = '  ' * indent
    print(f"{spaces}{COLORS['green']}*{COLORS['reset']} {text}")

def divider():
    print(f"{COLORS['dim']}{'─' * 50}{COLORS['reset']}")

def highlight(text):
    return f"{COLORS['yellow']}{text}{COLORS['reset']}"

def success(text):
    print(f"{COLORS['green']}{text}{COLORS['reset']}")

def warning(text):
    print(f"{COLORS['yellow']}{text}{COLORS['reset']}")

def format_duration(iso_duration):
    """
    Parse ISO 8601 duration to human-readable format
    e.g., "PT30M" -> "30 min", "PT1H30M" -> "1h 30m"
    """
    if not iso_duration.startswith('PT'):
        return iso_duration
    
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if not match:
        return iso_duration
        
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    
    if hours == 0 and minutes == 0:
        return 'instant'
    if hours == 0:
        return f"{minutes} min"
    if minutes == 0:
        return f"{hours}h"
    return f"{hours}h {minutes}m"

def truncate(text, max_length):
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'
