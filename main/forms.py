from django import forms
from django.contrib import messages
from .models import User, Manga, Figurine
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=32)
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=100)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password_confirmation"]

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        # Check if password_confirmation is same as the original password
        if password != password_confirmation:
            raise forms.ValidationError("This password confirmation doesn't match with password.")
        if password:
            msgs_error = []
            # Password length > 8 character
            if len(password) < 8:
                msgs_error.append(gettext("au moins 8 caractères"))
            if len(password) > 32:
                msgs_error.append(gettext("moins de 32 caractères"))
            # Password have at least 1 number
            if not any(char.isdigit() for char in password):
                msgs_error.append(gettext("un Nombre"))
            # Password have at least 1 Uppercase
            if not any(char.isupper() for char in password):
                msgs_error.append(gettext("une Majuscule"))
            # Password have at least 1 Lowercase
            if not any(char.islower() for char in password):
                msgs_error.append(gettext("une Minuscule"))
            # Password have at least 1 character that is not alphanumeric or digital
            if not any(not char.isalpha() and not char.isdigit() for char in password):
                msgs_error.append(gettext("un caractère spéciale"))
            # Password have whitespace
            if any(char.isspace() for char in password):
                msgs_error.append(gettext("aucun espace"))
            if msgs_error:
                raise forms.ValidationError(_("Le mot de passe doit contenir: ")+", ".join(msgs_error)+".")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            # If user doesn't exist make exception
            if User.objects.get(email=email):
                raise forms.ValidationError('This email address is already in use.')
        except:
            # return email in case if user doesn't exist
            return email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email'].lower()
        password = self.cleaned_data['password']
        try:
            # If user exist in database
            # Recheck pour le mot de passe car actuellement n'importe quel mot de passe marche
            self.user = User.objects.get(email=email)
            if password == self.user.password:
                return cleaned_data
            else:
                raise
        except:
            # raise error if user doesn't exist in database
            raise forms.ValidationError('This email address or this password is incorrect, please try again.')

    def get_user(self):
        return self.user


class ShoppingAddForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        id = self.cleaned_data['product_id']
        try:
            try:
                manga = Manga.objects.get(id=id)
                if quantity <= manga.quantity:
                    return quantity
            except:
                figurine = Figurine.objects.get(id=id)
                if quantity <= figurine.quantity:
                    return quantity
        except:
            raise forms.ValidationError('Cannot Add more than in stock quantity')
