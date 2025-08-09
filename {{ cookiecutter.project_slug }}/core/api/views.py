from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.errors import HttpError

from core.api.auth import MultipleAuthSchema
from core.models import Feedback, {% if cookiecutter.generate_blog == 'y' %}BlogPost{% endif %}
from core.api.schemas import (
    SubmitFeedbackIn,
    SubmitFeedbackOut,
    {%- if cookiecutter.generate_blog == 'y' %}
    BlogPostIn,
    BlogPostOut,
    {% endif -%}
    ProfileSettingsOut,
    UserSettingsOut,
)

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

api = NinjaAPI(auth=MultipleAuthSchema(), csrf=False)

@api.post("/submit-feedback", response=SubmitFeedbackOut)
def submit_feedback(request: HttpRequest, data: SubmitFeedbackIn):
    profile = request.auth
    try:
        Feedback.objects.create(profile=profile, feedback=data.feedback, page=data.page)
        return {"status": True, "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error("Failed to submit feedback", error=str(e), profile_id=profile.id)
        return {"status": False, "message": "Failed to submit feedback. Please try again."}

{% if cookiecutter.generate_blog == 'y' %}
@api.post("/blog-posts/submit", response=BlogPostOut)
def submit_blog_post(request: HttpRequest, data: BlogPostIn):
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
{% endif %}

@api.get("/user/settings", response=UserSettingsOut)
def user_settings(request: HttpRequest):
    profile = request.auth
    try:
        profile_data = {
            "has_pro_subscription": profile.has_active_subscription,
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
