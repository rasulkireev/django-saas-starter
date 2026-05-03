from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from django.http import HttpRequest

{% if cookiecutter.generate_blog == 'y' %}
from apps.blog.choices import BlogPostStatus
from apps.api.views import (
    submit_blog_post,
    list_internal_blog_posts,
    get_internal_blog_post,
    update_internal_blog_post,
    patch_internal_blog_post,
    delete_internal_blog_post,
    review_internal_blog_post,
    publish_internal_blog_post,
)


class BlogPostApiTests(SimpleTestCase):
    @staticmethod
    def _request() -> HttpRequest:
        request = HttpRequest()
        request.auth = SimpleNamespace(user=SimpleNamespace(is_superuser=True))
        return request

    @staticmethod
    def _post_data(**overrides):
        data = {
            "title": "Hello",
            "description": "Desc",
            "slug": "hello",
            "tags": "django",
            "content": "Body",
            "status": BlogPostStatus.DRAFT,
        }
        data.update(overrides)
        return SimpleNamespace(**data)

    def test_submit_blog_post_requires_superuser(self):
        request = HttpRequest()
        request.auth = SimpleNamespace(user=SimpleNamespace(is_superuser=False))

        status, payload = submit_blog_post(request, self._post_data())

        assert status == 403
        assert payload["message"] == "Forbidden: superuser access required."

    def test_submit_blog_post_creates_draft_post(self):
        request = self._request()
        data = self._post_data()

        with patch("apps.api.views.BlogPost.objects") as objects:
            response = submit_blog_post(request, data)

        assert response.status == "success"
        objects.create.assert_called_once_with(
            title="Hello",
            description="Desc",
            slug="hello",
            tags="django",
            content="Body",
            status=BlogPostStatus.DRAFT,
        )

    def test_list_internal_blog_posts_returns_serialized_items(self):
        request = self._request()
        post = SimpleNamespace(
            id=1,
            title="Hello",
            description="Desc",
            slug="hello",
            tags="django",
            content="Body",
            status=BlogPostStatus.DRAFT,
            created_at=None,
        )

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.order_by.return_value = [post]
            response = list_internal_blog_posts(request)

        assert len(response["blog_posts"]) == 1
        assert response["blog_posts"][0]["slug"] == "hello"

    def test_get_internal_blog_post_returns_404_when_missing(self):
        request = self._request()

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.get.side_effect = Exception("not found")
            # normalize to model-specific behavior
            from apps.blog.models import BlogPost

            objects.get.side_effect = BlogPost.DoesNotExist
            status, payload = get_internal_blog_post(request, blog_post_id=999)

        assert status == 404
        assert payload["message"] == "Blog post not found."

    def test_publish_internal_blog_post_sets_status_to_published(self):
        request = self._request()
        post = Mock()

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.get.return_value = post
            response = publish_internal_blog_post(request, blog_post_id=12)

        assert response["status"] == "success"
        assert post.status == BlogPostStatus.PUBLISHED
        post.save.assert_called_once_with(update_fields=["status", "updated_at"])

    def test_update_internal_blog_post_replaces_all_editable_fields(self):
        request = self._request()
        post = Mock()
        data = self._post_data(title="Updated", status=BlogPostStatus.PUBLISHED)

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.get.return_value = post
            response = update_internal_blog_post(request, blog_post_id=12, data=data)

        assert response["status"] == "success"
        assert post.title == "Updated"
        assert post.status == BlogPostStatus.PUBLISHED
        post.save.assert_called_once_with(
            update_fields=["title", "description", "slug", "tags", "content", "status", "updated_at"]
        )

    def test_patch_internal_blog_post_updates_only_supplied_fields(self):
        request = self._request()
        post = Mock()
        data = SimpleNamespace(
            title=None,
            description="New desc",
            slug=None,
            tags=None,
            content=None,
            status=BlogPostStatus.PUBLISHED,
        )

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.get.return_value = post
            response = patch_internal_blog_post(request, blog_post_id=12, data=data)

        assert response["status"] == "success"
        assert post.description == "New desc"
        assert post.status == BlogPostStatus.PUBLISHED
        post.save.assert_called_once_with(update_fields=["description", "status", "updated_at"])

    def test_delete_internal_blog_post_deletes_existing_post(self):
        request = self._request()

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.filter.return_value.delete.return_value = (1, {})
            response = delete_internal_blog_post(request, blog_post_id=12)

        assert response["status"] == "success"
        objects.filter.assert_called_once_with(id=12)

    def test_delete_internal_blog_post_returns_404_when_missing(self):
        request = self._request()

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.filter.return_value.delete.return_value = (0, {})
            status, payload = delete_internal_blog_post(request, blog_post_id=404)

        assert status == 404
        assert payload["message"] == "Blog post not found."

    def test_review_internal_blog_post_moves_post_to_draft(self):
        request = self._request()
        post = Mock()

        with patch("apps.api.views.BlogPost.objects") as objects:
            objects.get.return_value = post
            response = review_internal_blog_post(request, blog_post_id=12)

        assert response["status"] == "success"
        assert post.status == BlogPostStatus.DRAFT
        post.save.assert_called_once_with(update_fields=["status", "updated_at"])
{% else %}


class PlaceholderApiTests(SimpleTestCase):
    def test_placeholder(self):
        assert True
{% endif %}
