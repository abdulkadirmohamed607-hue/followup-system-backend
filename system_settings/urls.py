from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import SessionSettingViewSet


router = DefaultRouter()

router.register(
    'session-settings',
    SessionSettingViewSet,
    basename='session-settings'
)


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
]