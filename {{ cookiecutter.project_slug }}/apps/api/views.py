from django.http import HttpRequest
from django.db import connection
from django.core.cache import cache
from ninja import NinjaAPI
from ninja.errors import HttpError

from apps.api.auth import session_auth, superuser_api_auth
from apps.core.models import Feedback
{% if cookiecutter.generate_blog == 'y' -%}
from apps.blog.models import BlogPost
from apps.blog.choices import BlogPostStatus
{% endif -%}
from apps.api.schemas import (
    SubmitFeedbackIn,
    SubmitFeedbackOut,
    {%- if cookiecutter.generate_blog == 'y' %}
    BlogPostIn,
    BlogPostUpdateIn,
    BlogPostItemOut,
    BlogPostListOut,
    BlogPostOut,
    BlogPostDetailOut,
    {% endif -%}
    ProfileSettingsOut,
    UserSettingsOut,
)

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

api = NinjaAPI()

@api.get("/healthcheck", auth=None, include_in_schema=False, tags=["private"])
def healthcheck(request: HttpRequest):
    """
    Comprehensive healthcheck endpoint for monitoring and load balancers.

    Checks database and Redis connectivity.

    Returns:
    - 200 OK if all services are healthy
    - 503 if any service is down

    NOTE: We intentionally return boolean health fields (instead of "healthy"/"unhealthy"
    strings) to make healthcheck consumption trivial for load balancers and scripts.
    """

    checks = {
        "database": False,
        "redis": False,
    }

    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception as e:
        logger.error(
            "Healthcheck failed: Database connection error",
            error=str(e),
            exc_info=True,
        )

    # Check Redis connectivity
    try:
        cache_key = "healthcheck_test"
        cache_value = "ok"
        cache.set(cache_key, cache_value, timeout=10)
        retrieved_value = cache.get(cache_key)

        if retrieved_value == cache_value:
            checks["redis"] = True
        else:
            logger.error(
                "Healthcheck failed: Redis value mismatch",
                expected=cache_value,
                retrieved=retrieved_value,
            )
    except Exception as e:
        logger.error(
            "Healthcheck failed: Redis connection error",
            error=str(e),
            exc_info=True,
        )

    healthy = all(checks.values())
    payload = {
        "healthy": healthy,
        "checks": checks,
    }

    if healthy:
        logger.info("Healthcheck passed", **checks)
        return payload

    logger.error("Healthcheck failed", **checks)
    return 503, payload


@api.post(
    "/submit-feedback",
    response=SubmitFeedbackOut,
    auth=[session_auth],
    include_in_schema=False,
    tags=["private"],
)
def submit_feedback(request: HttpRequest, data: SubmitFeedbackIn):
    profile = request.auth
    try:
        Feedback.objects.create(profile=profile, feedback=data.feedback, page=data.page)
        return {"status": True, "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error("Failed to submit feedback", error=str(e), profile_id=profile.id)
        return {"status": False, "message": "Failed to submit feedback. Please try again."}


{% if cookiecutter.generate_blog == 'y' %}
def _serialize_blog_post(blog_post: BlogPost) -> BlogPostItemOut:
    return {
        "id": blog_post.id,
        "title": blog_post.title,
        "description": blog_post.description,
        "slug": blog_post.slug,
        "tags": blog_post.tags,
        "content": blog_post.content,
        "status": blog_post.status,
    }


@api.post(
    "/blog-posts/submit",
    response=BlogPostOut,
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def submit_blog_post(request: HttpRequest, data: BlogPostIn):
    profile = request.auth

    if not profile or not getattr(profile.user, "is_superuser", False):
        return BlogPostOut(status="error", message="Forbidden: superuser access required."), 403

    try:
        BlogPost.objects.create(
            title=data.title,
            description=data.description,
            slug=data.slug,
            tags=data.tags,
            content=data.content,
            status=data.status,
            # icon and image are ignored for now (file upload not handled)
        )
        return BlogPostOut(status="success", message="Blog post submitted successfully.")
    except Exception as e:
        return BlogPostOut(status="failure", message=f"Failed to submit blog post: {str(e)}")


@api.get(
    "/internal/blog-posts",
    response=BlogPostListOut,
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def list_internal_blog_posts(request: HttpRequest):
    blog_posts = BlogPost.objects.order_by("-created_at")
    return {"blog_posts": [_serialize_blog_post(blog_post) for blog_post in blog_posts]}


@api.get(
    "/internal/blog-posts/{blog_post_id}",
    response={200: BlogPostDetailOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def get_internal_blog_post(request: HttpRequest, blog_post_id: int):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
    except BlogPost.DoesNotExist:
        return 404, {"status": "error", "message": "Blog post not found."}

    return {
        "status": "success",
        "message": "Blog post retrieved successfully.",
        "blog_post": _serialize_blog_post(blog_post),
    }


@api.put(
    "/internal/blog-posts/{blog_post_id}",
    response={200: BlogPostDetailOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def update_internal_blog_post(request: HttpRequest, blog_post_id: int, data: BlogPostIn):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
    except BlogPost.DoesNotExist:
        return 404, {"status": "error", "message": "Blog post not found."}

    blog_post.title = data.title
    blog_post.description = data.description
    blog_post.slug = data.slug
    blog_post.tags = data.tags
    blog_post.content = data.content
    blog_post.status = data.status
    blog_post.save(update_fields=["title", "description", "slug", "tags", "content", "status", "updated_at"])

    return {
        "status": "success",
        "message": "Blog post updated successfully.",
        "blog_post": _serialize_blog_post(blog_post),
    }


@api.patch(
    "/internal/blog-posts/{blog_post_id}",
    response={200: BlogPostDetailOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def patch_internal_blog_post(request: HttpRequest, blog_post_id: int, data: BlogPostUpdateIn):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
    except BlogPost.DoesNotExist:
        return 404, {"status": "error", "message": "Blog post not found."}

    fields_to_update = []
    for field in ["title", "description", "slug", "tags", "content", "status"]:
        value = getattr(data, field)
        if value is not None:
            setattr(blog_post, field, value)
            fields_to_update.append(field)

    if fields_to_update:
        blog_post.save(update_fields=[*fields_to_update, "updated_at"])

    return {
        "status": "success",
        "message": "Blog post updated successfully.",
        "blog_post": _serialize_blog_post(blog_post),
    }


@api.delete(
    "/internal/blog-posts/{blog_post_id}",
    response={200: BlogPostOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def delete_internal_blog_post(request: HttpRequest, blog_post_id: int):
    deleted_count, _ = BlogPost.objects.filter(id=blog_post_id).delete()
    if deleted_count == 0:
        return 404, {"status": "error", "message": "Blog post not found."}

    return {"status": "success", "message": "Blog post deleted successfully."}


@api.post(
    "/internal/blog-posts/{blog_post_id}/review",
    response={200: BlogPostDetailOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def review_internal_blog_post(request: HttpRequest, blog_post_id: int):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
    except BlogPost.DoesNotExist:
        return 404, {"status": "error", "message": "Blog post not found."}

    blog_post.status = BlogPostStatus.DRAFT
    blog_post.save(update_fields=["status", "updated_at"])
    return {
        "status": "success",
        "message": "Blog post moved to draft for review.",
        "blog_post": _serialize_blog_post(blog_post),
    }


@api.post(
    "/internal/blog-posts/{blog_post_id}/publish",
    response={200: BlogPostDetailOut, 404: BlogPostOut},
    auth=[superuser_api_auth],
    include_in_schema=False,
    tags=["admin"],
)
def publish_internal_blog_post(request: HttpRequest, blog_post_id: int):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
    except BlogPost.DoesNotExist:
        return 404, {"status": "error", "message": "Blog post not found."}

    blog_post.status = BlogPostStatus.PUBLISHED
    blog_post.save(update_fields=["status", "updated_at"])
    return {
        "status": "success",
        "message": "Blog post published successfully.",
        "blog_post": _serialize_blog_post(blog_post),
    }
{% endif %}

@api.get(
    "/user/settings",
    response=UserSettingsOut,
    auth=[session_auth],
    include_in_schema=False,
    tags=["private"],
)
def user_settings(request: HttpRequest):
    profile = request.auth
    try:
        profile_data = {
            {% if cookiecutter.use_stripe == 'y' %}
            "has_pro_subscription": profile.has_active_subscription,
            {% endif %}
        }
        data = {"profile": profile_data}

        return data
    except Exception as e:
        logger.error(
            "Error fetching user settings",
            error=str(e),
            profile_id=profile.id,
            exc_info=True,
        )
        raise HttpError(500, "An unexpected error occurred.")
