from django.contrib import admin
from .models import Profile, Item, Achievement, New, Product, Download

# Register your models here.
#admin.site.register(Profile)
#admin.site.register(Item)
#admin.site.register(Achievement)

class NewsAdmin(admin.ModelAdmin):
    list_display = ("title","date", "created_at", "updated_at")

class DownloadAdmin(admin.ModelAdmin):
    list_display = ("title", "file")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "image", "price","category", "created_at", "updated_at")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name","level", "created_at", "updated_at")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "item_type", "created_at", "updated_at")

class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title","created_at", "updated_at")

admin.site.register(New, NewsAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Achievement, AchievementAdmin)