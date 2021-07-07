from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

Status = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('OnTheWay','OnTheWay'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)
States = (
    ("Alabama", "Alabama"),
    ("Alaska", "Alaska"),
    ("American", "American"),
    ("Samoa", "Samoa"),
    ("Arizona", "Arizona"),
    ("Arkansas", "Arkansas"),
    ("California", "California"),
    ("Colorado", "Colorado"),
    ("Washington", "Washington"),
    ("New York", "New York"),
    ("New Mexico", "New Mexico"),
    ("Florida", "Florida"),
)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100, default='none')
    cutPrice = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='static/app/images/product')

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300, choices = States)
    zip = models.IntegerField()

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quan = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quan * self.product.price

class OrderPlaced(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quan = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=Status, default='Pending')

    @property
    def total_cost(self):
        return self.quan * self.product.price