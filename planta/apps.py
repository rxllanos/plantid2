from django.apps import AppConfig


class PlantaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'planta'

    def ready(self):
        import planta.signals  # noqa

