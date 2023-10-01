# bonita_integration/models.py

from django.db import models

class BonitaAPICall(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint_called = models.CharField(max_length=255)
    request_data = models.TextField()
    response_data = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.endpoint_called}"
