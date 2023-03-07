import os
import re
import shutil

from .manager import Manager

class Installer:

    @staticmethod
    def _backup_profiles():
        print('BlenderDMX: Backing up profiles...')
        dmx_path = Manager._dmx_profiles_path()
        backup_path = Manager._profiles_backup_path()

        for filename in os.listdir(dmx_path):
            filepath = os.path.join(dmx_path, filename)
            shutil.copy(filepath, backup_path)

    @staticmethod
    def _restore_profiles():
        print('BlenderDMX: Restoring profiles...')
        dmx_path = Manager._dmx_profiles_path()
        backup_path = Manager._profiles_backup_path()

        for filename in os.listdir(backup_path):
            if (filename == 'README.md'):
                continue
            filepath = os.path.join(backup_path, filename)
            shutil.copy(filepath, dmx_path)

    @staticmethod
    def _remove_current():
        print('BlenderDMX: Uninstalling current BlenderDMX version...')
        dmx_path = Manager._dmx_path()
        for filename in os.listdir(dmx_path):
            node = os.path.join(dmx_path, filename)
            try:
                if os.path.isfile(node) or os.path.islink(node):
                    os.unlink(node)
                elif os.path.isdir(node):
                    shutil.rmtree(node)
            except Exception as e:
                print('BlenderDMX: Failed to delete %s. Reason: %s' % (node, e))

    @staticmethod
    def _unpack_branch_version(path, tag_name):
        branch = tag_name[7:]
        branch_path = os.path.join(path, 'blender-dmx-'+branch)
        for filename in os.listdir(branch_path):
            node = os.path.join(branch_path, filename)
            if os.path.isfile(node) or os.path.islink(node):
                shutil.copy(node, path)
            elif os.path.isdir(node):
                shutil.copytree(node, os.path.join(path,filename))
        shutil.rmtree(branch_path)

    @staticmethod
    def _add_branch_tag(path, tag_name):
        branch_tag_path = os.path.join(path, 'branch')
        with open(branch_tag_path, 'w') as file:
            file.write(tag_name)

    @staticmethod
    def _unzip_version(tag_name):
        print(f'BlenderDMX: Unzipping version {tag_name}...')
        is_branch_version = tag_name.startswith('branch-')
        version_filepath = Manager.version_filepath(tag_name)
        
        path = Manager._addons_path()
        if (is_branch_version):
            path = Manager._dmx_path()

        shutil.unpack_archive(version_filepath, path)

        if (is_branch_version):
            Installer._unpack_branch_version(path, tag_name)
            Installer._add_branch_tag(path, tag_name)
            
    @staticmethod
    def use_version(version):
        pre_existing = Manager.is_blenderdmx_installed()
        if (pre_existing):
            Installer._backup_profiles()
            Installer._remove_current()

        Installer._unzip_version(version.tag_name)

        if (pre_existing):
            Installer._restore_profiles()