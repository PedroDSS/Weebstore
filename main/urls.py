from django.urls import path

from . import views

# Here is my main view for my project
urlpatterns = [
    # Index
    path('', views.index, name="index"),


    # -- Not Connected (Register or Login for example) -- #

    # Login / Disconnect
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    # Register
    path('register/', views.register, name="register"),

    # User
    path('shoppingcart/', views.shoppingcart, name="shoppingcart"),
    path('shoppingcart-delete/<int:product_id>/', views.shoppingcart_delete_product, name="shoppingcart-delete"),

    # Products in Generals


    # Mangas
    path('mangas-gallery/', views.mangas_gallery, name="mangas-gallery"),
    path('manga-details/<str:manga_name>/<int:product_id>/', views.manga_details, name="manga-details"),

]
