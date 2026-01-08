import sys
import os
import argparse

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, divider

def main():
    parser = argparse.ArgumentParser(description='Browse and search ingredients')
    parser.add_argument('--q', type=str, help='Search by ingredient name')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--per_page', type=int, default=20, help='Results per page')
    args = parser.parse_args()

    header('Browse Ingredients')

    if args.q:
        print(f'Search: "{args.q}"')
    if args.category:
        print(f'Category: {args.category}')
    print()

    params = {
        'page': args.page,
        'per_page': args.per_page
    }
    if args.q:
        params['q'] = args.q
    if args.category:
        params['category'] = args.category

    response = api_request('/api/v1/ingredients', params)
    data = response['data']
    meta = response['meta']

    print(f"Found {meta['total']:,} ingredients (page {meta['page']}):\n")

    for ingredient in data:
        print(f"  {ingredient['name']}")
        print(f"    ID: {ingredient['id']}")
        print(f"    Category: {ingredient['category']}")
        print(f"    Source: {ingredient['source']}")
        print()

    divider()

    print('\nUsage examples:')
    print('  python src/scripts/08_ingredients.py --q="chicken"')
    print('  python src/scripts/08_ingredients.py --category="Vegetables"')
    print('  python src/scripts/08_ingredients.py --page=2')
    print('\nUse ingredient IDs to filter recipes:')
    print('  python src/scripts/05_filter.py --ingredients="<id1>,<id2>"\n')

if __name__ == "__main__":
    main()
