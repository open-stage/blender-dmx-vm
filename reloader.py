import bpy
import sys
import importlib
import dmx

class Reloader:

    @staticmethod
    def _clean_module_imports():
        modules = dict(sys.modules)
        for name in modules.keys():
            if (name == 'dmx'):
                continue
            if name.startswith('dmx'):
                del sys.modules[name]
        return None 

    @staticmethod
    def _reload_old_versions(tag_name):
        if (tag_name == 'v0.5.0-beta' or tag_name == 'v1.0.0-vanilla'):
            dmx.onLoadFile(None)

    @staticmethod
    def reload(tag_name):
        print('BlenderDMX: Reloading dmx add-on...')
        module = sys.modules.get('dmx')

        module.unregister()
        Reloader._clean_module_imports()
        importlib.reload(module)
        module.register()

        Reloader._reload_old_versions(tag_name)