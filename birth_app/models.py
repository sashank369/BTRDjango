# birth_app/models.py
from django.db import models

class BirthRegistrationApplication(models.Model):
    tenant_id = models.CharField(max_length=128)
    application_number = models.CharField(max_length=64, unique=True, blank=True)
    baby_first_name = models.CharField(max_length=128)
    baby_last_name = models.CharField(max_length=128, blank=True)
    father_of_applicant = models.CharField(max_length=128)
    mother_of_applicant = models.CharField(max_length=128)
    father_mobile_number = models.CharField(max_length=15, blank=True)
    mother_mobile_number = models.CharField(max_length=15, blank=True)
    doctor_name = models.CharField(max_length=128, blank=True)
    hospital_name = models.CharField(max_length=128, blank=True)
    place_of_birth = models.CharField(max_length=128, blank=True)
    time_of_birth = models.BigIntegerField()  # epoch time of birth
    address = models.JSONField(null=True, blank=True)  # e.g. store the address object
    applicant_user_id = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=32, default='NEW')  # e.g. workflow state
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_number} ({self.tenant_id})"
