from django.http import HttpRequest
from ninja import NinjaAPI

from core.api.auth import MultipleAuthSchema
from core.models import Feedback
from core.api.schemas import (
    SubmitFeedbackIn,
    SubmitFeedbackOut,
    {% if cookiecutter.generate_blog == 'y' %}
    BlogPostIn,
    BlogPostOut,
    {% endif %}
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
