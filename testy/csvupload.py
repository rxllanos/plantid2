import os
import django
# import pandas as pd
from django.contrib.postgres.search import TrigramSimilarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantas.settings')
django.setup()

from planta.models import IngredientID

name = 'tomato'
data2 = IngredientID.objects.filter(name__iregex=r'^' + name)
for dt in data2:
    print(dt)

print(f'Name: {name}')
data3 = IngredientID.objects.annotate(
    similarity=TrigramSimilarity('name', name),
).filter(similarity__gt=0.3).order_by('-similarity')

for dt in data3:
    print(dt)


print(f' Fist: {data3.first().id_ingredients}')



# data = pd.read_csv('ingredients.csv', delimiter=';')
# print(data.columns)



# for index, row in data.iterrows():
#     model_instance = IngredientID(
#         name=row['name'],
#         id=row['id'],
#     )
#     model_instance.save()
