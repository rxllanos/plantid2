# myapp/management/commands/import_file_data.py

from django.core.management.base import BaseCommand
import pandas as pd
from planta.models import IngredientID
import os

class Command(BaseCommand):
    help = 'Import data from an Excel or CSV file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel or CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        file_extension = os.path.splitext(file_path)[1]

        try:
            if file_extension == '.xlsx' or file_extension == '.xls':
                df = pd.read_excel(file_path)
            elif file_extension == '.csv':
                df = pd.read_csv(file_path)
            else:
                self.stdout.write(self.style.ERROR('Unsupported file format'))
                return

            for _, row in df.iterrows():
                IngredientID.objects.create(
                    spoon_name=row['spoon_name'],
                    spoon_id_ingredients=row['spoon_id_ingredients'],
                )
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import data: {e}'))
