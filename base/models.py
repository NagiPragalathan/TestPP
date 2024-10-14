from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('content_manager', 'Content Manager'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
