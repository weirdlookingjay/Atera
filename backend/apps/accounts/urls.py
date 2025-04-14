from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')

urlpatterns = [
    # URLs will be added here
    path('', include(router.urls)),
]
