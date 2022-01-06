from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from main.models import ShoppingCart


def is_connected(need_login=False):
    """
        Check if the user is connected to access to this page, if not, show an error page.
    """
    def _is_connected(function):
        def wrap(request, *args, **kwargs):
            from main.models import User, ShoppingCart
            if need_login:
                try:
                    if request.session and "token_main" in request.session:
                        request.user = User.objects.get(token=request.session["token_main"])
                        request.user.shoppingcart = ShoppingCart.objects.get(user=request.user)
                    else:
                        raise
                except Exception as err:
                    # Error
                    # getLogger("Main").error(f"Invalid token_main / User: {err}")
                    return redirect("login")
            else:
                try:
                    if request.session and "token_main" in request.session:
                        request.user = User.objects.get(token=request.session["token_main"])
                        request.user.shoppingcart = ShoppingCart.objects.get(user=request.user)
                    else:
                        raise
                except:
                    request.user = None
            return function(request, *args, **kwargs)
        return wrap
    return _is_connected


def is_not_connected():
    """
        Check if the user is not connected to access to this page, if not, show an error page.
    """
    def _is_not_connected(function):
        def wrap(request, *args, **kwargs):
            from main.models import User
            try:
                if request.session and "token_main" in request.session:
                    raise
            except:
                return redirect('index')
            return function(request, *args, **kwargs)
        return wrap
    return _is_not_connected
