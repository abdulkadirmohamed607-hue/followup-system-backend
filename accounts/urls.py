from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CurrentUserView,
    LoginView,
    UserViewSet,
)


router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [

    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name='change_password',
    ),

    path(
        'me/',
        CurrentUserView.as_view(),
        name='current_user',
    ),

    path(
        '',
        include(router.urls),
    ),
]