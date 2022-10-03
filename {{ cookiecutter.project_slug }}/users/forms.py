from allauth.account.forms import SignupForm, LoginForm
from {{ cookiecutter.project_slug }}.utils import DivErrorList

class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
      super(CustomSignUpForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super(CustomLoginForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList