from digit_client.services.workflow import WorkflowV2Service
from digit_client.models.workflow import WorkflowAction
from digit_client.models import BusinessServiceBuilder, StateBuilder, Role, UserBuilder,BusinessServiceSearchCriteria,BusinessServiceSearchCriteriaBuilder
from digit_client import RequestConfig, RoleBuilder


auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
# roles=[
#     (RoleBuilder()
#         .with_code("CITIZEN")
#         .with_name("Citizen")
#         .with_tenant_id("DIGITCLIENT")
#         .build()),
#     (RoleBuilder()
#         .with_code("EMPLOYEE")
#         .with_name("Employee")
#         .with_tenant_id("DIGITCLIENT")
#         .build()),
#     (RoleBuilder()
#         .with_code("ADMIN") 
#         .with_name("Administrator")
#         .with_tenant_id("DIGITCLIENT")
#         .build())
# ]
# user_info = (UserBuilder()
#     .with_id(1)
#     .with_user_name("priyanhugupta753@gmail.com")
#     .with_tenant_id("DIGITCLIENT")
#     .with_type("CITIZEN")
#     .with_roles(roles)
#     .with_mobile_number("9353822214")
#     .with_email("priyanhugupta753@gmail.com")
#     .with_name("Priyanhu Gupta")
#     .with_uuid("8b23df51-3454-4939-98e8-ee090730cbd0")
#     .build())

# Initialize RequestConfig with user info
RequestConfig.initialize(
    api_id="DIGIT-CLIENT",
    version="1.0.0",
    # user_info=user_info.to_dict(),
    auth_token=auth_token
)

workflow_service = WorkflowV2Service()  

    # Create search criteria
search_criteria = BusinessServiceSearchCriteriaBuilder()\
    .with_tenant_id("DIGITCLIENT")\
    .with_business_services(["BTRN"])\
    .build()    
    

# Search business service
result = workflow_service.search_business_service(
    criteria=search_criteria
)       

print("Search Business Service Result:", result)
