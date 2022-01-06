import logging
from django.utils import timezone
from django.templatetags.static import static
from main.utils.models import generate_code_for_object

# params logger
logger = logging.getLogger(__name__)


def login_user(request, user, regenerate_token=True):
    from main.models import User
    if not user.token or regenerate_token:
        user.token = generate_code_for_object(User, 128, "token")
        user.connected = timezone.now()
        user.save()
    else:
        logger.info(f"Login the user {user} on Interface to the main app without regenerate token")
    request.session["token_main"] = user.token
    logger.info(f"Login the user {user} on Interface to the main app")
    request.user = user


def logout_user(request):
    user_str = ""
    if hasattr(request, "user"):
        user_str = str(request.user)
        request.user.token = ""
        request.user.save()
        del request.user
        if "token_main" in request.session:
            del request.session["token_main"]
        logger.info(f"Logout the user {user_str} on Interface from the main app")
