import requests
import json
from django.contrib.postgres.search import TrigramSimilarity
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from planta.models import IngredientID, Plant_data, Ingredient, NutrientDetail, Property, Flavonoid, CaloricBreakdown, WeightPerServing, Plant_data
import requests
import json
from django.contrib.postgres.search import TrigramSimilarity
from django.db import transaction
import logging
from .formulas import save_recepy, headers_spoon

def save_plant_ingredient(plant_data_instance):
    if plant_data_instance.plant_data_edible_parts:  
        plant_common_names = plant_data_instance.plant_data_common_names

        list_id = set()
        list_name = set()

        for t in plant_common_names:
          threshold = 0.5
          result = IngredientID.objects.annotate(similarity=TrigramSimilarity("spoon_name", t)).filter(similarity__gt=threshold).order_by("-similarity")
          print(f"Results for '{t}': {result}")
          if result :
            for r in result:
              print(f" - {r.spoon_name} (similarity: {r.similarity})")
            #   all_plant_data = Plant_data.objects.filter(plant_data_name = plant_data_instance.plant_data_name).first()
            #   common_names_list_instance_exist = [plant.pd_common_names for plant in all_plant_data]
            #   if r.spoon_name not in common_names_list_instance_exist:
                 
              list_id.add(r.spoon_id_ingredients)  
              list_name.add(r.spoon_name)  

        print(f" Set: {list_id}")
        print(f" Set: {list_name}")

        amount = 150
        unit = 'grams'   
        for l in list_id:
          try:
            url_ingredient = f"https://api.spoonacular.com/food/ingredients/{l}/information?amount={amount}&unit={unit}"
            response_ingredient = requests.get(url_ingredient, headers=headers_spoon)
            data_Ingredient = response_ingredient.json()

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
                  ingredient_plant = plant_data_instance,
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
    else:
        print(f"Sorry {plant_data_instance.plant} is not eatable.")   


