from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("im_python", includes=["assets/*"])

block_cipher = None

a = Analysis(
    ['../scripts/run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='ImPython',
    console=False,            # True if you want a console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,                # e.g. "installer/app.ico" on Windows
)
