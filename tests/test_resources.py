def test_asset_exists_and_is_readable():
    from im_python.resources import resource, open_text

    p = resource("app_settings/icon.png")
    assert p.exists() and p.is_file()
    try:
        with open_text("defaults/config.json") as f:
            assert f.read()
    except FileNotFoundError:
        pass
