from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)
  phone =  models.CharField(max_length=200, null=True)
  profile_pic = models.ImageField(default="default_profile.jpg", null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.name


class Tag(models.Model):
  name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.name


class Product(models.Model):
  CATEGORY = (
    ('Indoor', 'Indoor'),
    ('Out door', 'Out door')
  )
  name = models.CharField(max_length=200, null=True)
  price = models.FloatField(null=True)
  category = models.CharField(max_length=200, null=True, choices=CATEGORY)
  description = models.CharField(max_length=200, null=True, blank=True)
  tags = models.ManyToManyField(Tag)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  def  __str__(self):
    return self.name


class Order(models.Model):
  STATUS = (
    ('Pending', 'Pending'),
    ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered')
  )
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) 
  product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
  status = models.CharField(max_length=200, null=True, choices=STATUS)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  note = models.CharField(max_length=1000, null=True)

  def __str__(self):
    return self.status
