from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TrackerAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="Tracker!2026pass")
        self.user2 = User.objects.create_user("user2", password="Tracker!2026pass")

    def add(self, **extra):
        data = {"company": "Test Co", "role": "Junior Backend Developer"}
        data.update(extra)
        return self.client.post("/api/applications/", data, format="json")

    def test_register(self):
        response = self.client.post(
            "/api/register/",
            {"username": "newuser", "email": "n@example.com", "password": "Tracker!2026pass"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

    def test_weak_password_rejected(self):
        response = self.client.post(
            "/api/register/", {"username": "weak", "password": "123"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_login_required(self):
        response = self.client.get("/api/applications/")
        self.assertIn(response.status_code, (401, 403))

    def test_create_application(self):
        self.client.force_authenticate(self.user1)
        response = self.add()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "applied")

    def test_users_see_only_their_own(self):
        self.client.force_authenticate(self.user1)
        self.add()
        self.client.force_authenticate(self.user2)
        self.assertEqual(len(self.client.get("/api/applications/").data), 0)

    def test_cannot_edit_someone_elses_application(self):
        self.client.force_authenticate(self.user1)
        app_id = self.add().data["id"]
        self.client.force_authenticate(self.user2)
        response = self.client.patch(
            f"/api/applications/{app_id}/", {"status": "offer"}, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_filter_by_status(self):
        self.client.force_authenticate(self.user1)
        self.add()
        self.add(status="interview")
        response = self.client.get("/api/applications/?status=interview")
        self.assertEqual(len(response.data), 1)

    def test_summary_counts(self):
        self.client.force_authenticate(self.user1)
        self.add()
        self.add()
        self.add(status="interview")
        data = self.client.get("/api/applications/summary/").data
        self.assertEqual(data["applied"], 2)
        self.assertEqual(data["interview"], 1)
        self.assertEqual(data["total"], 3)