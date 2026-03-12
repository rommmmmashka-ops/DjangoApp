from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=40)
    level = models.IntegerField(default=1)
    achievements = models.ManyToManyField("Achievement")
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
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name