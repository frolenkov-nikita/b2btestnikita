import pytest

from django.core.exceptions import ValidationError as DjValidationError
from rest_framework_json_api import serializers

from api.validators import NonZeroValidator, NonNegativeValidator


def test_non_negative_validator():
    for exc_cls in [serializers.ValidationError, DjValidationError]:
        with pytest.raises(exc_cls):
            NonNegativeValidator(exc_cls)(-1)

    NonNegativeValidator(DjValidationError)(1)


def test_non_zero_validator():
    for exc_cls in [serializers.ValidationError, DjValidationError]:
        with pytest.raises(exc_cls):
            NonZeroValidator(exc_cls)(0)

    NonZeroValidator(DjValidationError)(-1)
    NonZeroValidator(DjValidationError)(1)
