from rest_framework.generics import  ListAPIView

from users.models import CustomUser
from users.serializer import UserSerializer

class UserViewSet(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
