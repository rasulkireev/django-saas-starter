from django.http import HttpRequest
from ninja import NinjaAPI

from core.api.auth import MultipleAuthSchema
from core.api.schemas import (
    TestIn,
    TestOut,
)

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

api = NinjaAPI(auth=MultipleAuthSchema(), csrf=True)

@api.post("/test", response=TestOut)
def test(request: HttpRequest, data: TestIn):
    return TestOut(greeting=data.greeting)
