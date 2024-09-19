from django.views.generic import TemplateView

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

class HomeView(TemplateView):
    template_name = "pages/home.html"
