# Handle applicant creation if needed
from digit_client import CitizenUserBuilder, RequestConfig, RoleBuilder
from digit_client.services import UserService
from digit_client.models import ProcessInstance, Role, UserBuilder, StateBuilder, WorkflowActionBuilder, ProcessInstanceBuilder
from digit_client.services.idrequest import IdRequestService
from digit_client.models import IdRequest, IdRequestBuilder,Role,UserBuilder
from digit_client.request_config import RequestConfig, RequestInfo

auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
user_service = UserService()
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
# userinfo = (UserBuilder()
#     .with_id(10)
#     .with_user_name("sashank")
#     .with_tenant_id("DIGITCLIENT")
#     .with_type("CITIZEN")
#     .with_roles(roles)
#     .with_mobile_number("9353822215")
#     .with_email("sashank.budideti@egovernments.org")
#     .with_name("Sashank")
#     .with_uuid("123567102")
#     .build())
RequestConfig.initialize(
            api_id="DIGIT-CLIENT",
            version="1.0.0",
            # user_info=userinfo.to_dict(),
            auth_token=auth_token
        )

user_id = None
user_response = None

basic_citizen = (CitizenUserBuilder()
    .with_user_name("29225109")
    .with_password("Mus@123NK")
    .with_name("maqwkskd")
    .with_gender("MALE")
    .with_roles(roles)
    .with_mobile_number("9291909291")
    .with_tenant_id("DIGITCLIENT")
    .build())



# print("basic_citizen", basic_citizen.to_dict())
user_response = user_service.create_user_no_validate(basic_citizen)
# user_id = user_response.get('user', {}).get('id')
users = user_response.get('user', [])
print("user response", user_response)
user_id = users[0].get('id') if users and isinstance(users[0], dict) else None


# print("\nuser response", user_response)
print("user_id:\n", user_id)