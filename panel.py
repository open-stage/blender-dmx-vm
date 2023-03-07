#
#   BlendexDMX > Panels > Groups
#
#   - Create/Update/Rename/Remove Groups
#   - Select Fixtures by group for programming
#
#   http://www.github.com/open-stage/BlenderDMX
#

import bpy
import requests
import json

from bpy.props import (StringProperty, BoolProperty)

from bpy.types import (Panel,
                       Menu,
                       Operator,
                       UIList)

from .github import GitHub

# # List #

class DMX_UL_Version(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        dmx_vm = context.scene.dmx_vm
        if (dmx_vm.active_version == index):
            icon = 'SOLO_ON'
        elif (item.installed):
            icon = 'KEYFRAME_HLT'
        else:
            icon = 'KEYFRAME'
        layout.label(text = item.name, icon = icon)

# # Menus #

class DMX_MT_Version(Menu):
    bl_label = "DMX > Version Menu"
    bl_idname = "DMX_MT_Version"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        dmx_vm = scene.dmx_vm

        version = None
        if (len(dmx_vm.versions)):
            version = dmx_vm.versions[dmx_vm.selected_version]

        is_installed = version.installed if version else False
        is_active = dmx_vm.selected_version == dmx_vm.active_version
        is_branch = version.tag_name.startswith('branch-')

        row = layout.row()
        row.operator("dmx.version_search", text="Search New Versions", icon="VIEWZOOM")

        row = layout.row()
        download_text = "Download"
        if (is_branch and is_installed):
            download_text = "Update"
        row.operator("dmx.version_download", text=download_text, icon="IMPORT")
        row.enabled = is_branch or not is_installed

        row = layout.row()
        row.operator("dmx.version_remove", text="Remove", icon="TRASH")
        row.enabled = is_installed

        row = layout.row()
        row.operator("dmx.version_use", text="Use", icon="SOLO_ON")
        row.enabled = is_installed and not is_active

# # Operators #

class DMX_OT_Version_Search(Operator):
    bl_label = "DMX > Version > Search"
    bl_idname = "dmx.version_search"
    bl_description = "Search new versions on GitHub"
    bl_options = {'UNDO'}

    def execute(self, context):
        dmx_vm = context.scene.dmx_vm
        dmx_vm.search_versions()
        return {'FINISHED'}

class DMX_OT_Version_Download(Operator):
    bl_label = "DMX > Version > Download"
    bl_idname = "dmx.version_download"
    bl_description = "Download selected version"
    bl_options = {'UNDO'}

    def execute(self, context):
        dmx_vm = context.scene.dmx_vm
        version = dmx_vm.versions[dmx_vm.selected_version]

        if (version.tag_name.startswith('branch-') and version.installed):
            dmx_vm.update_version(version)
        else:
            dmx_vm.download_version(version)

        return {'FINISHED'}

class DMX_OT_Version_Remove(Operator):
    bl_label = "DMX > Version > Remove"
    bl_idname = "dmx.version_remove"
    bl_description = "Remove selected version"
    bl_options = {'UNDO'}

    def execute(self, context):
        dmx_vm = context.scene.dmx_vm
        version = dmx_vm.versions[dmx_vm.selected_version]
        dmx_vm.remove_version(version)
        return {'FINISHED'}

class DMX_OT_Version_Use(Operator):
    bl_label = "DMX > Version > Use"
    bl_idname = "dmx.version_use"
    bl_description = "Use selected version"
    bl_options = {'UNDO'}

    def execute(self, context):
        dmx_vm = context.scene.dmx_vm
        version = dmx_vm.versions[dmx_vm.selected_version]
        dmx_vm.use_version(version)
        return {'FINISHED'}

# Panel #

class DMX_PT_VersionManager(Panel):
    bl_label = "Version Manager"
    bl_idname = "DMX_PT_VersionManager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DMX"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        dmx_vm = context.scene.dmx_vm

        row = layout.row()
        row.template_list("DMX_UL_Version", "", dmx_vm, "versions", dmx_vm, "selected_version", rows=4)
        row.enabled = not dmx_vm.mutex

        row = layout.row()
        row.menu("DMX_MT_Version", text="...", icon="STICKY_UVS_LOC")
        row.enabled = not dmx_vm.mutex

        row = layout.row()
        row.prop(dmx_vm, 'include_branches')
        row.enabled = not dmx_vm.mutex

        row = layout.row()
        row.label(text = dmx_vm.status)
