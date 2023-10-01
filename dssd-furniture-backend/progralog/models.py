from django.db import models


class Progralog(models.Model):
    EVENT_OPTIONS = [
        ('ERROR', 'ERROR'),
        ('WARNING', 'WARNING'),
        ('OTHER', 'OTHER'),        
    ]
    event_type = models.CharField(choices=EVENT_OPTIONS, max_length=15)
    frame_info = models.CharField(max_length=250)
    tb_detail = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return self.event_type
