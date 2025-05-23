# birth_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BirthRegistrationApplication
from digit_client.request_config import RequestConfig
from .services.birth_service import BirthRegistrationService
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
            birth_app, user_response = birth_service.create_birth_registration(app_data, request_info)
            
            # Prepare response data for this application
            app_response = {
                'id': birth_app.id,
                'tenantId': birth_app.tenant_id,
                'applicationNumber': birth_app.application_number,
                'babyFirstName': birth_app.baby_first_name,
                'babyLastName': birth_app.baby_last_name,
                'fatherOfApplicant': birth_app.father_of_applicant,
                'motherOfApplicant': birth_app.mother_of_applicant,
                'fatherMobileNumber': birth_app.father_mobile_number,
                'motherMobileNumber': birth_app.mother_mobile_number,
                'doctorName': birth_app.doctor_name,
                'hospitalName': birth_app.hospital_name,
                'placeOfBirth': birth_app.place_of_birth,
                'timeOfBirth': birth_app.time_of_birth,
                'address': birth_app.address,
                'status': birth_app.status
            }

            if user_response:
                app_response['userServiceResponse'] = user_response

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
                'fatherOfApplicant': app.father_of_applicant,
                'motherOfApplicant': app.mother_of_applicant,
                'fatherMobileNumber': app.father_mobile_number,
                'motherMobileNumber': app.mother_mobile_number,
                'doctorName': app.doctor_name,
                'hospitalName': app.hospital_name,
                'placeOfBirth': app.place_of_birth,
                'timeOfBirth': app.time_of_birth,
                'address': app.address,
                'status': app.status
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
        applications = [{
            'id': app.id,
            'tenantId': app.tenant_id,
            'applicationNumber': app.application_number,
            'babyFirstName': app.baby_first_name,
            'babyLastName': app.baby_last_name,
            'fatherOfApplicant': app.father_of_applicant,
            'motherOfApplicant': app.mother_of_applicant,
            'fatherMobileNumber': app.father_mobile_number,
            'motherMobileNumber': app.mother_mobile_number,
            'doctorName': app.doctor_name,
            'hospitalName': app.hospital_name,
            'placeOfBirth': app.place_of_birth,
            'timeOfBirth': app.time_of_birth,
            'address': app.address,
            'status': app.status
        } for app in apps]

        response_data = ResponseFormatter.format_success_response({}, applications)
        return Response(response_data)

    except Exception as e:
        response_data = ResponseFormatter.format_error_response({}, str(e))
        return Response(response_data, status=400)
