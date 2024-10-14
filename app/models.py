from django.db import models
from django.core.validators import MinValueValidator

class Slide(models.Model):
    image = models.ImageField(upload_to='slides', null=True)

class Title(models.Model):
    title = models.CharField(max_length = 300, default='Welcome to Out Store', unique=True)
    
    def __str__(self):
        return self.title

class Size(models.Model):
    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('OUT OF STOCK', 'out of stock'),
    ]
    size = models.CharField(max_length = 15, choices = SIZE_CHOICES, unique=True)
    
    def __str__(self):
        return self.size

class Category(models.Model):
    name = models.CharField(max_length = 50, null=True, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.PROTECT, null=True)
    name = models.CharField(max_length = 200)
    price = models.FloatField(validators=[MinValueValidator(1)], default=0)
    sizes = models.ManyToManyField(Size)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return f'"{self.product.name}" image'


class Maktab(models.Model):
    name = models.CharField(max_length = 100, null=True)
    
    def __str__(self):
        return self.name


class Wilaya(models.Model):
    name = models.CharField(max_length = 100, default='Alger')
    domicile_price = models.FloatField(default = 0)
    yalidine_price = models.FloatField(default = 0)
    maktab = models.ManyToManyField(Maktab)



    def __str__(self):
        return f'{self.name}'

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    total = models.FloatField()
    size = models.CharField(max_length = 2, default='S')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default = 1)

    def __str__(self):
        return f'{self.product.name} | Order Item'

class Order(models.Model):
    full_name = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 30)
    delivery = models.CharField(max_length = 15)
    wilaya = models.CharField(max_length = 40)
    desktop =models.CharField(max_length = 200, null=True, blank=True)
    order_items = models.ManyToManyField(OrderItem)
    township = models.CharField(max_length = 200, null=True, blank=True)
    adress = models.CharField(max_length = 200, null=True, blank=True)
    total = models.FloatField(default = 0)

    def __str__(self):
        return f'{self.full_name} | Order'
