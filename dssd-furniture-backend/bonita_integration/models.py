# bonita_integration/models.py

from django.db import models
from authentication.models import User

class BonitaAPICall(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint_called = models.CharField(max_length=255)
    request_data = models.TextField()
    response_data = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.endpoint_called}"

class BonitaCookies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    BOS_Locale = models.CharField(max_length=255)
    JSESSIONID = models.CharField(max_length=255)
    X_Bonita_API_Token = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now_add=True,null=True)