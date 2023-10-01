from django.db import models
from authentication.models import User

class Role(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    denomination = models.CharField(max_length=40, unique=True, db_index=True)
    description = models.CharField(max_length=70)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.denomination

class HeadRole(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    observations = models.CharField(max_length=70)
    head = models.ForeignKey(to=Role, related_name="head", on_delete=models.CASCADE)
    child = models.ForeignKey(to=Role, related_name="child", on_delete=models.CASCADE) 
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']
        unique_together = ('head', 'child')

    def __str__(self):
        return str(f'{self.head}, {self.child}')

class EventSuspensionRole(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    observations = models.CharField(max_length=255)
    role_id = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']
        unique_together = ('role_id', 'start_at', 'end_at')

    def __str__(self):
        return str(f'{self.role_id}, {self.start_at}, {self.end_at}' )

class UserRole(models.Model):
    creator = models.ForeignKey(to=User, related_name="creator", on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, related_name="consumer", on_delete=models.CASCADE)
    role_id = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']        

    def __str__(self):
        return str(f'{self.user_id}, {self.role_id}')


class ViewDescriptor(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    denomination = models.CharField(max_length=120, unique=True, db_index=True)
    stack_name = models.CharField(max_length=120, unique=True, db_index=True)
    description = models.CharField(max_length=120)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.denomination

class PermissionRole(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    view_id = models.ForeignKey(to=ViewDescriptor, on_delete=models.CASCADE)
    role_id = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']        

    def __str__(self):
        return str(f'{self.view_id}, {self.role_id}')