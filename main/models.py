from django.db import models
from django.utils.translation import gettext_lazy as _
from main.utils.models import ModelProductUtils, rename_file

# The file that contains all of my models

# Mangas Category
MANGAS_SHONEN = 'shonen'
MANGAS_SHOJO = 'shojo'
MANGAS_SEINEN = 'seinen'
MANGAS_JOSEI = 'josei'
MANGAS_YAOI = 'yaoi'
MANGAS_YURI = 'yuri'


class User(models.Model):
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=30)
    # address = models.TextField(blank=True, null=True, help_text="The adress of the user (used for the delivery)")
    # favorite_product
    # wishlist wishlist model
    # money
    # commented_products
    # Important for login/logout
    token = models.CharField(max_length=128, blank=True, null=True, help_text="Auto-set on login via the interface and cleaned on logout")
    connected = models.DateTimeField(blank=True, null=True, help_text="The last connection date, used to check timeout of token")

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Theme(models.Model):
    name = models.CharField(max_length=16, help_text="Name of the theme")

    def __str__(self):
        return f"{self.name}"


class Manga(ModelProductUtils):
    title = models.CharField(max_length=64, help_text="Title of the manga")
    volume = models.IntegerField(help_text="The volume number")
    author = models.CharField(max_length=32, help_text="Author of the manga")
    CHOICES = [
        (MANGAS_SHONEN, _("Shonen")),
        (MANGAS_SHOJO, _("Shojo")),
        (MANGAS_SEINEN, _("Seinen")),
        (MANGAS_JOSEI, _("Josei")),
        (MANGAS_YAOI, _("Yaoi")),
        (MANGAS_YURI, _("Yuri"))
    ]
    release = models.IntegerField(help_text="This is the release year for reference")
    category = models.CharField(max_length=16, choices=CHOICES, default=MANGAS_SHONEN, help_text="This define the mangas category")
    themes = models.ManyToManyField(Theme, blank=True, help_text="Differents themes of the mangas")
    picture = models.FileField(upload_to=rename_file, null=True, blank=True, default=None, help_text="Either set a file here")

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return ""

    def get_all_themes(self):
        themes = []
        for theme in self.themes.all():
            themes.append(theme)
        return themes

    @property
    def quantity_range(self):
        return range(self.quantity)

    def __str__(self):
        return f"{self.title} Volume n°{self.volume}"


class Figurine(models.Model):
    name = models.CharField(max_length=64, help_text="Name of the Figurine")
    collection = models.CharField(max_length=32, help_text="Name of the figurine collection")
    picture = models.FileField(upload_to=rename_file, null=True, blank=True, default=None, help_text="Either set a file here")

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return ""

    @property
    def quantity_range(self):
        return range(self.quantity)

    def __str__(self):
        return f"{self.name} ({self.collection})"

# class Commentary(models.Model):
#     author=
#     description=
#     rate=
#     date=


class ShoppingItem(models.Model):
    shopping_cart = models.ForeignKey("ShoppingCart", on_delete=models.CASCADE, help_text="ShoppingCart")
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, help_text="Manga we wanted to buy")
    # figurine
    # Supply etc....
    quantity = models.IntegerField(default=1)

    def get_price(self):
        if self.manga:
            return self.manga.price * self.quantity
        return 0

    def get_product_picture(self):
        if self.manga:
            return self.manga.get_picture_url()
        return ""

    def __str__(self):
        if self.manga:
            return str(self.manga)


class ShoppingCart(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, help_text="User linked to this ShoppingCart")
    price = models.IntegerField(null=True, help_text="Total price in the user shopping cart")

    def get_all_products(self):
        products = []
        for shoppingitem in self.shoppingitem_set.all():
            products.append(shoppingitem)
        return products

    def get_total_price(self):
        products = self.get_all_products()
        total_price = 0
        for product in products:
            total_price += product.get_price()
        return f"{float(total_price)} €"

    def get_all_products_quantity(self):
        products = self.get_all_products()
        total = 0
        for product in products:
            total += product.quantity
        return total

    def __str__(self):
        return f"{self.user}'s Cart"

    # class Delivery qui serais les commandes éffectuées par l'utilisateur

    # class Author peut être pour ajouter une page d'autheur avec description et liste de mangas écrit par ce même auteur (dispo sur le site uniquement)
