from .matching import analyze_match
from django.db.models import Count
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Application, Profile
from .serializers import ApplicationSerializer, ProfileSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        qs = Application.objects.filter(owner=self.request.user)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-date_applied")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        counts = (
            Application.objects.filter(owner=request.user)
            .values("status")
            .annotate(total=Count("id"))
        )
        result = {choice[0]: 0 for choice in Application.STATUS_CHOICES}
        for row in counts:
            result[row["status"]] = row["total"]
        result["total"] = sum(result.values())
        return Response(result)

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        application = self.get_object()
        if not application.job_description.strip():
            return Response(
                {"detail": "Add a job description to this application first."}, status=400
            )
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if not profile.skills.strip():
            return Response(
                {"detail": "Add your skills at /api/profile/ first."}, status=400
            )
        return Response(analyze_match(application.job_description, profile.skills))

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile