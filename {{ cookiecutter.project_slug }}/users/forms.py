from allauth.account.forms import LoginForm, SignupForm
from {{cookiecutter.project_slug}}.utils import DivErrorList  # noqa: E999


class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
      super(CustomSignUpForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super(CustomLoginForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList
