from django.db import models
from django.contrib.auth.models import User


GENDER = (
    ("Male", "M"),
    ("Female", "F"),
    ("Other", "O")
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    profile_pix = models.ImageField(blank=True, null=True,upload_to="user_photo", default="https://cdn-icons-png.flaticon.com/512/6596/6596121.png")
    gender = models.CharField(max_length=50,choices=GENDER)
    
    def __str__(self):
        return self.fullname