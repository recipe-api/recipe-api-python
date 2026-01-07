import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, divider

def main():
    header('Cuisines')

    response = api_request('/api/v1/cuisines')
    data = response['data']

    print(f"Found {len(data)} cuisines:\n")

    # Sort by count descending
    sorted_cuisines = sorted(data, key=lambda x: x['count'], reverse=True)

    for cuisine in sorted_cuisines:
        bar = '█' * min(cuisine['count'] // 20, 20)
        print(f"  {cuisine['name']:<20} {bar} {cuisine['count']}")

    divider()
    print('\n>> Next step: Run `python src/scripts/03_browse.py` to see recipes\n')

if __name__ == "__main__":
    main()

