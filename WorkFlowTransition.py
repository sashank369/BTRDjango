from digit_client.services.workflow import WorkflowV2Service
from digit_client.models.workflow import WorkflowAction,  WorkflowActionBuilder, ProcessInstanceBuilder
from digit_client.models import BusinessServiceBuilder, StateBuilder, Role, UserBuilder,BusinessServiceSearchCriteria,BusinessServiceSearchCriteriaBuilder
from digit_client import RequestConfig, RoleBuilder


auth_token = "ed781948-9805-4dd8-a664-e8581524e8c8"
roles = [
        Role(
            name="EMPLOYEE",
            code="EMPLOYEE",
            tenant_id="DIGITCLIENT"
        ),
        Role(
            name="CITIZEN",
            code="CITIZEN",
            tenant_id="DIGITCLIENT"
        ),
        Role(
            name="ADMIN",
            code="ADMIN",
            tenant_id="DIGITCLIENT"
        )
    ]
user_info = (UserBuilder()
    .with_id(53745)
    .with_user_name("292251901")
    .with_tenant_id("DIGITCLIENT")
    .with_roles(roles)
    .with_mobile_number("9291909291")
    .with_name("maqwkskd")
    .with_uuid("3103ea74-ab20-4712-af8a-144845e4e00e")
    .build())

print("user_info:\n",user_info);

# Initialize RequestConfig with user info 
# user_info=user_info.to_dict(),
RequestConfig.initialize(
    api_id="DIGIT-CLIENT",
    version="1.0.0",
    user_info=user_info.to_dict(),
    auth_token=auth_token
)

workflow_service = WorkflowV2Service()
    
# Create state for transition
state = StateBuilder()\
    .with_uuid("1dbcc81d-9e5d-4255-9f3c-19258e9341e8")\
    .build()

# Create workflow action
# action = WorkflowActionBuilder()\
#     .with_action("APPLY")\
#     .with_next_state("APPLIED")\
#     .with_roles(["EMPLOYEE","CITIZEN"])\
#     .build()

# Create process instance
# .with_state(state)\
process_instance = ProcessInstanceBuilder()\
    .with_id("process-id")\
    .with_tenant_id("DIGITCLIENT")\
    .with_business_service("BTR1")\
    .with_business_id("5fb8382f-8840-4eec-88c3-76465b947e82")\
    .with_action("APPLY")\
    .with_module_name("birth-registration")\
    .build()

# Get request info
# request_info = RequestConfig.get_request_info(
#     action="POST",
#     msg_id="5bfa85e7-dfa1-47c8-98b2-747bf552be85"
# )

# Make the transition request
result = workflow_service.transition_process(
    process_instances=[process_instance],
    # request_info=request_info
)

print("Transition Result:", result)
    