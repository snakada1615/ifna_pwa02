import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator():
  
  def validate(self, password, user=None): 
    pattern = "[a-zA-Z-0-9~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not re.match(pattern, password):
      raise ValidationError("Password must contain letters, digits and special characters only")

  def get_help_text(self):
    return ("Password must contain letters, digits and special characters only. HIHI")