from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

SPECIAL_CHARACTERS = r"!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~"

class PasswordComplexityValidator:
    def __init__(self, min_uppercase=1, min_lowercase=1, min_digits=1, min_special_chars=1):
        self.min_uppercase = int(min_uppercase)
        self.min_lowercase = int(min_lowercase)
        self.min_digits = int(min_digits)
        self.min_special_chars = int(min_special_chars)

    def validate(self, password, user=None):
        if password is None:
            return

        errors = []
        uppercase_count = sum(1 for c in password if c.isupper())
        lowercase_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        special_count = sum(1 for c in password if c in SPECIAL_CHARACTERS)

        if uppercase_count < self.min_uppercase:
            errors.append(_(f'Password must contain at least {self.min_uppercase} uppercase letter(s).'))
        if lowercase_count < self.min_lowercase:
            errors.append(_(f'Password must contain at least {self.min_lowercase} lowercase letter(s).'))
        if digit_count < self.min_digits:
            errors.append(_(f'Password must contain at least {self.min_digits} digit(s).'))
        if special_count < self.min_special_chars:
            errors.append(_(f'Password must contain at least {self.min_special_chars} special character(s).'))

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            'Your password must contain at least '
            f'{self.min_uppercase} uppercase letter(s), '
            f'{self.min_lowercase} lowercase letter(s), '
            f'{self.min_digits} digit(s), and '
            f'{self.min_special_chars} special character(s).'
        )
