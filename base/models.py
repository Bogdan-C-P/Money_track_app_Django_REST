from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    ammount = models.DecimalField(max_digits=8,decimal_places=2)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['create']