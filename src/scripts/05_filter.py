import sys
import os
import argparse
import math

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request
from utils import header, label, divider, format_duration, highlight, truncate

def main():
    parser = argparse.ArgumentParser(description='Filter recipes')
    parser.add_argument('--category', type=str, help='Recipe category')
    parser.add_argument('--cuisine', type=str, help='Cuisine type')
    parser.add_argument('--difficulty', type=str, help='Difficulty level')
    parser.add_argument('--dietary', type=str, help='Dietary preference')
    parser.add_argument('--max_calories', type=int, help='Maximum calories')
    parser.add_argument('--min_protein', type=int, help='Minimum protein')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--per_page', type=int, default=10, help='Items per page')
    
    # parse_known_args allows us to check if any filters were provided easily if we wanted, 
    # but argparse doesn't give a simple "was anything passed" flag.
    # We'll check values manually.
    args = parser.parse_args()

    has_filters = any([
        args.category, args.cuisine, args.difficulty, 
        args.dietary, args.max_calories, args.min_protein
    ])

    if not has_filters:
        print('\nFilter recipes by multiple criteria\n')
        print('Available filters:')
        print('  --category     Recipe category (Breakfast, Main, Dessert, etc.)')
        print('  --cuisine      Cuisine type (run `python src/scripts/02_cuisines.py` for list)')
        print('  --difficulty   Beginner, Intermediate, or Advanced')
        print('  --dietary      Vegetarian, Vegan, Gluten-Free, etc. (run `python src/scripts/01_categories.py`)')
        print('  --max_calories Maximum calories per serving')
        print('  --min_protein  Minimum protein in grams\n')
        print('Examples:')
        print('  python src/scripts/05_filter.py --cuisine="Italian" --difficulty="Beginner"')
        print('  python src/scripts/05_filter.py --dietary="Vegan" --max_calories=400')
        print('  python src/scripts/05_filter.py --category="Dessert" --cuisine="French"\n')
        return

    # Build filter description
    filters = []
    if args.category: filters.append(f"category={args.category}")
    if args.cuisine: filters.append(f"cuisine={args.cuisine}")
    if args.difficulty: filters.append(f"difficulty={args.difficulty}")
    if args.dietary: filters.append(f"dietary={args.dietary}")
    if args.max_calories: filters.append(f"max_calories={args.max_calories}")
    if args.min_protein: filters.append(f"min_protein={args.min_protein}")
    
    header('Filtered Recipes')
    print(f"Filters: {', '.join(filters)}\n")

    params = {
        'category': args.category,
        'cuisine': args.cuisine,
        'difficulty': args.difficulty,
        'dietary': args.dietary,
        'max_calories': args.max_calories,
        'min_protein': args.min_protein,
        'page': args.page,
        'per_page': args.per_page
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    response = api_request('/api/v1/recipes', params)

    recipes = response['data']
    meta = response['meta']

    if not recipes:
        print('No recipes match your filters.\n')
        print('Try relaxing some criteria.\n')
        return

    print(f"Found {meta['total']} matching recipes\n")

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

    print('\n>> Get full recipe: python src/scripts/06_recipe.py --id=<recipe_id>\n')

if __name__ == "__main__":
    main()
