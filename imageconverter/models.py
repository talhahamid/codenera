from django.db import models
from accounts.models import Users


# Create your models here.


class ImagesStore(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')