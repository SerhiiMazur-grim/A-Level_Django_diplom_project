from django.utils import timezone
from djoser import utils
from django.http import JsonResponse

from help_desk.settings import TOKEN_AGE_LAST_ACTIVITY
from users.models import CustomUser


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser and 'Authorization' in request.headers:
            delta = timezone.now() - request.user.last_activity
            if delta.seconds > TOKEN_AGE_LAST_ACTIVITY:
                utils.logout_user(request)
                response = JsonResponse({'detail': 'Недійсний токен.'}, status=401)
            user = CustomUser.objects.get(pk=request.user.pk)
            user.cls_last_activity()

        return response