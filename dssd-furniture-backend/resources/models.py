from django.db import models

class Resource(models.Model):

    LANGUAGE_ASSESSMENT_OPTIONS = [
        ('eng', 'eng'),
        ('spa', 'spa'),
        ('fr', 'fr')
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    language = models.CharField(choices=LANGUAGE_ASSESSMENT_OPTIONS, max_length=7)    
    content = models.TextField(default='TODO')
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.name

class ConfigMessage(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    content = models.TextField()    
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.name

class UserTranslation(models.Model):

    LANGUAGE_ASSESSMENT_OPTIONS = [
        ('eng', 'eng'),
        ('spa', 'spa'),
        ('fr', 'fr')
    ]

    id_message_config = models.ForeignKey(to=ConfigMessage, on_delete=models.CASCADE)    
    language = models.CharField(choices=LANGUAGE_ASSESSMENT_OPTIONS, max_length=7)
    content = models.TextField() 
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.language


class ConfigResource(models.Model):

    LANGUAGE_ASSESSMENT_OPTIONS = [
        ('eng', 'eng'),
        ('spa', 'spa'),
        ('fr', 'fr')
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    language = models.CharField(choices=LANGUAGE_ASSESSMENT_OPTIONS, max_length=7)    
    content = models.ForeignKey(to=ConfigMessage, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.name
