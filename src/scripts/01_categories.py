import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, divider

def main():
    header('Dietary Flags')

    response = api_request('/api/v1/dietary-flags')
    data = response['data']

    print(f"Found {len(data)} dietary options:\n")

    # Sort by count descending
    sorted_flags = sorted(data, key=lambda x: x['count'], reverse=True)

    for flag in sorted_flags[:20]:
        print(f"  * {flag['name']} ({flag['count']} recipes)")

    if len(sorted_flags) > 20:
        print(f"  ... and {len(sorted_flags) - 20} more")

    divider()
    print('\n>> Next step: Run `python src/scripts/02_cuisines.py` to see available cuisines\n')

if __name__ == "__main__":
    main()

