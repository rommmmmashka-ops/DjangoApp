from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from . import models

# Create your views here.
def home(request):
    news = models.New.objects.order_by("date")
    file = get_object_or_404(models.Download, id=1)

    if request.method == "POST":

            email = request.POST.get("email")

            models.Subscriber.objects.get_or_create(
                email=email
            )


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

def wikiItem(request, id):
    item = get_object_or_404(models.Item, id=id)
    context = {
        "title": "Сторінка предмета",
        "item": item,
    }

    return render(request, "main/item.html", context)
    
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

    if request.method == "POST":

            ip = request.META.get("REMOTE_ADDR")

            models.Review.objects.create(
                product=product,
                nickname=request.POST["nickname"],
                comment=request.POST["comment"],
                rating=request.POST["rating"],
                ip_address=ip
            )

    reviews = models.Review.objects.filter(product=product)

    average = reviews.aggregate(Avg("rating"))

    context = {
        "title": "Сторінка товару",
        "product": product,
        "reviews": reviews,
        "average": average["rating__avg"],
    }
    
    return render(request, "main/product.html", context)


def cart(request):
    cart = request.session.get("cart", {})
    products = []
    total = 0

    for id, quantity in cart.items():
        product = models.Product.objects.get(id=id)
        subtotal = product.price * quantity
        total += subtotal

        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

    context = {
        "title": "Кошик",
        "products": products,
        "total": total
    }

    return render(request, "main/cart.html", context)

def addCart(request, id):
    cart = request.session.get("cart", {})
    id = str(id)

    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    request.session["cart"] = cart

    return redirect("cart")

def removeCart(request, id):
    cart = request.session.get("cart", {})
    id = str(id)

    if id in cart:
        del cart[id]

    request.session["cart"] = cart

    return redirect("cart")

def checkout(request):
    cart = request.session.get("cart", {})
    total = 0
    products = []

    for id, quantity in cart.items():
        product = models.Product.objects.get(id=id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })
    
    if total == 0:
        return redirect("cart")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        try:
            profile = models.Profile.objects.get(name=name, email=email)
        except models.Profile.DoesNotExist:
            # return HttpResponse("Профіль не знайдено")
            context = {
                "title": "Оформлення",
                "invalid": True,
                "products": products,
                "total": total,
            }
            return render(request, "main/checkout.html", context)

        order = models.Order.objects.create(profile=profile, total=total)
        for item in products:
            orderItem = models.OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"])
            models.InventoryItem.objects.create(profile=profile, product=item["product"], quantity=item["quantity"])
        
        request.session["cart"] = {}

        return render(request, "main/checkout.html", {
            "title": "Замовлення успішне",
            "total": total
        })

    context = {
        "title": "Оформлення",
        "products": products,
        "total": total,
    }
    return render(request, "main/checkout.html", context)


#GODOT
def get_profile(request, name):
    try:
        profile = models.Profile.objects.get(name=name)
        data = {
            "name": profile.name,
            "level": profile.level,
            "email": profile.email,
        }
        return JsonResponse(data)
    except models.Profile.DoesNotExist:
        return JsonResponse({"error": "Профіль не знайдено"}, status=404)