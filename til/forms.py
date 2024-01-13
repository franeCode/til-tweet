from allauth.account.forms import LoginForm
from til.utils import DivErrorList

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super(CustomLoginForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList