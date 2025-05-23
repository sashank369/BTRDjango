from digit_client.services.workflow import WorkflowV2Service
from digit_client.models.workflow import WorkflowAction,  WorkflowActionBuilder, ProcessInstanceBuilder, ProcessInstanceSearchCriteriaBuilder
from digit_client.models import BusinessServiceBuilder, StateBuilder, Role, UserBuilder,BusinessServiceSearchCriteria,BusinessServiceSearchCriteriaBuilder
from digit_client import RequestConfig, RoleBuilder


auth_token = "ed781948-9805-4dd8-a664-e8581524e8c8"


RequestConfig.initialize(
    api_id="DIGIT-CLIENT",
    version="1.0.0",
    # user_info=user_info.to_dict(),
    auth_token=auth_token
)
workflow_service = WorkflowV2Service()
    
# Create search criteria
search_criteria = ProcessInstanceSearchCriteriaBuilder()\
    .with_tenant_id("DIGITCLIENT")\
    .with_business_service("BTRNEWSERVICE")\
    .with_business_ids(["fcc91d4d-169e-40a3-9e08-4c76bd81fc74"])\
    .with_status("Initial")\
    .build()

# Get request info
request_info = RequestConfig.get_request_info(
    action="POST",
    msg_id="5bfa85e7-dfa1-47c8-98b2-747bf552be86"
)

# Make the search request
result = workflow_service.search_processes(
    search_criteria=search_criteria,
    request_info=request_info
)

print("Search Result:", result)
