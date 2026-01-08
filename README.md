# Recipe API - Python Starter

This is a Python starter kit for the [Recipe API](https://recipe-api.com). It includes a client library and example scripts to help you get started.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd recipe-api-python
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    *   Copy `.env.example` to `.env`
    *   Get your API key from [recipe-api.com](https://recipe-api.com)
    *   Add it to `.env`: `RECIPE_API_KEY=rapi_...`

## Usage

Run the example scripts to explore the API:

*   **List dietary flags:**
    ```bash
    python src/scripts/01_categories.py
    ```

*   **List cuisines:**
    ```bash
    python src/scripts/02_cuisines.py
    ```

*   **Browse recipes:**
    ```bash
    python src/scripts/03_browse.py
    python src/scripts/03_browse.py --page=2
    ```

*   **Search recipes:**
    ```bash
    python src/scripts/04_search.py --q="pasta"
    ```

*   **Filter recipes:**
    ```bash
    python src/scripts/05_filter.py --cuisine="Italian" --difficulty="Beginner"
    ```

*   **Get full recipe details:**
    ```bash
    python src/scripts/06_recipe.py --id=<recipe_id>
    ```

*   **List ingredient categories:**
    ```bash
    python src/scripts/07_ingredient_categories.py
    ```

*   **Search ingredients:**
    ```bash
    python src/scripts/08_ingredients.py --q="chicken"
    python src/scripts/08_ingredients.py --category="Vegetables"
    ```

## Project Structure

*   `src/client.py`: API client configuration and request handling
*   `src/utils.py`: Helper functions for formatting output
*   `src/scripts/`: Example scripts demonstrating various endpoints
