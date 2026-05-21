from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('news/<str:id>/', views.newsDetail, name='newsDetail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path("leaderboard/<str:orderBy>/", views.leaderboard, name="leaderboard"),
    path('wiki/', views.wiki, name='wiki'),
    path('wiki/item/<str:id>/', views.wikiItem, name='wikiItem'),
    path('community/', views.community, name='community'),
    path('catalog/', views.catalog, name='catalog'),
    path("catalog/<str:category>/", views.catalogCategory, name="catalogCategory"),
    path("product/<str:id>/", views.product, name="product"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:id>/", views.addCart, name="addCart"),
    path("remove-from-cart/<int:id>/", views.removeCart, name="removeCart"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.register, name="register"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("account/", views.account, name="account"),
    path("admin/",  views.admin, name="admin"),
    path("request-reset/", views.requestReset, name="requestReset"),
    path("confirm-reset/", views.confirmReset, name="confirmReset"),
    path('docs/', views.docs, name='docs'),

    path("api/profile/<str:name>/", views.get_profile, name="get_profile"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)