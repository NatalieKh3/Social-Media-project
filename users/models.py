from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=50)
    about=models.TextField()
    photo=models.FileField(upload_to="user_photos/")
    city=models.CharField(max_length=255)
    hobby=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Friends(models.Model):
    user1=models.ForeignKey(User,on_delete=models.CASCADE, related_name="user1")
    user2=models.ForeignKey(User,on_delete=models.CASCADE, related_name="user2")

class FriendRequest(models.Model):
    friend1=models.ForeignKey(User,on_delete=models.CASCADE, related_name="friend1")
    friend2=models.ForeignKey(User,on_delete=models.CASCADE, related_name="friend2")
    friend_accept=models.BooleanField()