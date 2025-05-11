from ninja import Schema
from typing import Optional

{% if cookiecutter.generate_blog == 'y' %}
from core.choices import BlogPostStatus
{% endif %}


class SubmitFeedbackIn(Schema):
    feedback: str
    page: str

class SubmitFeedbackOut(Schema):
    success: bool
    message: str

{% if cookiecutter.generate_blog == 'y' %}
class BlogPostIn(Schema):
    title: str
    description: str = ""
    slug: str
    tags: str = ""
    content: str
    icon: Optional[str] = None  # URL or base64 string
    image: Optional[str] = None  # URL or base64 string
    status: BlogPostStatus = BlogPostStatus.DRAFT


class BlogPostOut(Schema):
    status: str  # API response status: 'success' or 'failure'
    message: str
{% endif %}
