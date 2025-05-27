from digit_client.services.idrequest import IdRequestService
from digit_client.models import IdRequest, IdRequestBuilder,Role,UserBuilder
from digit_client.request_config import RequestConfig, RequestInfo

# Initialize the IdRequest service
id_request_service = IdRequestService()
# Create user info
roles = [
    Role(
        name="Employee",
        code="EMPLOYEE",
        tenant_id="DIGITCLIENT"
    ),
    Role(
        name="System user",
        code="SYSTEM",
        tenant_id="DIGITCLIENT"
    ),
    Role(
        name="CITIZEN",
        code="CITIZEN",
        tenant_id="DIGITCLIENT"
    ),
    Role(
        name="Administrator",
        code="ADMIN",
        tenant_id="DIGITCLIENT"
    ),
    Role(
        name="Super User",
        code="SUPERUSER",
        tenant_id="DIGITCLIENT"
    ),


]

auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
user_info = UserBuilder()\
    .with_id(53804)\
    .with_user_name("29225109")\
    .with_uuid("8ef4d0ee-af66-48ad-b33a-1de51c604881")\
    .with_name("maqwkskd")\
    .with_type("CITIZEN")\
    .with_mobile_number("9291909291")\
    .with_roles(roles)\
    .with_tenant_id("DIGITCLIENT")\
    .build()

# Initialize RequestConfig with user info
RequestConfig.initialize(
    api_id="DIGIT-CLIENT",
    version="1.0.0",
    user_info=user_info.to_dict(),
    auth_token=auth_token
)
# Create an IdRequest object
id_request = IdRequestBuilder()\
    .with_id_name("btr.registrationid")\
    .with_tenant_id("DIGITCLIENT")\
    .with_format("")\
    .build()

# Generate IDs
result = id_request_service.generate_id(id_request)
print(result)