import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator():

  def validate(self, password, user=None):
    pattern = r"[a-zA-Z-0-9~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not re.match(pattern, password):
      raise ValidationError({'password': [
        ('Your input for [%(field_name)s] is invalid! Please confirm and try again.') % {'field_name': ('Password')}]})

  def get_help_text(self):
    return ''
