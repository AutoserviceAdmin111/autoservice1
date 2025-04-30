from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sub = models.CharField(max_length=36, unique=True, primary_key=True)  
    roles = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True) 
    patronymic = models.CharField(max_length=150, blank=True)  
    email_verified = models.BooleanField(default=False)
    sid = models.CharField(max_length=100, blank=True, null=True)
    created_ts = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('approved', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    problem = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class PriceImage(models.Model):
    image = models.ImageField(upload_to='prices/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Прайс от {self.created_at.strftime('%d.%m.%Y')}"