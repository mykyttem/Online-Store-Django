from django.db import models

# Create your models here.
class Registration(models.Model):
    login_user = models.CharField(max_length=20)
    email_user = models.CharField(max_length=20)
    password_user = models.CharField(max_length=20) #TODO: пошукати щось більше для пароля