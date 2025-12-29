from django.urls import path
from .views import (add, PlantAPIView, PlantDataAPIView, PlantHealthAPIView, 
                    PlantDeseaseAPIView, PlantIngredientAPIView, RecepyIngredientAPIView, RecepyAPIView,
                    WeightPerServingAPIView, CaloricBreakdownAPIView, FlavonoidAPIView, PropertyAPIView,
                    NutrientAPIView)

app_name = "planta"

urlpatterns = [
    path('add/', add, name='add'),
    path('api/planta/<str:pk>/', PlantAPIView.as_view(), name='plantapiview'),
    path('api/plantadata/<str:pk>/', PlantDataAPIView.as_view(), name='plantadatapiview'),
    path('api/plantahealth/<str:pk>/', PlantHealthAPIView.as_view(), name='plantahealthapiview'),
    path('api/plantadesease/<str:pk>/', PlantDeseaseAPIView.as_view(), name='plantadeseaseapiview'),
    path('api/plantaingredient/<str:pk>/', PlantIngredientAPIView.as_view(), name='plantaingredientapiview'),
    path('api/plantan/<str:pk>/', NutrientAPIView.as_view(), name='plantanapiview'),
    path('api/plantap/<str:pk>/', PropertyAPIView.as_view(), name='plantapapiview'),
    path('api/plantaf/<str:pk>/', FlavonoidAPIView.as_view(), name='plantafapiview'),
    path('api/plantacbd/<str:pk>/', CaloricBreakdownAPIView.as_view(), name='plantacbdapiview'),
    path('api/plantawps/<str:pk>/', WeightPerServingAPIView.as_view(), name='plantawpsapiview'),
    path('api/ingredientrecepy/<str:pk>/', RecepyAPIView.as_view(), name='plantarecepyapiview'),
    path('api/recepyingredient/<str:pk>/', RecepyIngredientAPIView.as_view(), name='plantarecepyingredientapiview'),
]