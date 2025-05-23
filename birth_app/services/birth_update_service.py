from ..models import BirthRegistrationApplication
from digit_client.services import WorkflowV2Service
from digit_client.models import ProcessInstance

class BirthRegistrationUpdateService:
    def __init__(self):
        self.wf_service = WorkflowV2Service()

    def update_birth_registration(self, app_data, request_info):
        # Find the application
        if 'id' in app_data:
            app = BirthRegistrationApplication.objects.get(id=app_data['id'])
        else:
            app = BirthRegistrationApplication.objects.get(
                application_number=app_data.get('applicationNumber'))

        # Update fields
        if 'status' in app_data:
            app.status = app_data['status']
        if 'babyFirstName' in app_data:
            app.baby_first_name = app_data['babyFirstName']
        if 'babyLastName' in app_data:
            app.baby_last_name = app_data['babyLastName']
        app.save()

        # Handle workflow if provided
        workflow = app_data.get('Workflow')
        if workflow:
            self._start_workflow(app, request_info, workflow.get('action', ''))

        return app

    def _start_workflow(self, birth_app, request_info, action="APPLY"):
        proc_inst = ProcessInstance(
            tenant_id=birth_app.tenant_id,
            business_service="BTR",
            business_id=birth_app.application_number,
            action=action,
            module_name="birth-services"
        )
        self.wf_service.transition_process([proc_inst], request_info=request_info) 