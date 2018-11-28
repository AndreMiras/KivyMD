# -*- mode: python -*-

import os
import kivymd

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\LAPTOP MSI\\Documents\\KivyMD\\demos\\kitchen_sink'],
             binaries=[],
             datas=[(os.path.dirname(kivymd.__file__), 'kivymd'),
                    ('./assets','assets')],
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
          [],
          exclude_binaries=True,
          name='.kivyMD',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='kivyMD')
