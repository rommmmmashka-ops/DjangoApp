from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path("leaderboard/<str:orderBy>/", views.leaderboard, name="leaderboard"),
    path('wiki/', views.wiki, name='wiki'),
    path('community/', views.community, name='community'),
    path('catalog/', views.catalog, name='catalog'),
    path("catalog/<str:category>/", views.catalogCategory, name="catalogCategory"),
]