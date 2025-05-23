from .birth_create_service import BirthRegistrationCreateService
from .birth_search_service import BirthRegistrationSearchService
from .birth_update_service import BirthRegistrationUpdateService

class BirthRegistrationService:
    def __init__(self):
        self.create_service = BirthRegistrationCreateService()
        self.search_service = BirthRegistrationSearchService()
        self.update_service = BirthRegistrationUpdateService()

    def create_birth_registration(self, app_data, request_info):
        return self.create_service.create_birth_registration(app_data, request_info)

    def update_birth_registration(self, app_data, request_info):
        return self.update_service.update_birth_registration(app_data, request_info)

    def search_birth_registrations(self, tenant_id=None, statuses=None, ids=None, app_num=None):
        return self.search_service.search_birth_registrations(tenant_id, statuses, ids, app_num) 