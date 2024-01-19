
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default = 'default.jpg',upload_to = 'Product')
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    # address = models.CharField(max_length=50, default="", blank=True)
    # phone = models.CharField(max_length=20, default="", blank=True)
    # status = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)

    def __str__(self) :
        return f'{self.product} order by  {self.customer.username}'
    
    def order_price(self):
        return self.order_quantity * self.product.price

    def save(self, *args, **kwargs):
        self.total_price = self.order_quantity * self.product.price
        super(Order, self).save(*args, **kwargs)

class CustomerOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    status = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)

    def __str__(self) :
        return f'{self.product} order by  {self.customer.username}'
    
    def order_price(self):
        return self.order_quantity * self.product.price

    # def save(self, *args, **kwargs):
    #     self.total_price = self.order_quantity * self.product.price
    #     super(Order, self).save(*args, **kwargs)


class Custom(models.Model):
    Shoulder = models.PositiveIntegerField()
    Body_Length = models.PositiveIntegerField()
    Chest = models.PositiveIntegerField()
    Waist = models.PositiveIntegerField()
    Bottom_width = models.PositiveIntegerField()
    Sleeve_length = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    

    class Meta:
        verbose_name_plural = 'customs'
