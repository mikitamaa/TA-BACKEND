from rest_framework.routers import DefaultRouter
from .viewsets.viewsets import *

router = DefaultRouter()
router.register('users', UserViewSets, basename='users')

urlpatterns = router.urls