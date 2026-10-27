"""
Video to Markdown Suite
Professional tool to convert video content into structured study notes.
"""

import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    try:
        import subprocess
        _orig_popen_init = subprocess.Popen.__init__

        def _silent_popen_init(self, *args, **kwargs):
            creationflags = kwargs.get('creationflags', 0)
            creationflags |= getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
            kwargs['creationflags'] = creationflags
            return _orig_popen_init(self, *args, **kwargs)

        subprocess.Popen.__init__ = _silent_popen_init
    except Exception:
        pass

__version__ = "0.1.0"
