from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Produkty(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produktnazev=models.CharField(max_length=130)
    image=models.ImageField(null=True, blank=True)
    znacka=models.CharField(max_length=130,null=True, blank=True)
    kategorie=models.CharField(max_length=130,null=True, blank=True)
    info=models.TextField(null=True, blank=True)
    hodnoceni=models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    cena=models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    kusy=models.IntegerField(null=True, blank=True, default=0)
    vytvoreno=models.DateTimeField(auto_now_add=True)
    _id= models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.produktnazev

class Products(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produktnazev=models.CharField(max_length=130)
    image=models.ImageField(null=True, blank=True)
    znacka=models.CharField(max_length=130,null=True, blank=True)
    kategorie=models.CharField(max_length=130,null=True, blank=True)
    info=models.TextField(null=True, blank=True)
    hodnoceni=models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    recenze=models.IntegerField(null=True,blank=True,default=0)
    cena=models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    kusy=models.IntegerField(null=True, blank=True, default=0)
    vytvoreno=models.DateTimeField(auto_now_add=True)
    _id= models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.produktnazev

