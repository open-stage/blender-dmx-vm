import os
import re
import shutil

class Manager:

    VERSIONS_DIR = 'versions'
    PROFILES_BACKUP_DIR = 'profiles'

    @staticmethod
    def _addons_path():
        root = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(root, '..')

    @staticmethod
    def _dmx_path():
        return os.path.join(Manager._addons_path(), 'dmx')

    @staticmethod
    def _dmx_init_path():
        return os.path.join(Manager._dmx_path(), '__init__.py')

    @staticmethod
    def _dmx_profiles_path():
        return os.path.join(Manager._dmx_path(), 'assets', 'profiles')

    @staticmethod
    def _dmx_branch_tag_path():
        return os.path.join(Manager._dmx_path(), 'branch')

    @staticmethod
    def _versions_path():
        root = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(root, Manager.VERSIONS_DIR)

    @staticmethod
    def _profiles_backup_path():
        root = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(root, Manager.PROFILES_BACKUP_DIR)

    @staticmethod
    def version_filepath(tag_name):
        root = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(root, Manager.VERSIONS_DIR, tag_name+'.zip')

    @staticmethod
    def get_installed_versions():
        files = os.listdir(Manager._versions_path())
        versions = [filename[:-4] for filename in files if '.zip' in filename]
        return versions

    @staticmethod
    def remove_version(version):
        os.remove(Manager.version_filepath(version.tag_name))

    @staticmethod
    def is_blenderdmx_installed():
        path = Manager._dmx_path()
        path_exists = os.path.exists(path)
        path_empty = len(os.listdir(path)) == 0
        return path_exists and not path_empty

    @staticmethod
    def get_active_version_tag():
        branch_tag_path = Manager._dmx_branch_tag_path()
        if (os.path.exists(branch_tag_path)):
            with open(branch_tag_path, 'r') as file:
                return file.read()

        with open(Manager._dmx_init_path(), 'r') as file:
            for line in file:
                matches = re.findall(r'[\'"]version[\'"]: \( *(\d+) *, *(\d+) *, *(\d+) *\)', line)
                if (len(matches)):                    
                    major, minor, patch = matches[0]
                    tag = f'v{major}.{minor}.{patch}'
                    return tag
