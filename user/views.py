from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

from .serializers import UserTokenSerializer, AdminTokenSerializer, CountrySerializer, CitySerializer, \
    UserCreateSerializer, UserListSerializer, AdminCreateSerializer, UserSerializer, GenderSerializer
from .models import Country, City, Gender


class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer
    permission_classes = [AllowAny, ]


class AdminTokenView(TokenObtainPairView):
    serializer_class = AdminTokenSerializer
    permission_classes = [AllowAny, ]


class CountryViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class GenderViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class CityViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer


class UserViewSet(ModelViewSet):
    permission_classes = [AllowAny | IsAuthenticated]

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'list':
                return User.objects.all()
            elif self.action == 'retrieve' or self.action == 'update' or self.action == 'destroy':
                return User.objects.filter(pk=self.request.user.pk)
        except:
            raise PermissionDenied

    def get_serializer_class(self):
        try:
            if self.action == 'create':
                return UserCreateSerializer
            elif self.action == 'retrieve' or self.action == 'list':
                return UserListSerializer
            elif self.action == 'update' or self.action == 'destroy':
                return UserSerializer
        except:
            raise PermissionDenied


class AdminViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminCreateSerializer