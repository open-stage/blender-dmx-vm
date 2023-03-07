import re
import os
import shutil
from distutils.dir_util import copy_tree
from pygit2 import Repository

BUILD_DIR = 'build'
BLENDER_PACKAGE_NAME = 'dmx-vm'

branch_name = Repository('.').head.shorthand
if (branch_name == None):
    raise Exception('Run the script from the project root.')

zip_name = 'blender-dmx-vm@' + branch_name

print('---------')
print('branch name: ' + branch_name)
print('zip name: ' + zip_name + '.zip')
print('---------')

print('Resetting build directory...')
if (os.path.exists(BUILD_DIR)):
    shutil.rmtree(BUILD_DIR)
os.mkdir(BUILD_DIR)
os.mkdir(BUILD_DIR+'/'+BLENDER_PACKAGE_NAME)

print('Copying dependencies to build directory...')
copy_tree('profiles', BUILD_DIR+'/'+BLENDER_PACKAGE_NAME+'/profiles')
copy_tree('versions', BUILD_DIR+'/'+BLENDER_PACKAGE_NAME+'/versions')

print('Copying source to build directory...')
for filename in os.listdir('.'):
    if filename.endswith('.py'):
        shutil.copy2(filename, BUILD_DIR+'/'+BLENDER_PACKAGE_NAME)

print('Copying metadata to build directory...')
shutil.copy2('LICENSE', BUILD_DIR+'/'+BLENDER_PACKAGE_NAME)

print('Zipping release...')
shutil.make_archive(zip_name, 'zip', BUILD_DIR)

print('Clearing build directory...')
shutil.rmtree(BUILD_DIR)

print('Build successfull! Have a great release!')