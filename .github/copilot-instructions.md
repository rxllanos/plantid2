# PlantID2 AI Coding Guidelines

## Project Overview
PlantID2 is a Django-based web application for plant identification, health assessment, and nutritional analysis. Users upload plant images which are processed through external APIs to identify species, assess health, and analyze edible components using nutritional databases.

## Architecture
- **Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL with trigram similarity search for fuzzy matching
- **Storage**: AWS S3 for media and static files
- **Frontend**: Django templates with Crispy Forms and Bootstrap 5
- **APIs**: 
  - Plant.id API for plant identification and health assessment
  - Spoonacular API for ingredient nutritional data and recipes

### Core Apps
- `accounts`: Custom user authentication with profile photos
- `planta`: Main application handling plant data, API integrations, and business logic

### Data Flow
1. User uploads plant image via `PlantPictureForm`
2. `post_save` signal on `Plant` model triggers identification via Plant.id API
3. Plant data saved to `Plant_data` model
4. Health assessment performed; diseases saved if unhealthy
5. Edible plants trigger ingredient matching using trigram similarity against Spoonacular database
6. Nutritional data fetched and stored in related models (NutrientDetail, Property, Flavonoid, etc.)

## Key Models & Relationships
- `Plant` → `Plant_data` (1:1), `HealthAssessment` (1:1)
- `HealthAssessment` → `DiseaseSuggestion` (1:many)
- `Plant_data` → `Ingredient` (1:many)
- `Ingredient` → `NutrientDetail`, `Property`, `Flavonoid`, `CaloricBreakdown`, `WeightPerServing` (1:many each)
- `Ingredient` → `Recepy` → `IngredientRecepy` (recipe relationships)

## Critical Workflows

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables in .env
# Required: SECRET_KEY, DEBUG, RDS_* (PostgreSQL), AWS_*, Head_Plant, Head_Spoon

# Run migrations
python manage.py migrate

# Import ingredient database (requires CSV/Excel file)
python manage.py import_file_data path/to/ingredients.csv

# Start development server
python manage.py runserver
```

### API Integration Patterns
- **Plant.id API**: Use `imagefield_to_base64()` to encode images, send latitude/longitude for location-aware results
- **Spoonacular API**: Fuzzy match plant names to ingredient IDs using `TrigramSimilarity`, fetch detailed nutritional data
- **Headers**: Stored in `formulas.py`, loaded via `decouple.config()`

### Signal-Based Processing
All API calls happen asynchronously via Django signals in `signals.py`. Never call APIs directly in views - rely on model post_save signals.

### Ingredient Matching
```python
# Example pattern for fuzzy matching
from django.contrib.postgres.search import TrigramSimilarity
results = IngredientID.objects.annotate(
    similarity=TrigramSimilarity("spoon_name", search_term)
).filter(similarity__gt=0.5).order_by("-similarity")
```

### File Handling
- Images uploaded to `Plant.plant_image` are automatically processed by signals
- Use `imagefield_to_base64()` for API payloads
- Media files stored on AWS S3 with custom domain configuration

### API Endpoints
REST API views in `views.py` follow pattern:
- Query by plant access token or ingredient name
- Return serialized data from related models
- Handle 404s for missing data

### Testing
- API test files in `testy/` directory
- Use JSON fixtures for API response mocking
- Test signal processing with sample images

## Code Patterns
- **Error Handling**: Wrap API calls in try/except blocks, log errors but don't fail silently
- **Database Transactions**: Use `@transaction.atomic()` for multi-model saves
- **Model Defaults**: Many fields have default values (0, '', False) to handle API variability
- **Naming**: Models use verbose names (e.g., `plant_data_name`), fields prefixed with model name
- **Serialization**: DRF serializers for all API responses

## Common Gotchas
- Plant.id API requires base64-encoded images without data URL prefix
- Spoonacular ingredient IDs must be matched via fuzzy search - exact name matching rarely works
- Signals run synchronously - long API calls can block response
- PostgreSQL trigram extension required for similarity searches
- AWS S3 configuration affects media URL generation

## Dependencies
- `python-decouple` for environment variables
- `django-storages` + `boto3` for S3 integration
- `psycopg2-binary` for PostgreSQL with trigram support
- `pandas` for bulk data import
- `requests` for API calls</content>
<parameter name="filePath">/Users/ricardollanos/plantid2/.github/copilot-instructions.md