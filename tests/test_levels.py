import pytest

from im_python.app_logger.levels import Level


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("debug", Level.DEBUG),
        (" WARN ", Level.WARNING),
        ("fatal", Level.CRITICAL),
        ("20", Level.INFO),
        (30, Level.WARNING),
        (Level.ERROR, Level.ERROR),
    ],
)
def test_parse_Should_ReturnLevel_If_ValueIsValid(value, expected):
    assert Level.parse(value) is expected


@pytest.mark.parametrize("value", ["unknown", "999", 999])
def test_parse_Should_RaiseValueError_If_ValueIsInvalid(value):
    with pytest.raises(ValueError):
        Level.parse(value)
