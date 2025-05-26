from django.db import models


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True)
    code = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    created_by = models.BigIntegerField(blank=True)
    created_date = models.DateField(blank=True)
    last_modified_by = models.BigIntegerField(blank=True)
    last_modified_date = models.DateField(blank=True)
    tenant_id = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class AuditDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.CharField(max_length=256)
    last_modified_by = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created by {self.created_by}"


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.CharField(max_length=128)
    door_no = models.CharField(max_length=64, blank=True)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)
    address_id = models.CharField(max_length=64, blank=True)
    address_number = models.CharField(max_length=64, blank=True)
    type = models.CharField(max_length=64, blank=True)
    detail = models.TextField(blank=True)
    building_name = models.CharField(max_length=256, blank=True)
    street = models.CharField(max_length=256, blank=True)
    registration_id = models.CharField(max_length=64, blank=True)
    locality = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.building_name}, {self.street}"


class FatherApplicant(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=128, unique=True)
    user_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    dob = models.DateField(blank=True)
    gender = models.CharField(max_length=16)
    pan = models.CharField(max_length=16, blank=True)
    aadhaar_number = models.CharField(max_length=16, blank=True)
    alt_contact_number = models.CharField(max_length=15, blank=True)
    account_locked = models.BooleanField(default=False)
    pwd_expiry_date = models.DateTimeField(blank=True)
    locale = models.CharField(max_length=16, blank=True)
    type = models.CharField(max_length=64, blank=True)
    signature = models.TextField(blank=True)
    otp_reference = models.CharField(max_length=64, blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    active = models.BooleanField(default=True)
    tenant_id = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MotherApplicant(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=128, unique=True)
    user_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    dob = models.DateField(blank=True)
    gender = models.CharField(max_length=16)
    pan = models.CharField(max_length=16, blank=True)
    aadhaar_number = models.CharField(max_length=16, blank=True)
    alt_contact_number = models.CharField(max_length=15, blank=True)
    account_locked = models.BooleanField(default=False)
    pwd_expiry_date = models.DateTimeField(blank=True)
    locale = models.CharField(max_length=16, blank=True)
    type = models.CharField(max_length=64, blank=True)
    signature = models.TextField(blank=True)
    otp_reference = models.CharField(max_length=64, blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    active = models.BooleanField(default=True)
    tenant_id = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Workflow(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.CharField(max_length=128)
    business_service = models.CharField(max_length=128)
    business_id = models.CharField(max_length=128)
    module_name = models.CharField(max_length=128)
    action = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    assignees = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    created_by = models.CharField(max_length=128)
    last_modified_by = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_id


class BirthRegistrationApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    application_id = models.CharField(max_length=64, unique=True)
    tenant_id = models.CharField(max_length=128)
    application_number = models.CharField(max_length=128, unique=True)
    baby_first_name = models.CharField(max_length=128)
    baby_last_name = models.CharField(max_length=128, blank=True)
    father_mobile_number = models.CharField(max_length=15)
    mother_mobile_number = models.CharField(max_length=15)
    doctor_name = models.CharField(max_length=128)
    hospital_name = models.CharField(max_length=128)
    place_of_birth = models.CharField(max_length=128)
    time_of_birth = models.BigIntegerField(blank=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    father_of_applicant = models.ForeignKey(FatherApplicant, on_delete=models.SET_NULL, null=True)
    mother_of_applicant = models.ForeignKey(MotherApplicant, on_delete=models.SET_NULL, null=True)
    audit_details = models.OneToOneField(AuditDetails, on_delete=models.SET_NULL, null=True)
    workflow = models.OneToOneField(Workflow, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.application_number
