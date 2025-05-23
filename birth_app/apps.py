from django.apps import AppConfig
from django.conf import settings
from digit_client.config import Config
from digit_client.request_config import RequestConfig
import os
class BirthAppConfig(AppConfig):
    name = 'birth_app'
    def ready(self):
        Config.set_api_endpoint(settings.DIGIT_API_ENDPOINT)
        RequestConfig.initialize(
            api_id=settings.DIGIT_API_ID,
            version=settings.DIGIT_API_VERSION,
            auth_token=os.getenv("ACCESS_TOKEN")
            # If authentication is used, set auth_token/user_info here
        )
