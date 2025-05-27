from digit_client import RequestConfig, UserService, CitizenUserBuilder, RoleBuilder, UserBuilder, UserSearchModel,UserSearchModelBuilder
from pprint import pprint


# Initialize with default auth token
auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
# roles=[
#     (RoleBuilder()
#         .with_code("CITIZEN")
#         .with_name("Citizen")
#         .with_tenant_id("pg")
#         .build()),
#     (RoleBuilder()
#         .with_code("EMPLOYEE")
#         .with_name("Employee")
#         .with_tenant_id("pg")
#         .build()),
#     (RoleBuilder()
#         .with_code("ADMIN") 
#         .with_name("Administrator")
#         .with_tenant_id("pg")
#         .build())
# ]
# userinfo = (UserSearchModelBuilder()
#     .with_id(1)
#     .with_user_name("priyanhugupta753@gmail.com")
#     .with_tenant_id("pg")
#     .with_type("CITIZEN")
#     .with_roles(roles)
#     .with_mobile_number("9353822214")
#     .with_email("priyanhugupta753@gmail.com")
#     .with_name("Priyanhu Gupta")
#     .with_uuid("1234567890")
#     .build())


# First initialize with basic config
RequestConfig.initialize(
    api_id="DIGIT-CLIENT",
    version="1.0.0",
    # user_info=userinfo.to_dict(),
    auth_token=auth_token
)


# Create user service
user_service = UserService()

# Example 1: Create a basic citizen user with minimum required fields
basic_citizen = (UserSearchModelBuilder()  
    .with_id([53804])
    .with_tenant_id("DIGITCLIENT")
    .build())  # Will automatically add CITIZEN role




# Create citizen user
response = user_service.search_users(basic_citizen)
print("\nCreate Response:", response)

# Update user


