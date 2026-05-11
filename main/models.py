from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=40, unique=True)
    level = models.IntegerField(default=1)
    achievements = models.ManyToManyField("Achievement")
    email = models.EmailField(null=True, unique=False)
    
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    current_killstreak = models.IntegerField(default=0)
    max_killstreak = models.IntegerField(default=0)
    vehicles_destroyed = models.IntegerField(default=0)
    #time_alive = models.IntegerField(default=0)
    #max_time_alive = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class New(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    date = models.DateField(auto_now_add=True)
    href = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Download(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="downloads/")

class Product(models.Model):
    TYPE_CHOICES = [
        ("cosmetics", "Декор"),
        ("weapon", "Зброя"),
        ("decals", "Декалі"),
    ]

    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to="products/", default="products/no_foto.jpg")
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TYPE_CHOICES, default="")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order #{self.order.id}"

class InventoryItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    comment = models.TextField(default="")
    rating = models.IntegerField()

    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.nickname

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Achievement(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Item(models.Model):
    TYPE_CHOICES = [
        ("Tool", "Tool"),
        ("Weapon", "Weapon"),
        ("Gun", "Gun"),
        ("Armor", "Armor"),
        ("Other", "Other"),
    ]
    
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="items/", default="items/no_foto.jpg")
    description = models.TextField()
    item_type = models.CharField(max_length=40, choices=TYPE_CHOICES, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name