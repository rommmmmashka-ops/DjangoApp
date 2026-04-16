from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.
def home(request):
    news = models.New.objects.order_by("date")
    file = get_object_or_404(models.Download, id=1)
    context = {
        "title": "Головна сторінка",
        "news": news,
        "file": file,
    }
    
    
    return render(request, "main/home.html", context)


def leaderboard(request, orderBy=0):
    #profiles = models.Profile.objects.order_by("kills").reverse()
    if orderBy:
        profiles = models.Profile.objects.order_by(orderBy).reverse()
    else:
        profiles = models.Profile.objects.order_by("kills").reverse()
    context = {
        "title": "Лідерборд",
        "players": profiles,
    }

    return render(request, "main/leaderBoard.html", context)


def wiki(request):
    items = models.Item.objects.order_by("name")
    types = [choice[0] for choice in models.Item.TYPE_CHOICES]
    
    context = {
        "title": "Вікі",
        "items": items,
        "types": types,
    }

    return render(request, "main/wiki.html", context)
    
def community(request):
    links = ["youtube", "telegram", "twitter", "facebook", "instagram", "reddit"]
    links = [x.upper() for x in links]
    context = {
        "title": " Спільнота",
        "links": links,
    }

    return render(request, "main/community.html", context)
    
def catalog(request):
    products = models.Product.objects.all()
    categories = [choice[0] for choice in models.Product.TYPE_CHOICES]
    context = {
        "title": "Магазин",
        "products": products,
        "categories": categories,
    }

    return render(request, "main/catalog.html", context)

def catalogCategory(request, category):
    products = models.Product.objects.filter(category=category)
    context = {
        "title": "Магазин",
        "products": products,
    }

    return render(request, "main/catalog.html", context)

def product(request, id):
    product = get_object_or_404(models.Product, id=id)
    context = {
        "title": "Сторінка товару",
        "product": product,
    }
    
    return render(request, "main/product.html", context)