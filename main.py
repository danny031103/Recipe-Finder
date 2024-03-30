import requests
import config

def get_recipes(ingredients):
    #url for api
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={",".join(ingredients)}&apiKey={config.API_key}'
    #url response
    response = requests.get(url)
    #all good
    if response.status_code==200:
        data=response.json()
        return data
    #didnt work
    else:
        print(f'Error: {response.status_code}')
        return 
    
def get_ingredients(title):
    url = f'https://api.spoonacular.com/recipes/search?query={title}&apiKey={config.API_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            recipe_id = data['results'][0]['id']
            recipe_details_url = f'https://api.spoonacular.com/recipes/{recipe_id}/ingredientWidget.json?apiKey={config.API_key}'
            details_response = requests.get(recipe_details_url)
            if details_response.status_code == 200:
                details_data = details_response.json()
                ingredients = details_data['ingredients']
                return ingredients
            else:
                print(f"Failed to fetch recipe details: {details_response.status_code}")
        
    else:
        print(f"Failed to fetch recipe: {response.status_code}")

def main():
    while True:
        print()
        choiceofuser=int(input("What would you like to do: \n1. Search for recipes using all your ingredients?\n2. Search for recipes that include some of your ingredients?\n3.Quit\n"))
        #show recipes that include all of the ingredients listed by the user
        if choiceofuser==1:
            print()
            ingredients=input("Enter your (comma separated) ingredients: ").lower().split(',')
            recipes = get_recipes(ingredients)
            if recipes:
                print("Found Recipes:\n")
                for recipe in recipes:
                    used_ingredient_names = [ingredient['name'] for ingredient in recipe['usedIngredients']]
                    if all(ingredient in used_ingredient_names for ingredient in ingredients):
                        print("Dish Name:", recipe['title'])
                        print("All Ingredients:")
                        ingredientslist = get_ingredients(recipe['title'])
                        if ingredientslist:
                            for ing in ingredientslist:
                                print("-", ing['name'].capitalize())
                            print()
                        else:
                            print("Ingredients not found.")

        #show all possible recipes that include at least one of the ingredients listed by the user
        elif choiceofuser==2:
            ingredients=input("Enter your (comma separated) ingredients: ").lower().split(',')
            recipes=get_recipes(ingredients)
            if recipes:
                print("Found recipes:")
                for recipe in recipes:
                    print("\nRecipe Name:", recipe['title'])
                    print("All Ingredients:")
                    ingredientslist = get_ingredients(recipe['title'])
                    if ingredientslist:
                        for ing in ingredientslist:
                            print("-", ing['name'].capitalize())
                    else:
                         print("Ingredients not found.")
            else:
                print("No recipes found.")
            
        #quit   
        elif choiceofuser==3:
            break
        else:
            print("Invalid choice. Try again.")

#usedIngredients-returns a list of ingredients used in the recipe as an
#instructions-returns the instructions for the recipe as a string
#title-returns the title of the recipe as a string  

#run 
if __name__ == "__main__":
    main()

