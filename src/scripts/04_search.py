import sys
import os
import argparse
import math

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, label, divider, format_duration, highlight, truncate

def main():
    parser = argparse.ArgumentParser(description='Search recipes')
    parser.add_argument('--q', type=str, required=True, help='Search query')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--per_page', type=int, default=10, help='Items per page')
    args = parser.parse_args()

    header(f'Search: "{args.q}"')

    response = api_request('/api/v1/recipes', {
        'q': args.q,
        'page': args.page,
        'per_page': args.per_page
    })

    recipes = response['data']
    meta = response['meta']

    if not recipes:
        print('No recipes found matching your search.\n')
        print('Try:')
        print('  * Different keywords')
        print('  * Broader terms')
        print('  * Check spelling\n')
        return

    total_pages = math.ceil(meta['total'] / meta['per_page'])
    print(f"Page {meta['page']} of {total_pages} ({meta['total']} matching recipes)\n")

    for recipe in recipes:
        print(f"{highlight(recipe['name'])}")
        label('ID', recipe['id'])
        label('Category', f"{recipe['category']} | {recipe['cuisine']}")
        label('Difficulty', recipe['difficulty'])
        label('Time', format_duration(recipe['meta']['total_time']))
        
        if recipe['dietary']['flags']:
            label('Dietary', ', '.join(recipe['dietary']['flags'][:4]))
            
        label('Calories', f"{round(recipe['nutrition_summary']['calories'])} kcal")
        print(f"  {truncate(recipe['description'], 80)}")
        divider()

if __name__ == "__main__":
    main()
