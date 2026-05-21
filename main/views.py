from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from . import models
import random

# Create your views here.
def home(request):
    news = models.New.objects.order_by("-date")[:6]
    file = get_object_or_404(models.Download, id=1)

    if request.method == "POST":
        email = request.POST.get("email")
        models.Subscriber.objects.get_or_create(email=email)

        from django.shortcuts import redirect
        return redirect("home")

    context = {
        "title": "Головна сторінка",
        "news": news,
        "file": file,
    }
    
    return render(request, "main/home.html", context)

def newsDetail(request, id):
    new_item = get_object_or_404(models.New, id=id)
    context = {
        "title": new_item.title,
        "new_item": new_item,
    }
    return render(request, "main/newsDetail.html", context)

def docs(request):
    active_tab = request.GET.get('tab', 'terms')
    
    context = {
        'active_tab': active_tab,
        'title': 'Юридична документація'
    }
    return render(request, 'main/docs.html', context)

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
    # links = ["youtube", "telegram", "twitter", "facebook", "instagram", "reddit"]
    links = [
        ("YOUTUBE", "https://www.youtube.com/"), ("TELEGRAM", "https://t.me/"), 
        ("TWITTER", "https://twitter.com/"), ("FACEBOOK", "https://www.facebook.com/"), 
        ("INSTAGRAM", "https://www.instagram.com/"), ("REDDIT", "https://www.reddit.com/")
        ]
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

            if len(request.POST["nickname"]) > 30:
                return redirect("product", id)
            
            already_reviewed = models.Review.objects.filter(product=product, ip_address=ip).exists()
            if already_reviewed:
                from django.contrib import messages
                messages.error(request, "Ви вже залишили оцінку для цього товару.")
                return redirect("product", id=product.id)

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
            # orderItem = models.OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"])
            # models.InventoryItem.objects.create(profile=profile, product=item["product"], quantity=item["quantity"])
            models.OrderItem.objects.create(
                order=order, 
                product=item["product"], 
                quantity=item["quantity"]
            )
            
            inventory_item, created = models.InventoryItem.objects.get_or_create(
                profile=profile,
                product=item["product"],
                defaults={"quantity": item["quantity"]}
            )

            if not created:
                inventory_item.quantity += int(item["quantity"])
                inventory_item.save()
        
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

def register(request):
    context = {"title": "Реєстрація"}

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST.get('email')
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Акаунт з таким іменем уже існує!')
            return render(request, 'main/register.html', context)
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        # messages.success(request, 'Реєстрація успішна!')
        return redirect('login')

    return render(request, "main/register.html", context)

def loginUser(request):
    context = {
        "title": "Вхід",
    }
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            # messages.success(request, 'Ви увійшли в аккаунт!')
            return redirect("home")
        
        messages.error(request, 'Такого аккаунту не існує!')
        return render(request, 'main/login.html', context) 

    return render(request, "main/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


@login_required
def account(request):
    if is_admin(request.user):
        return redirect("admin")
    profiles = models.Profile.objects.filter(user=request.user).prefetch_related(
        'achievements',
        'inventoryitem_set__product',
        'order_set__orderitem_set__product'
        )
    context = {
        "title": "Особистий кабінет",
        "profiles": profiles
    }

    if request.method == "POST" and "create_profile" in request.POST:
        profile_name = request.POST.get("profile_name")
        
        if profile_name:
            models.Profile.objects.create(
                user=request.user,
                name=profile_name,
                email=request.user.email
            )
            return redirect("account")

    return render(request, "main/account.html", context)

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin(request):
    all_users = User.objects.prefetch_related(
        'profile_set',
        'profile_set__achievements',
        'profile_set__inventoryitem_set__product',
        'profile_set__order_set__orderitem_set__product'
    ).order_by('-date_joined')
    
    context = {
        "title": "Панель адміністратора",
        "all_users": all_users,
    }
    return render(request, 'main/admin.html', context)


def requestReset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)

            code = "".join([str(random.randint(0, 9)) for _ in range(6)])
            
            models.PasswordResetCode.objects.filter(user=user).delete()
            models.PasswordResetCode.objects.create(user=user, code=code)
            
            message = EmailMessage(
                subject='Код для зміни пароля',
                body=f'Ваш тимчасовий код для зміни пароля: {code}. Він дійсний 15 хвилин.',
                from_email='noreply@rmkdev.com',
                to=[email],
            )
            message.content_subtype = "plain"
            message.encoding = 'utf-8'

            message.send(fail_silently=False)
            request.session['reset_email'] = email
            messages.success(request, "Код успішно надіслано на ваш Email!")
            return redirect('confirmReset')
            
        except User.DoesNotExist:
            messages.error(request, "Користувача з таким Email не знайдено.")
            
    return render(request, 'main/requestReset.html', {"title": "Зміна пароля"})

def confirmReset(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('requestReset')

    if request.method == "POST":
        code_input = request.POST.get("code")
        password_input = range_password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            reset_code = models.PasswordResetCode.objects.get(user=user, code=code_input)

            if reset_code.is_valid():
                user.set_password(password_input)
                user.save()
                
                reset_code.is_used = True
                reset_code.save()
                del request.session['reset_email']
                
                messages.success(request, "Пароль успішно змінено!")
                return redirect('login')
            else:
                messages.error(request, "Термін дії коду вичерпано.")
        except (User.DoesNotExist, models.PasswordResetCode.DoesNotExist):
            messages.error(request, "Невірний код підтвердження.")

    return render(request, 'main/confirmReset.html', {"title": "Зміна пароля"})



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