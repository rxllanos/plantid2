import requests
import json

import os
import django
from django.contrib.postgres.search import TrigramSimilarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantas.settings')
django.setup()

from planta.models import IngredientID

api_key= 'cfe862eb5b72450185899fbba7ec215c'
headers = {
  'x-api-key': api_key,
  'Content-Type': 'application/json'
}


test = ['garden tomato', 'tomato', 'tomato plant']

list_id = set()
list_name = set()

for t in test:
  threshold = 0.4
  result = IngredientID.objects.annotate(similarity=TrigramSimilarity("name", t)).filter(similarity__gt=threshold).order_by("-similarity")
  print(f"Results {result}.")
  print(f"Results for '{t}':")
  if result :
    for r in result:
      print(f" - {r.name} (similarity: {r.similarity})")
      list_id.add(r.id_ingredients)  
      list_name.add(r.name)  


print(f" Set: {list_id}")
print(f" Set: {list_name}")

amount = 150
unit = 'grams'   
api_key1= 'cfe862eb5b72450185899fbba7ec215c'
headers_spoon = {
  'x-api-key': api_key1,
  'Content-Type': 'application/json'
}

for l in list_id:
    url_ingredient = f"https://api.spoonacular.com/food/ingredients/{l}/information?amount={amount}&unit={unit}"
    response_ingredient = requests.get(url_ingredient, headers=headers_spoon)
    data_Ingredient = response_ingredient.json()
    print(f" response from ingredient {l} ...{response_ingredient.status_code}")



number = 5
ranking = 1

for l in list_name:
  url2 = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={l}&number={number}&ranking={ranking}"
  response_name = requests.get(url2, headers=headers)
  data_recepy = response_name.json()
  print(f" response from recepy {l} ...{response_name.status_code}")


from django.db.models import F
from django.contrib.postgres.search import TrigramSimilarity

