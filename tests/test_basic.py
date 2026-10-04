from im_python import __version__, about


def test_version_Should_BeNonemptyString():
    assert isinstance(__version__, str)
    assert __version__


def test_about_Should_MentionTemplate():
    assert "template" in about().lower()
