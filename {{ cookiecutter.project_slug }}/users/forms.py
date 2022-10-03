from allauth.account.forms import SignupForm
from {{ cookiecutter.project_slug }}.utils import DivErrorList

class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
      super(CustomSignUpForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList