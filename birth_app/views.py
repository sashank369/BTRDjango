# birth_app/views.py
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BirthRegistrationApplication
from digit_client.request_config import RequestConfig
from .services.birth_service import BirthRegistrationService
from digit_client import UserService,UserSearchModelBuilder
from .utils.response_formatter import ResponseFormatter

# POST /v1/registration/_create
@api_view(['POST'])
def create_birth(request):
    try:
        data = request.data
        request_info = data.get('RequestInfo', {})
        applications = data.get('BirthRegistrationApplications', [])
        created_apps = []
        birth_service = BirthRegistrationService()
        req_info_obj = RequestConfig.get_request_info()

        for app_data in applications:
            birth_app, user_father_response, user_mother_response = birth_service.create_birth_registration(app_data, request_info)
            
            # Prepare response data for this application
            app_response = {
                'id': birth_app.id,
                'tenantId': birth_app.tenant_id,
                'applicationNumber': birth_app.application_number,
                'babyFirstName': birth_app.baby_first_name,
                'babyLastName': birth_app.baby_last_name,
                'doctorName': birth_app.doctor_name,
                'hospitalName': birth_app.hospital_name,
                'placeOfBirth': birth_app.place_of_birth,
                'timeOfBirth': birth_app.time_of_birth
            }

            if user_father_response:
                app_response['FatheruserServiceResponse'] = user_father_response
            if user_mother_response:
                app_response['MotheruserServiceResponse'] = user_mother_response

            created_apps.append(app_response)

        response_data = ResponseFormatter.format_success_response(request_info, created_apps)
        return Response(response_data, status=201)

    except ValueError as ve:
        response_data = ResponseFormatter.format_error_response(request_info, str(ve))
        return Response(response_data, status=400)
    except Exception as e:
        response_data = ResponseFormatter.format_error_response(request_info, str(e))
        return Response(response_data, status=400)

# POST /v1/registration/_update
@api_view(['POST'])
def update_birth(request):
    try:
        data = request.data
        request_info = data.get('RequestInfo', {})
        applications = data.get('BirthRegistrationApplications', [])
        updated_apps = []
        birth_service = BirthRegistrationService()
        req_info_obj = RequestConfig.get_request_info()

        for app_data in applications:
            app = birth_service.update_birth_registration(app_data, req_info_obj)
            
            # Prepare response data for this application
            updated_apps.append({
                'id': app.id,
                'tenantId': app.tenant_id,
                'applicationNumber': app.application_number,
                'babyFirstName': app.baby_first_name,
                'babyLastName': app.baby_last_name,
                'doctorName': app.doctor_name,
                'hospitalName': app.hospital_name,
                'placeOfBirth': app.place_of_birth,
                'timeOfBirth': app.time_of_birth
            })

        response_data = ResponseFormatter.format_success_response(request_info, updated_apps)
        return Response(response_data, status=200)

    except Exception as e:
        response_data = ResponseFormatter.format_error_response(request_info, str(e))
        return Response(response_data, status=400)

# POST /v1/registration/_search
@api_view(['POST'])
def search_birth(request):
    try:
        # Get query parameters
        tenant_id = request.query_params.get('tenantId')
        statuses = request.query_params.getlist('status')
        ids = request.query_params.getlist('ids')
        app_num = request.query_params.get('applicationNumber')

        # Search using service
        birth_service = BirthRegistrationService()
        apps = birth_service.search_birth_registrations(
            tenant_id=tenant_id,
            statuses=statuses,
            ids=ids,
            app_num=app_num
        )
        # Prepare response data
        applications = []
        for app in apps:
            father_details = get_father_details(app.Father_id) if app.Father_id else None
            mother_details = get_father_details(app.Mother_id) if app.Mother_id else None

            applications.append({
                'id': app.id,
                'tenantId': app.tenant_id,
                'applicationNumber': app.application_number,
                'babyFirstName': app.baby_first_name,
                'babyLastName': app.baby_last_name,
                'doctorName': app.doctor_name,
                'hospitalName': app.hospital_name,
                'placeOfBirth': app.place_of_birth,
                'timeOfBirth': app.time_of_birth,
                'FatherID': app.Father_id,
                'MotherID': app.Mother_id,
                'father': father_details,
                'mother': mother_details,
            })

        response_data = ResponseFormatter.format_success_response({}, applications)
        return Response(response_data)

    except Exception as e:
        response_data = ResponseFormatter.format_error_response({}, str(e))
        return Response(response_data, status=400)

def get_father_details(father_id):
    try:
        auth_token = "9d265031-5edc-4e3e-96ca-1bb087a6a517"
        RequestConfig.initialize(
            api_id="DIGIT-CLIENT",
            version="1.0.0",
            # user_info=userinfo.to_dict(),
            auth_token=auth_token
        )
        user_service = UserService()
        search_model = (
            UserSearchModelBuilder()
            .with_uuid([father_id])
            .with_tenant_id("DIGITCLIENT")
            .build()
        )
        response = user_service.search_users(search_model)
        if response and 'user' in response and response['user']:
            user_data = response['user'][0]
            return {
                'name': user_data.get('name'),
                'mobileNumber': user_data.get('mobileNumber'),
                'email': user_data.get('emailId'),
                'aadhaarNumber': user_data.get('aadhaarNumber'),
            }
        print("User Response \n:",response)
    except Exception as e:
        print(f"Error fetching user details for ID {father_id}: {e}")
    return None