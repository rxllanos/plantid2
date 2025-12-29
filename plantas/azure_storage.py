from storages.backends.azure_storage import AzureStorage
from decouple import config

class AzureMediaStorage(AzureStorage):
    account_name = config('AZURE_ACCOUNT_NAME')
    account_key = config('AZURE_ACCOUNT_KEY')
    azure_container = 'media-agriculture'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = config('AZURE_ACCOUNT_NAME')
    account_key = config('AZURE_ACCOUNT_KEY')
    azure_container = 'static-agriculture'
    expiration_secs = None