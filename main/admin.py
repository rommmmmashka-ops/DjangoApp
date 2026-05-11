from django.contrib import admin
from .models import Profile, Item, Achievement, New, Product, Download, Review, Subscriber, Order, OrderItem

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

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "nickname", "comment", "rating", "created_at")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "total")

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "created_at")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name","level", "created_at", "updated_at")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "item_type", "created_at", "updated_at")

class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title","created_at", "updated_at")

admin.site.register(New, NewsAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Achievement, AchievementAdmin)