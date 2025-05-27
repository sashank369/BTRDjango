# birth_app/serializers.py
from rest_framework import serializers
from .models import BirthRegistrationApplication

class RequestInfoSerializer(serializers.Serializer):
    apiId = serializers.CharField()
    ver = serializers.CharField()
    ts = serializers.IntegerField()
    action = serializers.CharField(required=False, allow_blank=True)
    did = serializers.CharField(required=False, allow_blank=True)
    key = serializers.CharField(required=False, allow_blank=True)
    msgId = serializers.CharField(required=False, allow_blank=True)
    requesterId = serializers.CharField(required=False, allow_blank=True)
    authToken = serializers.CharField(required=False, allow_blank=True)
    userInfo = serializers.JSONField(required=False)
    correlationId = serializers.CharField(required=False, allow_blank=True)

class BirthRegistrationApplicationSerializer(serializers.ModelSerializer):
    # Map snake_case model fields to spec's camelCase JSON keys
    babyFirstName = serializers.CharField(source='baby_first_name')
    babyLastName = serializers.CharField(source='baby_last_name', allow_blank=True)
    fatherOfApplicant = serializers.CharField(source='father_of_applicant')
    motherOfApplicant = serializers.CharField(source='mother_of_applicant')
    fatherMobileNumber = serializers.CharField(source='father_mobile_number', allow_blank=True)
    motherMobileNumber = serializers.CharField(source='mother_mobile_number', allow_blank=True)
    doctorName = serializers.CharField(source='doctor_name', allow_blank=True)
    hospitalName = serializers.CharField(source='hospital_name', allow_blank=True)
    placeOfBirth = serializers.CharField(source='place_of_birth', allow_blank=True)
    timeOfBirth = serializers.IntegerField(source='time_of_birth')
    tenantId = serializers.CharField(source='tenant_id')
    applicationNumber = serializers.CharField(source='application_number', read_only=True)
    address = serializers.JSONField(required=False, allow_null=True)
    applicant = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta:
        model = BirthRegistrationApplication
        # Expose JSON keys (field order here is illustrative)
        fields = ['id', 'tenantId', 'applicationNumber',
                  'babyFirstName', 'babyLastName', 'fatherOfApplicant', 'motherOfApplicant',
                  'fatherMobileNumber', 'motherMobileNumber', 'doctorName', 'hospitalName',
                  'placeOfBirth', 'timeOfBirth', 'address', 'applicant', 'status']

    def get_applicant(self, obj):
        # Return minimal user info if created
        if obj.applicant_user_id:
            return {"id": obj.applicant_user_id}
        return None

class BirthRegistrationRequestSerializer(serializers.Serializer):
    RequestInfo = RequestInfoSerializer()
    BirthRegistrationApplications = serializers.ListSerializer(
        child=BirthRegistrationApplicationSerializer()
    )

class ResponseInfoSerializer(serializers.Serializer):
    apiId = serializers.CharField()
    ver = serializers.CharField()
    ts = serializers.IntegerField()
    resMsgId = serializers.CharField()
    msgId = serializers.CharField()
    status = serializers.CharField()

class BirthRegistrationResponseSerializer(serializers.Serializer):
    ResponseInfo = ResponseInfoSerializer()
    BirthRegistrationApplications = serializers.ListSerializer(
        child=BirthRegistrationApplicationSerializer()
    )