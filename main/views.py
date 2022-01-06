import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from main.utils.user import login_user, logout_user
from main.decorator.user import is_connected, is_not_connected
from main.forms import RegisterForm, LoginForm, ShoppingAddForm
from main.models import User, Manga, Figurine, ShoppingCart, ShoppingItem

# params logger
logger = logging.getLogger(__name__)


# Views for not logged


@is_not_connected()
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                # try to connect user
                login_user(request, form.get_user())
                messages.add_message(request, messages.INFO, _("Vous vous êtes connecté avec succès."))
                return redirect('index')
        except Exception as err:
            messages.add_message(request, messages.ERROR, _(f"Echec lors de l'envoi du formulaire a cause de : {err}."))
            logger.error(f'Problem in form cause of {err}')
            return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


@is_not_connected()
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                # Get user and then, create ShoppingCart linked to this user
                user = User.objects.get(email=form.cleaned_data['email'])
                ShoppingCart.objects.create(user=user)
                messages.add_message(request, messages.INFO, _("Compte d'utilisateur crée avec succès."))
                return redirect('login')
        except Exception as err:
            messages.add_message(request, messages.ERROR, _(f"Echec lors de l'envoi du formulaire a cause de : {err}."))
            logger.error(f'Problem in form cause of {err}')
            return redirect('register')
    return render(request, 'register.html', {'form': form})

# Views for logged


@is_connected()
def index(request):
    # Send objects to context
    mangas = Manga.objects.all()
    figurines = Figurine.objects.all()
    return render(request, 'home.html', {"mangas": mangas, "figurines": figurines})


@is_connected(need_login=True)
def logout(request):
    # Logout the current user
    logout_user(request)
    return redirect('index')


@is_connected()
def mangas_gallery(request):
    mangas = Manga.objects.all()
    return render(request, 'mangas-gallery.html', {"mangas": mangas})


@is_connected()
def figurines_gallery(request):
    figurines = Figurine.objects.all()
    return render(request, 'figurines-gallery.html', {"figurines": figurines})


@is_connected()
def manga_details(request, manga_name, product_id):
    manga = Manga.objects.get(title=manga_name, id=product_id)
    form = ShoppingAddForm(request.POST or None, initial={"product_id": product_id, "type": "manga"})  # category: category
    if request.method == 'POST':
        try:
            if form.is_valid():
                # Get quantity to create Shopping item and get shoppingcart to add shoppingitem
                # Try to get cart, if not connected redirect to login
                try:
                    cart = ShoppingCart.objects.get(user=request.user)
                except Exception as err:
                    messages.add_message(request, messages.ERROR, _("Vous devez être connecter pour effectuer cette action"))
                    return redirect('login')
                ShoppingItem.objects.create(shopping_cart=cart, manga=manga, quantity=form.cleaned_data['quantity'])
                messages.add_message(request, messages.INFO, _("Vous avez ajouter votre article au panier avec succès"))
                return redirect('index')
        except Exception as err:
            messages.add_message(request, messages.ERROR, _(f"Echec lors de l'envoi du formulaire a cause de : {err}."))
            return redirect('index')
    return render(request, 'mangas-details.html', {"form": form, "manga": manga})


@is_connected()
def figurine_details(request, figurine_name, product_id):
    figurine = Figurine.objects.get(name=figurine_name, id=product_id)
    form = ShoppingAddForm(request.POST or None, initial={"product_id": product_id, "type": "figurine"})  # category: category
    if request.method == 'POST':
        try:
            if form.is_valid():
                # Get quantity to create Shopping item and get shoppingcart to add shoppingitem
                # Try to get cart, if not connected redirect to login
                try:
                    cart = ShoppingCart.objects.get(user=request.user)
                except Exception as err:
                    messages.add_message(request, messages.ERROR, _("Vous devez être connecter pour effectuer cette action"))
                    return redirect('login')
                ShoppingItem.objects.create(shopping_cart=cart, figurine=figurine, quantity=form.cleaned_data['quantity'])
                messages.add_message(request, messages.INFO, _("Vous avez ajouter votre article au panier avec succès"))
                return redirect('index')
        except Exception as err:
            messages.add_message(request, messages.ERROR, _(f"Echec lors de l'envoi du formulaire a cause de : {err}."))
            return redirect('index')
    return render(request, 'figurines-details.html', {"form": form, "figurine": figurine})


@is_connected(need_login=True)
def shoppingcart(request):
    return render(request, 'shoppingcart-details.html')


@is_connected(need_login=True)
def shoppingcart_delete_product(request, product_id):
    cart = ShoppingCart.objects.get(user=request.user)
    try:
        ShoppingItem.objects.filter(shopping_cart=cart, id=product_id).delete()
        messages.add_message(request, messages.INFO, _("Le produit à bien été supprimer du panier"))
        return redirect('shoppingcart')
    except Exception as err:
        messages.add_message(request, messages.ERROR, _(f"Un problème est survenu lors de la suppression du produit car : {err}"))
        return redirect('index')
