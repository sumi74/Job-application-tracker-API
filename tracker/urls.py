from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, RegisterView

router = DefaultRouter()
router.register("applications", ApplicationViewSet, basename="application")

urlpatterns = [
    path("register/", RegisterView.as_view()),
] + router.urls 