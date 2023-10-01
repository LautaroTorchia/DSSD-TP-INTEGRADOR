from django.db import models


class SystemRequest(models.Model):

    METHOD_OPTIONS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE')    
    ]

    denomination_command = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    url = models.CharField(max_length=255)
    headers = models.TextField(null=True)
    method = models.CharField(choices=METHOD_OPTIONS, max_length=10)
    data_request = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return self.denomination_command