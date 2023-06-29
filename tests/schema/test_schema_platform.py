import pytest

from app.schema.apiv1 import Platform


def test_platform_valid_value():
    assert Platform("telegram") == Platform.telegram
    assert Platform("instagram") == Platform.instagram
    assert Platform("twitter") == Platform.twitter
    assert Platform("whatsapp") == Platform.whatsapp
    assert Platform("facebook") == Platform.facebook
    assert Platform("linkedin") == Platform.linkedin
    assert Platform("clubhouse") == Platform.clubhouse


def test_platform_invalid_value():
    with pytest.raises(ValueError):
        Platform("invalid_platform")
