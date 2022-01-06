from django.contrib import admin
from django import forms
from .models import User, Manga, Theme, ShoppingCart, ShoppingItem


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_filter = []
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)


class MangaAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'author', 'category', '_themes', 'price', 'quantity', 'rate', 'modified', 'created']
    list_filter = ['author', 'category', 'themes']
    search_fields = ['title', 'author', 'category', 'themes']

    class Meta:
        model = Manga

    def _themes(self, obj):
        return "\n".join([t.name for t in obj.themes.all()])

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None, *args, **kwargs):
        # According the page, we add specific .js file to context
        if add or change:
            context["media"] += forms.Media(css={"all": ("css/admin/selectize.min.css",)}, js=("js/admin/jquery.min.js",
                                                                                               "js/admin/selectize.min.js", "js/admin/select.js"))
        return super(MangaAdmin, self).render_change_form(request=request, context=context, add=add, change=change, form_url=form_url, obj=obj)


admin.site.register(Manga, MangaAdmin)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = []
    search_fields = ['name']

    class Meta:
        model = Theme


admin.site.register(Theme, ThemeAdmin)


class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ['shopping_cart', '_item', 'quantity']
    list_filter = []
    search_fields = ['shopping_cart']

    def _item(self, obj):
        if obj.manga:
            return str(obj.manga)


admin.site.register(ShoppingItem, ShoppingItemAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    list_display = ['_name', '_user', 'price']
    list_filter = []
    search_fields = ['_user']

    def _name(self, obj):
        return str(obj)

    def _user(self, obj):
        return obj.user.username


admin.site.register(ShoppingCart, ShoppingCartAdmin)

# Register your models here.
