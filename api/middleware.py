from django.utils import timezone
from djoser import utils


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            last_activity = request.user.last_activity
            if last_activity is not None:
                delta = timezone.now() - last_activity
                print(f'Time delta: {delta.seconds}')
                if delta.seconds > 60:
                    utils.logout_user(request)
                    print('User LOGOUT!')

        response = self.get_response(request)

        return response