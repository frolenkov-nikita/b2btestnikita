from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class BaseValidator:
    def __init__(self, exc_cls, msg=None):
        self.exc_cls = exc_cls
        if msg:
            self.msg = msg

    def __call__(self, value):
        if not self._is_valid(value):
            raise self.exc_cls(self.msg)

    def _is_valid(self, value):
        raise NotImplementedError


@deconstructible
class NonNegativeValidator(BaseValidator):
    msg = _("Must be greater or equal to 0.")

    def _is_valid(self, value):
        return value >= 0


@deconstructible
class NonZeroValidator(BaseValidator):
    msg = _("Must be greater or equal to 0.")

    def _is_valid(self, value):
        return value != 0
