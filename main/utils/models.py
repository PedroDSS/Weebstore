from django.db import models
from main.utils.string import random_key
from os.path import join, exists
from os import makedirs
from weebstoreinterface.settings import MEDIA_ROOT


class ModelProductUtils(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product", default=0)
    quantity = models.IntegerField(help_text="Quantity of the product", default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="The rate of the product, can see if the product is liked or not", default=0)
    description = models.TextField(blank=True, null=True, help_text="Description, describes the details of the product")
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)


def rename_file(instance, filename):
    from main.models import Manga, Figurine  # , Cosplays, Supply, Other

    # Filename
    ext = filename.split(".")[-1].lower()
    random_str = random_key(16)
    filename = f"{random_str}.{ext}"
    folder = None

    # Get folder according instance
    if isinstance(instance, Manga):
        folder = "mangas/picture"
    if isinstance(instance, Figurine):
        folder = "figurines/picture"
    # elif isinstance(instance, Cosplays):
    #     folder = "cosplays/picture"
    # if isinstance(instance, Supply):
    #     folder = "supply/picture"
    else:
        folder = "other"

    absolute_folder = join(MEDIA_ROOT, folder)
    if not exists(absolute_folder):
        makedirs(absolute_folder)

    # Join folder+filename
    return join(folder, filename)


def generate_code_for_object(model, size=20, key="code", chars_or_methods=None):
    """
    Generate a unique code.
    """
    from main.utils.string import random_key
    code = ""
    fields = {}
    while len(code) == 0:
        if chars_or_methods and not isinstance(chars_or_methods, str):
            # Token generation by a given method
            code = chars_or_methods(size)
        else:
            # Token generation by a string
            code = random_key(size, chars=chars_or_methods)
        fields[key] = code
        # Check if code is unique
        try:
            model.objects.get(**fields)
            # No error, code already exist, code reset
            code = ""
        except Exception:
            # No model with this code
            return code
