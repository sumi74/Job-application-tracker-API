from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, ProfileView, RegisterView

router = DefaultRouter()
router.register("applications", ApplicationViewSet, basename="application")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("profile/", ProfileView.as_view()),
] + router.urls 