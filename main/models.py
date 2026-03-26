from django.db import models

# Create your models here.
class New(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    date = models.DateField(auto_now_add=True)
    href = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    TYPE_CHOICES = [
        ("cosmetics", "Декор"),
        ("weapon", "Зброя"),
        ("decals", "Декалі"),
    ]

    title = models.CharField(max_length=40)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TYPE_CHOICES, default="")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    name = models.CharField(max_length=40)
    level = models.IntegerField(default=1)
    achievements = models.ManyToManyField("Achievement")
    
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
        ("Food", "Food"),
        ("Clothes", "Clothes"),
        ("BuildingMaterial", "BuildingMaterial"),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=40, choices=TYPE_CHOICES, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name