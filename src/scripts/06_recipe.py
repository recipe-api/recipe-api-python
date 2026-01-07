import sys
import os
import argparse

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import api_request, RecipeApiError
from utils import header, subheader, label, format_duration, highlight, warning

def main():
    parser = argparse.ArgumentParser(description='Get full recipe details')
    parser.add_argument('--id', type=str, help='Recipe ID')
    args = parser.parse_args()

    if not args.id:
        print('\nGet full recipe details\n')
        warning('!! Note: This endpoint costs 1 credit per request !!\n')
        print('Usage: python src/scripts/06_recipe.py --id=<recipe_id>\n')
        print('To find recipe IDs:')
        print('  1. Run `python src/scripts/03_browse.py` or `python src/scripts/04_search.py`')
        print('  2. Copy the ID from a recipe you want\n')
        return

    warning('\n!! Fetching full recipe (costs 1 credit) ...\n')

    try:
        response = api_request(f'/api/v1/recipes/{args.id}')
        recipe = response['data']
        usage = response.get('usage')

        header(recipe['name'])

        print(recipe['description'])
        print()

        # Overview
        label('Category', f"{recipe['category']} | {recipe['cuisine']}")
        label('Difficulty', recipe['difficulty'])
        label('Active time', format_duration(recipe['meta']['active_time']))
        label('Passive time', format_duration(recipe['meta']['passive_time']))
        label('Total time', format_duration(recipe['meta']['total_time']))
        label('Yields', recipe['meta']['yields'])
        
        if recipe['dietary']['flags']:
            label('Dietary', ', '.join(recipe['dietary']['flags']))
            
        if recipe['meta']['overnight_required']:
            warning('  ** Requires overnight preparation **')

        # Nutrition
        nutrition = recipe['nutrition']['per_serving']
        print()
        subheader('Nutrition (per serving)')
        label('Calories', f"{round(nutrition['calories'])} kcal")
        label('Protein', f"{round(nutrition['protein_g'])}g")
        label('Carbs', f"{round(nutrition['carbohydrates_g'])}g")
        label('Fat', f"{round(nutrition['fat_g'])}g")
        if nutrition.get('fiber_g'):
            label('Fiber', f"{round(nutrition['fiber_g'])}g")

        # Equipment
        if recipe['equipment']:
            print()
            subheader('Equipment')
            for item in recipe['equipment']:
                alt = f" (or: {item['alternative']})" if item['alternative'] else ''
                req = '' if item['required'] else ' [optional]'
                print(f"  * {item['name']}{alt}{req}")

        # Ingredients
        print()
        subheader('Ingredients')
        for group in recipe['ingredients']:
            if group.get('group_name'):
                print(f"\n  [{group['group_name']}]")
            for ing in group['items']:
                amount = f"{ing['quantity']} {ing['unit']}" if ing['unit'] else f"{ing['quantity']}"
                prep = f", {ing['preparation']}" if ing['preparation'] else ''
                notes = f" ({ing['notes']})" if ing['notes'] else ''
                print(f"  * {amount} {ing['name']}{prep}{notes}")

        # Instructions
        print()
        subheader('Instructions')
        for step in recipe['instructions']:
            duration = ''
            if step.get('structured') and step['structured'].get('duration'):
                duration = f" {highlight(f'[{format_duration(step['structured']['duration'])}]')}"
            
            print(f"\n  {step['step_number']}. [{step['phase']}] {step['text']}{duration}")

            if step.get('tips'):
                for tip in step['tips']:
                    print(f"     >> {tip}")

        # Chef notes
        if recipe.get('chef_notes'):
            print()
            subheader('Chef Notes')
            for note in recipe['chef_notes']:
                print(f"  * {note}")

        # Cultural context
        if recipe.get('cultural_context'):
            print()
            subheader('About This Dish')
            print(f"  {recipe['cultural_context']}")

        # Storage
        if recipe.get('storage'):
            print()
            subheader('Storage')
            storage = recipe['storage']
            if storage.get('does_not_keep'):
                print('  Best eaten immediately.')
            if storage.get('refrigerator'):
                ref = storage['refrigerator']
                print(f"  Refrigerator: {ref.get('notes') or ref.get('duration')}")
            if storage.get('reheating'):
                print(f"  Reheating: {storage['reheating']}")

        # Usage info
        if usage:
            print('\n--- API Usage ---')
            print(f"Monthly remaining: {usage['monthly_remaining']:,}")
            print(f"Daily remaining:   {usage['daily_remaining']:,}")

        print()

    except RecipeApiError as e:
        if e.status == 404:
            print(f'\n[X] Recipe not found: {args.id}\n')
            print('Make sure the ID is correct. Find IDs with:')
            print('  python src/scripts/03_browse.py')
            print('  python src/scripts/04_search.py --q="..."\n')
        else:
            raise e

if __name__ == "__main__":
    main()
