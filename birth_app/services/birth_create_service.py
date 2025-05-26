from ..models import BirthRegistrationApplication
from digit_client import CitizenUserBuilder, RequestConfig, RoleBuilder
from digit_client.services import UserService, WorkflowV2Service
from digit_client.models import ProcessInstance, Role, UserBuilder, StateBuilder, WorkflowActionBuilder, ProcessInstanceBuilder
import uuid
import os

class BirthRegistrationCreateService:
    def __init__(self):
        self.user_service = UserService()
        self.wf_service = WorkflowV2Service()   

    def create_birth_registration(self, app_data, request_info):
        # Validate required fields
        required_fields = ['tenantId', 'babyFirstName', 'fatherOfApplicant', 'motherOfApplicant', 'timeOfBirth']
        for field in required_fields:
            if not app_data.get(field):
                raise ValueError(f"Required field '{field}' is missing")

        # Handle applicant creation if needed
        auth_token = "ed781948-9805-4dd8-a664-e8581524e8c8"
        roles=[
            (RoleBuilder()
                .with_code("CITIZEN")
                .with_name("CITIZEN")
                .with_tenant_id("DIGITCLIENT")
                .build()),
            (RoleBuilder()
                .with_code("EMPLOYEE")
                .with_name("EMPLOYEE")
                .with_tenant_id("DIGITCLIENT")
                .build()),
            (RoleBuilder()
                .with_code("ADMIN") 
                .with_name("Administrator")
                .with_tenant_id("DIGITCLIENT")
                .build())
        ]
        userinfo = (UserBuilder()
            .with_id(10)
            .with_user_name("sashank.budideti@egovernments.org")
            .with_tenant_id("DIGITCLIENT")
            .with_type("CITIZEN")
            .with_roles(roles)
            .with_mobile_number("9353822215")
            .with_email("sashank.budideti@egovernments.org")
            .with_name("Sashank")
            .with_uuid("123567102")
            .build())
        RequestConfig.initialize(
                    api_id="DIGIT-CLIENT",
                    version="1.0.0",
                    user_info=userinfo.to_dict(),
                    auth_token=auth_token
                )
        applicant = app_data.get('fatherOfApplicant')
        user_id = None
        user_response = None
        if applicant:
            basic_citizen = (CitizenUserBuilder()
                .with_user_name("292251901")
                .with_password("Mus@123NK")
                .with_name("maqwkskd")
                .with_gender("MALE")
                .with_roles(roles)
                .with_mobile_number("9291909291")
                .with_tenant_id("DIGITCLIENT")
                .build())
            


            # print("basic_citizen", basic_citizen.to_dict())
            user_response = self.user_service.create_user_no_validate(basic_citizen)
            # user_id = user_response.get('user', {}).get('id')
            users = user_response.get('user', [])
            user_id = users[0].get('id') if users and isinstance(users[0], dict) else None


        # print("\nuser response", user_response)
        print("user_id:\n", user_id)

        birth_app = BirthRegistrationApplication.objects.create(
            tenant_id=app_data['tenantId'],
            baby_first_name=app_data['babyFirstName'],
            baby_last_name=app_data.get('babyLastName', ''),
            father_of_applicant=app_data['fatherOfApplicant'],
            mother_of_applicant=app_data['motherOfApplicant'],
            father_mobile_number=app_data.get('fatherMobileNumber', ''),
            mother_mobile_number=app_data.get('motherMobileNumber', ''),
            doctor_name=app_data.get('doctorName', ''),
            hospital_name=app_data.get('hospitalName', ''),
            place_of_birth=app_data.get('placeOfBirth', ''),
            time_of_birth=app_data['timeOfBirth'],
            address=app_data['address'],
            applicant_user_id=user_id,
            status=app_data.get('status', 'applied')
        )

        # Generate application number
        birth_app.application_number = f"BTR-{birth_app.id}"
        birth_app.save()

        # Start initial workflow
        # self._start_workflow(birth_app, request_info)
        
        # Process workflow transition
        # self._process_workflow_transition(birth_app, request_info)

        return birth_app, user_response

    # def _start_workflow(self, birth_app, request_info, action="APPLY"):
    #     proc_inst = ProcessInstance(
    #         tenant_id=birth_app.tenant_id,
    #         business_service="BTR",
    #         business_id=birth_app.application_number,
    #         action=action,
    #         module_name="birth-services"
    #     )
    #     self.wf_service.transition_process([proc_inst], request_info=request_info)

    # def _process_workflow_transition(self, birth_app, request_info):
    #     # Create user info with roles
    #     roles = [
    #         Role(
    #             name="Employee",
    #             code="EMPLOYEE",
    #             tenant_id=birth_app.tenant_id
    #         ),
    #         Role(
    #             name="System user",
    #             code="SYSTEM",
    #             tenant_id=birth_app.tenant_id
    #         )
    #     ]
        
    #     # Get auth token from environment
    #     auth_token = os.getenv("ACCESS_TOKEN")
        
    #     # Create user info
    #     user_info = UserBuilder()\
    #         .with_id(birth_app.applicant_user_id)\
    #         .with_user_name(str(uuid.uuid4()))\
    #         .with_uuid(str(uuid.uuid4()))\
    #         .with_type("EMPLOYEE")\
    #         .with_name(birth_app.father_of_applicant)\
    #         .with_mobile_number(birth_app.father_mobile_number)\
    #         .with_email(f"{birth_app.father_of_applicant.lower().replace(' ', '')}@egovernments.org")\
    #         .with_roles(roles)\
    #         .with_tenant_id(birth_app.tenant_id)\
    #         .build()
        
    #     # Initialize RequestConfig with user info
    #     RequestConfig.initialize(
    #         api_id="DIGIT-CLIENT",
    #         version="1.0.0",
    #         user_info=user_info.to_dict(),
    #         auth_token=auth_token
    #     )
        
    #     # Create state for transition
    #     state = StateBuilder()\
    #         .with_uuid(str(uuid.uuid4()))\
    #         .with_state("APPROVED")\
    #         .build()
        
    #     # Create workflow action
    #     action = WorkflowActionBuilder()\
    #         .with_action("APPROVE")\
    #         .with_uuid(str(uuid.uuid4()))\
    #         .with_next_state("APPROVED")\
    #         .with_roles(["EMPLOYEE"])\
    #         .build()
        
    #     # Create process instance
    #     process_instance = ProcessInstanceBuilder()\
    #         .with_id(str(uuid.uuid4()))\
    #         .with_tenant_id(birth_app.tenant_id)\
    #         .with_business_service("BTR")\
    #         .with_business_id(birth_app.application_number)\
    #         .with_action("APPROVE")\
    #         .with_state(state)\
    #         .with_module_name("birth-services")\
    #         .build()
        
    #     # Get request info
    #     request_info = RequestConfig.get_request_info(
    #         action="POST",
    #         msg_id=str(uuid.uuid4())
    #     )
        
    #     # Make the transition request
    #     result = self.wf_service.transition_process(
    #         process_instances=[process_instance],
    #         request_info=request_info
    #     )
        
    #     print("Transition Result:", result) 