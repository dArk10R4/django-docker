from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class InstagramCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instagram_username = models.CharField(max_length=50,unique=True)
    instagram_password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.instagram_username} - {self.user.username}'
class InstagramDatas(models.Model):
    instagram = models.OneToOneField(InstagramCredentials, on_delete=models.CASCADE)
    instagram_followers = models.IntegerField(null=True,blank=True)
    instagram_following = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.instagram_followers} - {self.instagram_following} - {self.instagram.instagram_username}'