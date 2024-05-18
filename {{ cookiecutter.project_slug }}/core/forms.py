from allauth.account.forms import LoginForm, SignupForm

from .utils import DivErrorList


class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.error_class = DivErrorList

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.error_class = DivErrorList
