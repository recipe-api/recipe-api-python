import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, divider

def main():
    header('Ingredient Categories')

    response = api_request('/api/v1/ingredient-categories')
    data = response['data']

    print(f"Found {len(data)} ingredient categories:\n")

    # Sort by count descending
    sorted_categories = sorted(data, key=lambda x: x['count'], reverse=True)

    for category in sorted_categories[:20]:
        print(f"  * {category['name']} ({category['count']:,} ingredients)")

    if len(sorted_categories) > 20:
        print(f"  ... and {len(sorted_categories) - 20} more")

    divider()
    print('\n>> Next step: Run `python src/scripts/08_ingredients.py` to browse ingredients\n')

if __name__ == "__main__":
    main()
