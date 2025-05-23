from digit_client.services.workflow import WorkflowV2Service
from digit_client.models.workflow import WorkflowAction
from digit_client.models import BusinessServiceBuilder, StateBuilder, UserBuilder
from digit_client import RequestConfig, RoleBuilder


auth_token = "36d3e03d-1b29-42d3-8290-f3fd9ae5c6fa"
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

# States definition
print("Creating states...")
applied_state = StateBuilder()\
    .with_state("APPLIED")\
    .with_application_status("APPLIED")\
    .with_doc_upload_required(False)\
    .with_is_start_state(False)\
    .with_is_terminate_state(True)\
    .with_is_state_updatable(False)\
    .with_actions([
        WorkflowAction(action="APPROVE", next_state="APPROVED", roles=["EMPLOYEE"]),
        WorkflowAction(action="REJECT", next_state="REJECTED", roles=["EMPLOYEE"])
    ])\
    .build()

print("Creating approved state...")
approved_state = StateBuilder()\
    .with_state("APPROVED")\
    .with_application_status("APPROVED")\
    .with_doc_upload_required(False)\
    .with_is_start_state(False)\
    .with_is_terminate_state(False)\
    .with_is_state_updatable(False)\
    .with_actions([
        WorkflowAction(action="PAY", next_state="REGISTRATIONCOMPLETED", roles=["SYSTEM_PAYMENT", "CITIZEN", "EMPLOYEE"])
    ])\
    .build()

print("Creating rejected state...")
rejected_state = StateBuilder()\
    .with_state("REJECTED")\
    .with_application_status("REJECTED")\
    .with_doc_upload_required(False)\
    .with_is_start_state(False)\
    .with_is_terminate_state(True)\
    .with_is_state_updatable(False)\
    .with_actions(None)\
    .build()

print("Creating registration completed state...")
registration_completed_state = StateBuilder()\
    .with_state("REGISTRATIONCOMPLETED")\
    .with_application_status("REGISTRATIONCOMPLETED")\
    .with_doc_upload_required(False)\
    .with_is_start_state(False)\
    .with_is_terminate_state(True)\
    .with_is_state_updatable(False)\
    .with_actions(None)\
    .build()

print("Creating initial state...")
initial_state = StateBuilder()\
    .with_doc_upload_required(False)\
    .with_is_start_state(True)\
    .with_is_terminate_state(False)\
    .with_is_state_updatable(True)\
    .with_actions([
        WorkflowAction(action="APPLY", next_state="APPLIED", roles=["CITIZEN", "EMPLOYEE"])
    ])\
    .build()

# Business Service
business_service = BusinessServiceBuilder()\
    .with_tenant_id("DIGITCLIENT")\
    .with_business_service("BTR1")\
    .with_business("birth-registration")\
    .with_business_service_sla(432000000)\
    .with_states([
        initial_state,
        applied_state,
        approved_state,
        rejected_state,
        registration_completed_state
    ])\
    .build()

# Create the business service
result = workflow_service.create_business_service(
    business_services=[business_service]
)

print("Create Business Service Result:", result)

