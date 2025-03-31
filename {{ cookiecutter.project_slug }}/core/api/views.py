from django.http import HttpRequest
from ninja import NinjaAPI

from core.api.auth import MultipleAuthSchema
from core.models import Feedback
from core.api.schemas import (
    SubmitFeedbackIn,
    SubmitFeedbackOut,
)

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

api = NinjaAPI(auth=MultipleAuthSchema(), csrf=True)

@api.post("/submit-feedback", response=SubmitFeedbackOut)
def submit_feedback(request: HttpRequest, data: SubmitFeedbackIn):
    profile = request.auth
    try:
        Feedback.objects.create(profile=profile, feedback=data.feedback, page=data.page)
        return {"status": "success", "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error("Failed to submit feedback", error=str(e), profile_id=profile.id)
        return {"status": "error", "message": "Failed to submit feedback. Please try again."}
