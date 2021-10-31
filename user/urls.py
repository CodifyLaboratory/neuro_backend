from django.urls import path

from .views import UserTokenView, AdminTokenView, CountryViewSet, CityViewSet, UserViewSet, AdminViewSet, GenderViewSet

urlpatterns = [
    path('auth/users/token/', UserTokenView.as_view()),
    path('auth/users/token/refresh/', UserTokenView.as_view()),

    path('auth/admins/token/', AdminTokenView.as_view()),
    path('auth/admins/token/refresh/', AdminTokenView.as_view()),

    path('countries/', CountryViewSet.as_view({'get': 'list'})),
    path('cities/', CityViewSet.as_view({'get': 'list'})),
    path('genders/', GenderViewSet.as_view({'get': 'list'})),

    path('auth/users/create/', UserViewSet.as_view({'post': 'create'})),
    path('auth/users/', UserViewSet.as_view({'get': 'list'})),
    path('auth/users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('auth/users/update/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('auth/users/delete/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    path('auth/admins/create/', AdminViewSet.as_view({'post': 'create'})),
]