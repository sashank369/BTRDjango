from ..models import BirthRegistrationApplication
from digit_client.services import WorkflowV2Service
from digit_client.models import ProcessInstance
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from typing import Dict, Any

class BirthRegistrationUpdateService:
    def __init__(self):
        self.wf_service = WorkflowV2Service()

    def update_birth_registration(self, app_data, request_info):
        """
        Update birth registration application with error handling
        
        Args:
            app_data: Dictionary containing application data to update
            request_info: Dictionary containing request information
            
        Returns:
            BirthRegistrationApplication: Updated application object
            
        Raises:
            ObjectDoesNotExist: If application not found
            ValidationError: If data validation fails
            Exception: For other unexpected errors
        """
        try:
            # Validate required data
            if not app_data:
                raise ValidationError("Application data cannot be empty")

            # Find the application
            try:
                if 'id' in app_data:
                    app = BirthRegistrationApplication.objects.get(id=app_data['id'])
                elif 'applicationNumber' in app_data:
                    app = BirthRegistrationApplication.objects.get(
                        application_number=app_data['applicationNumber'])
                else:
                    raise ValidationError("Either 'id' or 'applicationNumber' must be provided")
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist("Birth registration application not found")

            # Update fields
            try:
                if 'status' in app_data:
                    app.status = app_data['status']
                if 'babyFirstName' in app_data:
                    app.baby_first_name = app_data['babyFirstName']
                if 'babyLastName' in app_data:
                    app.baby_last_name = app_data['babyLastName']
                
                # Validate the model before saving
                app.full_clean()
                app.save()
                return app
                
            except ValidationError as e:
                raise ValidationError(f"Invalid data provided: {str(e)}")
            except Exception as e:
                raise Exception(f"Error updating application: {str(e)}")

        except Exception as e:
            # Log the error here if you have logging configured
            raise Exception(f"Failed to update birth registration: {str(e)}")

    # def _start_workflow(self, birth_app, request_info, action="APPLY"):
    #     try:
    #         proc_inst = ProcessInstance(
    #             tenant_id=birth_app.tenant_id,
    #             business_service="BTR",
    #             business_id=birth_app.application_number,
    #             action=action,
    #             module_name="birth-services"
    #         )
    #         self.wf_service.transition_process([proc_inst], request_info=request_info)
    #     except Exception as e:
    #         raise Exception(f"Workflow transition failed: {str(e)}") 