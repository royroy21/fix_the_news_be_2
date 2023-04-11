from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class EmailValidator(validators.RegexValidator):
    regex = r'[^@]+@[^@]+\.[^@]+'
    message = _('Enter a valid email address')
    flags = 0
