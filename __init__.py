bl_info = {
    "name": "DMX Version Manager",
    "description": "Manage Blender DMX Version",
    "author": "Open Stage",
    "version": (1, 0, 1),
    "blender": (3, 0, 0),
    "location": "3D View > DMX Version Manager",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "http://www.github.com/open-stage/blenderDMX/wiki",
    "tracker_url": "",
    "category": "Lighting"
}

import sys
import bpy
import json

from threading import Timer

from bpy.types import (PropertyGroup)
from bpy.props import (
    StringProperty,
    BoolProperty,
    CollectionProperty,
    PointerProperty,
    IntProperty
)

from .manager import Manager
from .reloader import Reloader
from .installer import Installer
from .github import GitHub
from .panel import *

class DMX_Version(PropertyGroup):
    tag_name: StringProperty(
        name = "Name")
    name: StringProperty(
        name = "Name")
    download_url: StringProperty(
        name = "Name")
    installed: BoolProperty(
        name = "Installed")

class DMX_VersionManager(PropertyGroup):
    versions: CollectionProperty(
        name = "DMX Fixtures",
        type = DMX_Version)

    selected_version : IntProperty(
        name = "Selected Version",
        default = 0)

    active_version: IntProperty(
        name = "Active Version",
        default = -1)

    status: StringProperty(
        name = "Status")

    mutex: BoolProperty(
        name = "mutex")

    include_branches: BoolProperty(
        name = "Include Branches on Search",
        default = False
    )

    def _update(self, versions=[]):
        print('BlenderDMX: Updating version list...')
        self.status = "Updating version list..."
        self.mutex = True

        if (len(versions)):
            self.versions.clear()
            for version in versions:
                tag_name = version['tag_name']
                name = version['name']
                download_url = version['assets'][0]['browser_download_url']
                # print(f'{tag_name} | {name} {download_url}')

                self.versions.add()
                self.versions[-1].tag_name = tag_name
                self.versions[-1].name = name
                self.versions[-1].download_url = download_url

        installed_versions = Manager.get_installed_versions()
        for version in self.versions:
            installed = version['tag_name'] in installed_versions
            version.installed = installed

        self.active_version = -1
        if (Manager.is_blenderdmx_installed()):
            active_version_tag = Manager.get_active_version_tag()
            for i, version in enumerate(self.versions):
                if (version['tag_name'].startswith(active_version_tag)):
                    self.active_version = i
                    break

        self.selected_version = -1
        self.mutex = False
        self.status = ""

    def _error(self, e):
        self.status = 'Failed. Check terminal.'
        self.mutex = False
        print(e)

    def _include_branches(self, versions, branches):
        for branch in branches:
            version = {
                'tag_name': 'branch-'+branch['name'],
                'name': f'[{branch["name"]}]',
                'assets': [{
                    'browser_download_url': f'https://github.com/open-stage/blender-dmx/archive/refs/heads/{branch["name"]}.zip',
                }]
            }
            versions.insert(0,version)

    def search_branches(self, then):
        print('BlenderDMX: Searching for branch versions...')
        self.status = 'Downloading branch list...'

        try:
            releases = GitHub.get_branches(then, self._error)
        except Exception as e:
            self._error(e)

    def search_versions(self):
        print('BlenderDMX: Searching for new versions...')
        self.status = 'Downloading version list...'
        self.mutex = True

        def then(versions):
            def then_branches(branches):
                self._include_branches(versions, branches)
                self._update(versions)
                self.status = ""

            versions = versions[:-2]
            if (self.include_branches):
                self.search_branches(then_branches)
            else:
                self._update(versions)
                self.status = ""

        try:
            releases = GitHub.get_releases(then, self._error)
        except Exception as e:
            self._error(e)

    def download_version(self, version):
        print(f'BlenderDMX: Downloading version "{version.name}"')
        print(f'\t{version.download_url}')
        self.status = f'Downloading {version.name}...'
        self.mutex = True

        def then():
            self._update()
            self.status = f'{version.name} downloaded'

        try:
            url = version.download_url
            filepath = Manager.version_filepath(version.tag_name)
            GitHub.download(url, filepath, then, self._error)
        except Exception as e:
            self._error(e)

    def update_version(self, version):
        print(f'BlenderDMX: Updating version "{version.name}"')
        self.download_version(version)
        if (self.selected_version == self.active_version):
            self.use_version(version)

    def remove_version(self, version):
        print(f'BlenderDMX: Removing version "{version.name}"')
        self.status = f'Removing {version.name}...'
        self.mutex = True

        try:
            Manager.remove_version(version)
            self._update()
            self.status = f'{version.name} removed'
        except Exception as e:
            self._error(e)

    def use_version(self, version):
        print(f'BlenderDMX: Switching to version "{version.name}"')
        self.status = f'Switching to {version.name}...'
        self.mutex = True

        try:
            Installer.use_version(version)
            self._update()
            self.status = f'{version.name} loaded'
            Reloader.reload(version.tag_name)
        except Exception as e:
            self._error(e)

# Blender API registering

classes = (
    DMX_Version,
    DMX_VersionManager,
    DMX_UL_Version,
    DMX_MT_Version,
    DMX_OT_Version_Search,
    DMX_OT_Version_Download,
    DMX_OT_Version_Remove,
    DMX_OT_Version_Use,
    DMX_PT_VersionManager
)

def on_register():
    bpy.context.scene.dmx_vm.search_versions()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dmx_vm = PointerProperty(type=DMX_VersionManager)
    Timer(1, on_register, ()).start()

def clean_module_imports():
    modules = dict(sys.modules)
    for name in modules.keys():
        if (name == __name__):
            continue
        if name.startswith(__name__):
            del sys.modules[name]
    return None 

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    clean_module_imports()

if __name__ == "__main__":
    register()