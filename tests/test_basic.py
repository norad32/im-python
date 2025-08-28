from im_python import __version__, about


def test_version():
    assert isinstance(__version__, str) and len(__version__) >= 5


def test_about():
    assert "template" in about().lower()
