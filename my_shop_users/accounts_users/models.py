from django.db import models


class Registration(models.Model):
    login_user = models.CharField(max_length=20)
    email_user = models.EmailField(max_length=20)
    password_user = models.CharField(max_length=20) 
    avatar_user = models.ImageField(null=True, blank=True, upload_to="avatars/", default='avatars/default_avatar.png')