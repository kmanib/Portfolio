import os

class Environment:
    @staticmethod
    def getExternalStorageDirectory():
        # Maps Android external storage to Linux user's Documents folder
        # or a sandboxed XDG directory.
        xdg_docs = os.environ.get('XDG_DOCUMENTS_DIR', os.path.expanduser('~/Documents'))
        ares_dir = os.path.join(xdg_docs, 'ARES_Storage')
        os.makedirs(ares_dir, exist_ok=True)
        return ares_dir

    @staticmethod
    def getDataDirectory():
        # Maps Android data directory to XDG data home
        data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        ares_data = os.path.join(data_home, 'ares')
        os.makedirs(ares_data, exist_ok=True)
        return ares_data
