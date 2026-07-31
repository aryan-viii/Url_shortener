from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import Shortener


class ShortenerAPITests(APITestCase):

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------

    def test_create_short_url(self):
        """A short code should be generated automatically."""

        data = {
            "url": "https://example.com"
        }

        response = self.client.post(
            "/api/shorten/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Shortener.objects.count(),
            1
        )

        obj = Shortener.objects.first()

        self.assertTrue(obj.short_code)
        self.assertEqual(obj.url, "https://example.com")


    def test_create_custom_short_code(self):
        """User should be able to provide a custom short code."""

        data = {
            "url": "https://example.com",
            "short_code": "example"
        }

        response = self.client.post(
            "/api/shorten/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        obj = Shortener.objects.first()

        self.assertEqual(
            obj.short_code,
            "example"
        )


    def test_duplicate_short_code(self):
        """Duplicate short codes should not be allowed."""

        Shortener.objects.create(
            url="https://google.com",
            short_code="google"
        )

        data = {
            "url": "https://example.com",
            "short_code": "google"
        }

        response = self.client.post(
            "/api/shorten/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Shortener.objects.count(),
            1
        )


    def test_invalid_url(self):
        """Invalid URLs should be rejected."""

        data = {
            "url": "this-is-not-a-url"
        }

        response = self.client.post(
            "/api/shorten/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    # --------------------------------------------------
    # RETRIEVE
    # --------------------------------------------------

    def test_retrieve_short_url(self):
        """API should retrieve an existing short URL."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        response = self.client.get(
            f"/api/shorten/{obj.short_code}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["short_code"],
            "example"
        )

        self.assertEqual(
            response.data["url"],
            "https://example.com"
        )


    def test_retrieve_nonexistent_short_url(self):
        """Unknown short codes should return 404."""

        response = self.client.get(
            "/api/shorten/doesnotexist/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def test_update_url(self):
        """Original URL should be updateable."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        data = {
            "url": "https://google.com",
            "short_code": "example"
        }

        response = self.client.put(
            f"/api/shorten/{obj.short_code}/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.url,
            "https://google.com"
        )


    def test_short_code_cannot_be_changed(self):
        """Existing short codes should not be changeable."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        data = {
            "url": "https://example.com",
            "short_code": "changed"
        }

        response = self.client.put(
            f"/api/shorten/{obj.short_code}/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.short_code,
            "example"
        )


    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    def test_delete_short_url(self):
        """A short URL should be deletable."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        response = self.client.delete(
            f"/api/shorten/{obj.short_code}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Shortener.objects.count(),
            0
        )


    # --------------------------------------------------
    # REDIRECT
    # --------------------------------------------------

    def test_redirect_short_url(self):
        """Public short URL should redirect to original URL."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        response = self.client.get(
            f"/{obj.short_code}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )

        self.assertEqual(
            response.url,
            "https://example.com"
        )


    def test_redirect_increases_access_count(self):
        """Redirecting should increment access_count."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        self.assertEqual(
            obj.access_count,
            0
        )

        self.client.get(
            f"/{obj.short_code}/"
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.access_count,
            1
        )


    def test_api_retrieve_does_not_increase_access_count(self):
        """Inspecting a URL through the API should not count as a click."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        self.client.get(
            f"/api/shorten/{obj.short_code}/"
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.access_count,
            0
        )


    # --------------------------------------------------
    # EXPIRATION
    # --------------------------------------------------

    def test_expired_url_does_not_redirect(self):
        """Expired short URLs should return HTTP 410."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="expired",
            expires_at=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(
            f"/{obj.short_code}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_410_GONE
        )


    def test_expired_url_does_not_increase_access_count(self):
        """Attempting to visit an expired link should not count as a click."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="expired",
            expires_at=timezone.now() - timedelta(days=1)
        )

        self.client.get(
            f"/{obj.short_code}/"
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.access_count,
            0
        )


    def test_non_expired_url_redirects(self):
        """Links with future expiration dates should still work."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="active",
            expires_at=timezone.now() + timedelta(days=1)
        )

        response = self.client.get(
            f"/{obj.short_code}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )


    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    def test_url_statistics(self):
        """Stats endpoint should return access count."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example",
            access_count=5
        )

        response = self.client.get(
            f"/api/shorten/{obj.short_code}/stats/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["access_count"],
            5
        )


    def test_stats_does_not_increase_access_count(self):
        """Viewing statistics should not count as a click."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example",
            access_count=5
        )

        self.client.get(
            f"/api/shorten/{obj.short_code}/stats/"
        )

        obj.refresh_from_db()

        self.assertEqual(
            obj.access_count,
            5
        )


    # --------------------------------------------------
    # LIST
    # --------------------------------------------------

    def test_list_short_urls(self):
        """List endpoint should return shortened URLs."""

        Shortener.objects.create(
            url="https://google.com",
            short_code="google"
        )

        Shortener.objects.create(
            url="https://youtube.com",
            short_code="youtube"
        )

        response = self.client.get(
            "/api/shorten/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )


    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def test_search_by_short_code(self):
        """URLs should be searchable by short code."""

        Shortener.objects.create(
            url="https://google.com",
            short_code="google"
        )

        Shortener.objects.create(
            url="https://youtube.com",
            short_code="youtube"
        )

        response = self.client.get(
            "/api/shorten/?search=youtube"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["short_code"],
            "youtube"
        )


    def test_search_by_url(self):
        """URLs should be searchable using the original URL."""

        Shortener.objects.create(
            url="https://google.com",
            short_code="abc123"
        )

        Shortener.objects.create(
            url="https://youtube.com",
            short_code="xyz123"
        )

        response = self.client.get(
            "/api/shorten/?search=google"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )


    # --------------------------------------------------
    # QR CODE
    # --------------------------------------------------

    def test_qr_code_endpoint(self):
        """QR endpoint should return a PNG image."""

        obj = Shortener.objects.create(
            url="https://example.com",
            short_code="example"
        )

        response = self.client.get(
            f"/api/shorten/{obj.short_code}/qr/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response["Content-Type"],
            "image/png"
        )