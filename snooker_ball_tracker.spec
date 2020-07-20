# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src/snooker_ball_tracker/__main__.py'],
             pathex=['/home/dblack/snooker-ball-tracker'],
             binaries=[],
             datas=[ ('src/snooker_ball_tracker/config/*.py', 'config') ],
             hiddenimports=['PIL._tkinter_finder'],
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
          name='snooker_ball_tracker.exe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
