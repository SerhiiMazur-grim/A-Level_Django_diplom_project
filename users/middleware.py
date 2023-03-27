from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse

from help_desk import settings


class RedirectAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/login/') \
            and not request.path.startswith('/registration/') \
                and not request.path.startswith('/api/'):
            return redirect('/login/')
        response = self.get_response(request)
        return response


class SessionLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE_LAST_ACTIVITY)
        response = self.get_response(request)
        return response


class UserActionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and response.status_code not in [302, 303]:
            UserModel = get_user_model()
            user = UserModel.objects.get(id=request.user.id)
            user.increment_actions_count()
            user.save()

        return response

