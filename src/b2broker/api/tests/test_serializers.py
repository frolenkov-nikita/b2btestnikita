import pytest

from rest_framework_json_api import serializers

from api.serializers import non_negative_validator, non_zero_validator


def test_non_negative_validator():
    with pytest.raises(serializers.ValidationError):
        non_negative_validator(-1)

    non_negative_validator(0)


def test_non_zero_validator():
    with pytest.raises(serializers.ValidationError):
        non_zero_validator(0)

    non_zero_validator(1)
    non_zero_validator(-1)
