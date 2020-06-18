import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall("\d", password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 digit, 0-9.")


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", "[a-z]", password):
            raise ValidationError(
                _("The password must have at least one character"),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Your password must have at least one character")
