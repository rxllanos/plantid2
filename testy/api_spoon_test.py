import requests
import json
import os
import django
from django.contrib.postgres.search import TrigramSimilarity
from django.db import models, IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantas.settings')
django.setup()

from planta.models import IngredientID, Plant_data, Ingredient, NutrientDetail, Property, Flavonoid, CaloricBreakdown, WeightPerServing, Recepy, IngredientRecepy

api_key= 'cfe862eb5b72450185899fbba7ec215c'
headers_spoon = {
  'x-api-key': api_key,
  'Content-Type': 'application/json'
}

# def save_recepy(ing_n):
#     print('_____')
#     ingr = Ingredient.objects.filter(ingredient_original_name=ing_n).first()
#     print(f"running api for ingredient with name {ing_n}")
    
#     # with transaction.atomic():
#     number = 3
#     ranking = 1
#     url_recepy = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingr}&number={number}&ranking={ranking}"
#     response_recepy = requests.get(url_recepy, headers=headers_spoon)
#     data_recepy = response_recepy.json()        
#     print(f" received api recepy for {ing_n}: {response_recepy.status_code}")
#     with open(f'api_response_recepy_{ing_n}.json', 'w') as json_file:
#         json.dump([data_recepy], json_file)   


#     print(json.dumps(data_recepy, indent=2))

#     while True:
#         keyword = input("Enter 'resume' to continue: ").strip().lower()
#         if keyword == 'resume':
#             break
#         else:
#             print("Incorrect keyword. Please try again.") 

#     for recipe in data_recepy:
#         try:
#             print(f" id_recepy : {recipe['id']}")
#             print(f" title: {recipe['title']}")
#             print(f" image : {recipe['image']}")
#             print(f" used_ingredient_count : {recipe['usedIngredientCount']}")
#             print(f" missed_ingredient_count : {recipe['missedIngredientCount']}")
#             r = Recepy.objects.create(
#                 recepy_ingredient = ingr,
#                 recepy_id_recepy = recipe['id'],
#                 recepy_title = recipe['title'],
#                 recepy_image = recipe['image'],
#                 recepy_used_ingredient_count = recipe['usedIngredientCount'],
#                 recepy_missed_ingredient_count = recipe['missedIngredientCount'],
#             )
#             print(f"Recepy {r.recepy_title} saved with used ingredient  : {r.recepy_used_ingredient_count} ,and missed ingredients: {r.recepy_missed_ingredient_count}.")
        
#             print('----Recepy Ingredients...')
#             print(f" --Missed Ingredients")
#         except Exception as e:
#                 logging.error(f"Error occurred while creating Recepy: {e}")
#                 continue
#         try:
#             for ingredient_data in recipe['missedIngredients']:
            
#                 print(f" recepy: {r}")
#                 print(f" id : {ingredient_data['id']}")
#                 print(f" amount {ingredient_data['amount']}")
#                 print(f" unit : {ingredient_data['unit']}")
#                 print(f" name : {ingredient_data['name']}")
#                 print(f" meta : {ingredient_data['meta']}")
#                 print(f" image : {ingredient_data['image']}")

#                 ing = IngredientRecepy.objects.create(
#                     ingrecepy_recepy=r,
#                     ingrecepy_id_ingredientrecepy=ingredient_data['id'],
#                     ingrecepy_amount=ingredient_data['amount'],
#                     ingrecepy_unit=ingredient_data['unit'],
#                     ingrecepy_name=ingredient_data['name'],
#                     ingrecepy_meta=ingredient_data['meta'],
#                     ingrecepy_image=ingredient_data['image'],
#                     ingrecepy_is_missed=True
#                 )
#                 print(f"missedIngredient of Recepy {ing.ingrecepy_name}  saved.")
        
#             print(f" --Used Ingredients")
#             for ingredient_data in recipe['usedIngredients']:
#                 print(f" recepy: {r}")
#                 print(f" id : {ingredient_data['id']}")
#                 print(f" amount {ingredient_data['amount']}")
#                 print(f" unit : {ingredient_data['unit']}")
#                 print(f" name : {ingredient_data['name']}")
#                 print(f" meta : {ingredient_data['meta']}")
#                 print(f" image : {ingredient_data['image']}")

#                 IngredientRecepy.objects.create(
#                     ingrecepy_recepy=r,
#                     ingrecepy_id_ingredientrecepy=ingredient_data['id'],
#                     ingrecepy_amount=ingredient_data['amount'],
#                     ingrecepy_unit=ingredient_data['unit'],
#                     ingrecepy_name=ingredient_data['name'],
#                     ingrecepy_meta=ingredient_data['meta'],
#                     ingrecepy_image=ingredient_data['image'],
#                     ingrecepy_is_missed=False
#                 )
#                 print(f"used Ingredient of Recepy {ing.ingrecepy_name}  saved.")
#         except Exception as e:
#                 logging.error(f"Error occurred while creating Recepy: {e}")
#                 continue
#         print(f'Recepy saved!')
#     print("\n" + "-"*40 + "\n")


test = ['garden tomato', 'tomato', 'tomato plant']
plant = Plant_data.objects.filter(plant_data_gbif_id=2930137).first()

list_id = set()
list_name = set()

for t in test:
  threshold = 0.5
  result = IngredientID.objects.annotate(similarity=TrigramSimilarity("spoon_name", t)).filter(similarity__gt=threshold).order_by("-similarity")
  print(f"Results for '{t}': {result}")
  if result :
    for r in result:
      print(f" - {r.spoon_name} (similarity: {r.similarity})")
      list_id.add(r.spoon_id_ingredients)  
      list_name.add(r.spoon_name)  

print(f" Set: {list_id}")
print(f" Set: {list_name}")

while True:
    keyword = input("Enter 'resume' to continue: ").strip().lower()
    if keyword == 'resume':
        break
    else:
        print("Incorrect keyword. Please try again.")


amount = 150
unit = 'grams'   
for l in list_id:
  try:
    url_ingredient = f"https://api.spoonacular.com/food/ingredients/{l}/information?amount={amount}&unit={unit}"
    response_ingredient = requests.get(url_ingredient, headers=headers_spoon)
    data_Ingredient = response_ingredient.json()

    with open(f'api_response_ingredient_{l}.json', 'w') as json_file:
      json.dump([data_Ingredient], json_file)
    n = IngredientID.objects.filter(spoon_id_ingredients = l).first()
    print('_____')
    print(f" response from ingredient {l} ...{response_ingredient.status_code}")
    print(f" id: {data_Ingredient['id']}")
    print(f" name; {n.spoon_name}")
    print(f" amount: {data_Ingredient['amount']}")
    print(f" unit : {data_Ingredient['unit']}")
    print(f" pu: {data_Ingredient['possibleUnits']}")
    print(f" value : {data_Ingredient['estimatedCost']['value']}")
    print(f" cu : {data_Ingredient['estimatedCost']['unit']}")
    print(f" consistency : {data_Ingredient['consistency']}")
    print(f" image : {data_Ingredient['image']}")



    for dt in data_Ingredient:
      instance_ingredient = Ingredient.objects.create(
          ingredient_plant = plant,
          ingredient_id_Ingredient = data_Ingredient['id'],
          ingredient_original_name = n.spoon_name,
          ingredient_amount = data_Ingredient['amount'],
          ingredient_unit = data_Ingredient['unit'],
          ingredient_possible_units = data_Ingredient['possibleUnits'],
          ingredient_estimated_cost_value = data_Ingredient['estimatedCost']['value'],
          ingredient_estimated_cost_unit = data_Ingredient['estimatedCost']['unit'],
          ingredient_consistency = data_Ingredient['consistency'],
          ingredient_img = data_Ingredient['image'],
      )

      ing_n = instance_ingredient.ingredient_original_name
      save_recepy(ing_n)

      print(f"Ingredient {instance_ingredient.ingredient_original_name} saved.")
      print('----Ingredient Attributes ---')
      print(f" ingredient: {instance_ingredient}....")

      print(f" --Nutrient")
      for d in data_Ingredient['nutrition']['nutrients']:
        print(f" name; {d['name']}")
        print(f" amount: {d['amount']}")
        print(f" unit : {d['unit']}")
        print(f" percent_of_daily_needs: {d['percentOfDailyNeeds']}")   
        try:       
          n =NutrientDetail.objects.create(
              nutrient_ingredient = instance_ingredient,
              nutrient_name = d['name'],
              nutrient_amount = d['amount'],
              nutrient_unit = d['unit'],
              nutrient_percent_of_daily_needs = d['percentOfDailyNeeds'],              
          )
          print(f"Nutrients {n.nutrient_name} saved.")

        except ValidationError as e:
            print(f"Validation Error: {e.message_dict}")
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
        except DatabaseError as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  

      print(f" ---Properties")
      for d in data_Ingredient['nutrition']['properties']:
        print(f" name; {d['name']}")
        print(f" amount: {d['amount']}")
        print(f" unit : {d['unit']}")
        try:      
          p = Property.objects.create(
              property_ingredient = instance_ingredient,
              property_name = d['name'],
              property_amount = d['amount'],
              property_unit = d['unit'],         
          )
          print(f"Properties {p.property_name} saved.")
        except ValidationError as e:
            print(f"Validation Error: {e.message_dict}")
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
        except DatabaseError as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  

      print(f" ---flavonoids")
      for d in data_Ingredient['nutrition']['flavonoids']:
        print(f" name; {d['name']}")
        print(f" amount: {d['amount']}")
        print(f" unit : {d['unit']}")
        try:  
          f= Flavonoid.objects.create(
              flavonoid_ingredient = instance_ingredient,
              flavonoid_name = d['name'],
              flavonoid_amount = d['amount'],
              flavonoid_unit = d['unit'],             
          )
          print(f"Flavonoids  {f.flavonoid_name} saved.")
        except ValidationError as e:
            print(f"Validation Error: {e.message_dict}")
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
        except DatabaseError as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  

      print(f" ---Caloric breakdown")
      print(f" % proteint; {data_Ingredient['nutrition']['caloricBreakdown']['percentProtein']}")
      print(f" % fat: {data_Ingredient['nutrition']['caloricBreakdown']['percentFat' ]}")
      print(f" % carbs : {data_Ingredient['nutrition']['caloricBreakdown']['percentCarbs']}")
      try:
        CB = CaloricBreakdown.objects.create(
            cb_ingredient = instance_ingredient,
            cb_percent_protein = data_Ingredient['nutrition']['caloricBreakdown']['percentProtein'],
            cb_percent_fat =data_Ingredient['nutrition']['caloricBreakdown']['percentFat' ],
            cb_percent_carbs = data_Ingredient['nutrition']['caloricBreakdown']['percentCarbs'],
        )
        print(f"Caloric Breakdown {CB.cb_ingredient} saved.")

      except ValidationError as e:
          print(f"Validation Error: {e.message_dict}")
      except IntegrityError as e:
          print(f"Integrity Error: {e}")
      except DatabaseError as e:
          print(f"Database Error: {e}")
      except Exception as e:
          print(f"An unexpected error occurred: {e}")  

      print(f" ---Weight per Serving")
      print(f" % amount; {data_Ingredient['nutrition']['weightPerServing']['amount']}")
      print(f" % unit: {data_Ingredient['nutrition']['weightPerServing']['unit']}")
      try:  
        WPS = WeightPerServing.objects.create(
            wps_ingredient = instance_ingredient,
            wps_amount = data_Ingredient['nutrition']['weightPerServing']['amount'],
            wps_unit = data_Ingredient['nutrition']['weightPerServing']['unit'],      
        )
        print(f"Weight {WPS.wps_amount} and {WPS.wps_unit} saved.")

        print(f" ---End Ingredient----------")       
      except ValidationError as e:
          print(f"Validation Error: {e.message_dict}")
      except IntegrityError as e:
          print(f"Integrity Error: {e}")
      except DatabaseError as e:
          print(f"Database Error: {e}")
      except Exception as e:
          print(f"An unexpected error occurred: {e}")  
  except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred in ingredient: {err}') 
  except Exception as err:
    print(f'Other error occurred in ingredient: {err}')   


print(f" -----------End All Ingredients------------------------------------------")  

