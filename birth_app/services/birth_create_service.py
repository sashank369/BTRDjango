from ..models import BirthRegistrationApplication
from digit_client import CitizenUserBuilder, RequestConfig, RoleBuilder
from digit_client.services import UserService, WorkflowV2Service
from digit_client.models import ProcessInstance, Role, UserBuilder, StateBuilder, WorkflowActionBuilder, ProcessInstanceBuilder
from digit_client.services.idrequest import IdRequestService
from digit_client.models import IdRequest, IdRequestBuilder,Role,UserBuilder
from digit_client.request_config import RequestConfig, RequestInfo
from ..models import (
    BirthRegistrationApplication,
    AuditDetails,
    Workflow,
    Address,
    FatherApplicant,
    MotherApplicant
)
import uuid
import os

class BirthRegistrationCreateService:
    def __init__(self):
        self.user_service = UserService()
        self.wf_service = WorkflowV2Service()   

    def create_birth_registration(self, app_data, request_info):

        #-----------------------------------------------------------------------------------------------------------------------
        #Validator
        # Validate required fields
        required_fields = ['tenantId', 'babyFirstName', 'fatherOfApplicant', 'motherOfApplicant', 'timeOfBirth']
        for field in required_fields:
            if not app_data.get(field):
                raise ValueError(f"Required field '{field}' is missing")
            


        
        #-----------------------------------------------------------------------------------------------------------------------
        #Configs for client libararies
        auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
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
                .build()),
            (RoleBuilder()
                .with_code("SUPERUSER") 
                .with_name("Super User")
                .with_tenant_id("DIGITCLIENT")
                .build())
        ]
        RequestConfig.initialize(
                    api_id="DIGIT-CLIENT",
                    version="1.0.0",
                    auth_token=auth_token
                )


        #-----------------------------------------------------------------------------------------------------------------------
        # #Enrichment
        # id_request_service = IdRequestService()
        # # Create user info
        # roles = [
        #     Role(
        #         name="Employee",
        #         code="EMPLOYEE",
        #         tenant_id="LMN"
        #     ),
        #     Role(
        #         name="System user",
        #         code="SYSTEM",
        #         tenant_id="LMN"
        #     )
        # ]
        
        # auth_token = "0e9b955f-5e25-4809-b680-97ef37ccf53f"
        # user_info = UserBuilder()\
        #     .with_id(181)\
        #     .with_user_name("TestEggMUSTAKIMNK")\
        #     .with_uuid("4f6cf5fa-bcb2-4a3a-9dff-9740c04e3a92")\
        #     .with_type("EMPLOYEE")\
        #     .with_name("mustak")\
        #     .with_mobile_number("1234567890")\
        #     .with_email("xyz@egovernments.org")\
        #     .with_roles(roles)\
        #     .with_tenant_id("LMN")\
        #     .build()
        
        # # Initialize RequestConfig with user info
        # RequestConfig.initialize(
        #     api_id="DIGIT-CLIENT",
        #     version="1.0.0",
        #     user_info=user_info.to_dict(),
        #     auth_token=auth_token
        # )
        # # Create an IdRequest object
        # id_request = IdRequestBuilder()\
        #     .with_id_name("test_id_name")\
        #     .with_tenant_id("test_tenant_id")\
        #     .with_format("test_format")\
        #     .build()

        # # Generate IDs
        # result = id_request_service.generate_id(id_request)
        # print(result)








        #-----------------------------------------------------------------------------------------------------------------------
        #Create Birth Registration Application User Service
        # Handle applicant creation if needed
        
        
        applicant = app_data.get('fatherOfApplicant')
        user_id = None
        user_response = None
        if applicant:
            basic_citizen = (CitizenUserBuilder()
                .with_user_name(app_data.get('fatherOfApplicant', {}).get('userName', ''))
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
            print("user_response\n", user_response)
            users = user_response.get('user', [])
            user_id = users[0].get('id') if users and isinstance(users[0], dict) else None


        # print("\nuser response", user_response)
        print("user_id:\n", user_id)






        #-----------------------------------------------------------------------------------------------------------------------
        #Saving into database 
        address = Address.objects.create(
            tenant_id=app_data['tenantId'],
            door_no=app_data.get('address', {}).get('doorNo', ''),
            latitude=app_data.get('address', {}).get('latitude', ''),
            longitude=app_data.get('address', {}).get('longitude', ''),
            address_number=app_data.get('address', {}).get('addressNumber', ''),
            type=app_data.get('address', {}).get('type', ''),
            detail=app_data.get('address', {}).get('detail', ''),
            building_name=app_data.get('address', {}).get('buildingName', ''),
            street=app_data.get('address', {}).get('street', ''),
            locality=app_data.get('address', {}).get('locality', '')
        )
        father_applicant = FatherApplicant.objects.create(
            uuid=str(uuid.uuid4()),
            user_name=app_data.get('fatherOfApplicant', {}).get('userName', ''),
            name=app_data.get('fatherOfApplicant', {}).get('name', ''),
            mobile_number=app_data.get('fatherOfApplicant', {}).get('mobileNumber', ''),
            email=app_data.get('fatherOfApplicant', {}).get('email', ''),
            pan=app_data.get('fatherOfApplicant', {}).get('pan', ''),
            aadhaar_number=app_data.get('fatherOfApplicant', {}).get('aadhaarNumber', ''),
            alt_contact_number=app_data.get('fatherOfApplicant', {}).get('altContactNumber', ''),
            locale=app_data.get('fatherOfApplicant', {}).get('locale', ''),
            type=app_data.get('fatherOfApplicant', {}).get('type', ''),
            signature=app_data.get('fatherOfApplicant', {}).get('signature', ''),
            otp_reference=app_data.get('fatherOfApplicant', {}).get('otpReference', ''),
            tenant_id=app_data['tenantId']
        )
        mother_applicant = MotherApplicant.objects.create(
            uuid=str(uuid.uuid4()),
            user_name=app_data.get('motherOfApplicant', {}).get('userName', ''),
            name=app_data.get('motherOfApplicant', {}).get('name', ''),
            mobile_number=app_data.get('motherOfApplicant', {}).get('mobileNumber', ''),
            email=app_data.get('motherOfApplicant', {}).get('email', ''),
            dob=app_data.get('motherOfApplicant', {}).get('dob'),
            gender=app_data.get('motherOfApplicant', {}).get('gender', ''),
            pan=app_data.get('motherOfApplicant', {}).get('pan', ''),
            aadhaar_number=app_data.get('motherOfApplicant', {}).get('aadhaarNumber', ''),
            alt_contact_number=app_data.get('motherOfApplicant', {}).get('altContactNumber', ''),
            locale=app_data.get('motherOfApplicant', {}).get('locale', ''),
            type=app_data.get('motherOfApplicant', {}).get('type', ''),
            signature=app_data.get('motherOfApplicant', {}).get('signature', ''),
            otp_reference=app_data.get('motherOfApplicant', {}).get('otpReference', ''),
            tenant_id=app_data['tenantId']
        )
        audit_details = AuditDetails.objects.create(
            created_by=app_data.get('requestInfo', {}).get('userInfo', {}).get('uuid', ''),
            last_modified_by=app_data.get('requestInfo', {}).get('userInfo', {}).get('uuid', '')
        )
        workflow = Workflow.objects.create(
            tenant_id=app_data['tenantId'],
            business_service='BTR',
            business_id=str(uuid.uuid4()),
            module_name='birth-registration',
            action='CREATE',
            state='INITIATED',
            created_by=app_data.get('requestInfo', {}).get('userInfo', {}).get('uuid', ''),
            last_modified_by=app_data.get('requestInfo', {}).get('userInfo', {}).get('uuid', '')
        )
        birth_app = BirthRegistrationApplication.objects.create(
            id=user_id,
            tenant_id=app_data['tenantId'],
            application_number=app_data.get('applicationNumber', ''),
            baby_first_name=app_data['babyFirstName'],
            baby_last_name=app_data.get('babyLastName', ''),
            doctor_name=app_data.get('doctorName', ''),
            hospital_name=app_data.get('hospitalName', ''),
            place_of_birth=app_data.get('placeOfBirth', ''),
            time_of_birth=app_data.get('timeOfBirth'),
            address=address,
            father_of_applicant=father_applicant,
            mother_of_applicant=mother_applicant,
            audit_details=audit_details,
            workflow=workflow
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