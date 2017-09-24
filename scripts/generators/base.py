# Base generator.
# All other generators inherit from this
#
# @author Daniel J. Finnegan
# @date September 2017

import os
from os import path
import logging
from logging import handlers
import re

version_number = 1.0 # Updater version number
author_name = 'Daniel J. Finnegan'

template_keys = {
    'version_number': 1.0,
    'author_name': 'Daniel J. Finnegan'
}

class ProjectGenerator():

    def __init__(self, proj_root):
        self.initialize(proj_root)

    def initialize(self, proj_root):
        self.project_root = proj_root
        self.logger = logging.getLogger('updater_application')
        self.template_name = 'base.txt'

    def write_cmake_file(self):
        # pass
        with open (os.path.join(os.getcwd(), 'templates', self.template_name)) as f:
            lines = f.readlines()

        def replace_key_vals(match):
            for key, value in template_keys.iteritems():
                if key in match.string():
                    return value

        regex = re.compile(r">>>>>{(\w+)}")
        for line in lines:
            line = re.sub(regex, replace_key_vals, line)

        with open(os.path.join(self.project_root, 'CMakeLists.txt'), 'w') as cmake_file:
            cmake_file.write(lines)


    def write_readme_file(self):
        file_contents = (
            '# ' + os.path.basename(self.project_root) +'\n'
            'Put your README information here\n'
        )

        with open(os.path.join(self.project_root, 'README.md'), 'w') as readme_file:
            readme_file.write(file_contents)

    def write_build_file(self):
        file_contents = (
            '#\n'
            '# Module automatically generated by Updater v' + str(version_number) + '\n'
            '# @author ' + author_name + '\n'
            '#\n'
            '\n'
            'import os\n'
            'from subprocess import call\n'
            '\n'
            'UPDATER_CMAKE_ARGS = [] # Required CMake arguments for Updater\n'
            'UPDATER_BUILD_CUSTOM = False # Set this to True if your project has a custom build function\n'
            '\n'
            '# Default implementation just calls cmake\n'
            '# Reimplement as you see fit\n'
            'def build_full_package(project_root):\n'
            '\tif not os.path.isdir(os.path.join(project_root, \'bin\')):\n'
            '\t\tos.mkdir(os.path.join(project_root, \'bin\'))\n'
            '\n'
            '\tos.chdir(os.path.join(project_root, \'bin\'))\n'
            '\tcall([\'cmake\'] + UPDATER_CMAKE_ARGS + [\'..\'])\n'
            '\tcall([\'cmake\', \'--build\', \'.\'])\n'
            '\n####################################################################\n'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', 'build_project.py'), 'w') as build_module:
            build_module.write(file_contents)

    def write_sample_source_file(self):
        pass

    def write_init_file(self):
        file_contents = (
            '# __init__ file for module\n'
            '# @author ' + author_name + '\n'
            '\n'
            '__all__ = [\'build_project\']\n'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', '__init__.py'), 'w') as init_module:
            init_module.write(file_contents)

    def generate_project(self):
        if os.path.isdir(self.project_root):
            self.logger.info('Project already exists! Aborting...')
            return 1
        else:
            os.mkdir(self.project_root)
            os.mkdir(os.path.join(self.project_root, 'scripts'))
            os.mkdir(os.path.join(self.project_root, 'scripts', 'builder'))

            self.write_init_file()
            self.write_readme_file()
            self.write_build_file()
            self.write_cmake_file()
            self.write_sample_source_file()
            return 0

###########################################################