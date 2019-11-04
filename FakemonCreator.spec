# -*- mode: python -*-
from pathlib import Path
import sys
import importlib

package_imports = [['qtmodern', ['resources/frameless.qss', 'resources/style.qss']]]

added_file = [("creator/res", "res")]
for package, files in package_imports:
    proot = Path(importlib.import_module(package).__file__).parent
    added_file.extend((proot / f, package) for f in files)


block_cipher = None

if sys.platform.startswith('win'):
    pathex = ['C:\\Windows\\WinSxS', Path().cwd()]
elif sys.platform.startswith('darwin'):
    pathex = [Path().cwd()]

print("System:", sys.platform)

a = Analysis(['creator/__main__.py'],
             pathex=pathex,
             binaries=[],
             datas=added_file,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          icon="creator/res/icon_96.ico",
          name='Fakemon.Creator.WIN',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)

app = BUNDLE(exe,
             name='Fakemon.Creator.OSX.app',
             bundle_identifier=None)

if sys.platform.startswith('darwin'):
    import zipfile
    input_filename = Path("./dist/Fakemon.Creator.OSX.app")
    output_filename = Path("./dist/Fakemon.Creator.OSX.zip")
    directory = input_filename.parent
    with zipfile.ZipFile(output_filename, "w") as zip:
        for file in input_filename.glob("**/*.*"):
            # add directory (needed for empty dirs)
            zip.write(file.parent, file.parent.relative_to(directory))
            zip.write(file, file.relative_to(directory))
