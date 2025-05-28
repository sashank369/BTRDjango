from django.db import models


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    code = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_modified_by = models.BigIntegerField(blank=True, null=True)
    last_modified_date = models.DateField(blank=True, null=True)
    tenant_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class AuditDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.CharField(max_length=256, blank=True, null=True)
    last_modified_by = models.CharField(max_length=256, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"Created by {self.created_by}"


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.CharField(max_length=128)
    door_no = models.CharField(max_length=64, blank=True, null=True)
    latitude = models.CharField(max_length=64, blank=True, null=True)
    longitude = models.CharField(max_length=64, blank=True, null=True)
    address_number = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    building_name = models.CharField(max_length=256, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    registration_id = models.CharField(max_length=64, blank=True, null=True)
    locality = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.building_name}, {self.street}"


class FatherApplicant(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=128, unique=True)
    user_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    pan = models.CharField(max_length=16, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=16, blank=True, null=True)
    alt_contact_number = models.CharField(max_length=15, blank=True, null=True)
    account_locked = models.BooleanField(default=False)
    pwd_expiry_date = models.DateTimeField(blank=True, null=True)
    locale = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    otp_reference = models.CharField(max_length=64, blank=True, null=True)
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
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, blank=True, null=True)
    pan = models.CharField(max_length=16, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=16, blank=True, null=True)
    alt_contact_number = models.CharField(max_length=15, blank=True, null=True)
    account_locked = models.BooleanField(default=False)
    pwd_expiry_date = models.DateTimeField(blank=True, null=True)
    locale = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    otp_reference = models.CharField(max_length=64, blank=True, null=True)
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
    action = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    assignees = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=128)
    last_modified_by = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_id


class BirthRegistrationApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.CharField(max_length=128)
    application_number = models.CharField(max_length=128, unique=True)
    baby_first_name = models.CharField(max_length=128)
    baby_last_name = models.CharField(max_length=128, blank=True)
    doctor_name = models.CharField(max_length=128)
    hospital_name = models.CharField(max_length=128)
    place_of_birth = models.CharField(max_length=128)
    time_of_birth = models.BigIntegerField(blank=True, null=True)
    Father_id = models.CharField(max_length=128, null=True, blank=True)
    Mother_id = models.CharField(max_length=128, null=True, blank=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    father_of_applicant = models.ForeignKey(FatherApplicant, on_delete=models.SET_NULL, null=True)
    mother_of_applicant = models.ForeignKey(MotherApplicant, on_delete=models.SET_NULL, null=True)
    audit_details = models.OneToOneField(AuditDetails, on_delete=models.SET_NULL, null=True)
    workflow = models.OneToOneField(Workflow, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.application_number
