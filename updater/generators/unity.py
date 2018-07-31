# This is the build script for Updater.
# This enables Updater to operate in a recursive manner; it can update itself!
#
# @author Daniel J. Finnegan
# @date July 2017

import os
from os import path
import logging
from logging import handlers
import re
import generators.base_gen as base_gen

class UnityGenerator(base_gen.ProjectGenerator):

    def __init__(self, proj_root):
        super(UnityGenerator, self).__init__(proj_root)
        self.template_name = 'unity.txt'
        self.template_keys['projname'] =  'Unity-Updater-Project'
        self.template_keys['appname'] =  'Unity-Application'
        self.template_keys['appnote'] =  'An updater-generated Unity Application'
        self.template_keys['proj_languages'] = 'NONE'
        self.cmake_module_files = ['FindUnityGame.cmake']

    def write_sample_source_file(self):
        if not os.path.isdir(os.path.join(self.project_root, 'unity')):
            os.mkdir(os.path.join(self.project_root, 'unity'))

        file_contents = (
            'Automatically generated by Updater v' + str(self.template_keys['version_number']) + '\n'
            '@author ' + self.template_keys['author_name'] + '\n\n'
            '# Generate your Unity Project here\n'
            '# You will need to keep the GetUnityVersion.cs file located in the Assets/Editor folder\n'
        )

        with open(os.path.join(self.project_root, 'unity', 'README.txt'), 'w') as sample_source:
            sample_source.write(file_contents)

    def copy_generator_specific_files(self):
        # The unity generator uses the custom editor file for grabbing the unity version
#        os.mkdir(os.path.join(self.project_root, 'unity', 'Assets'))
#        os.mkdir(os.path.join(self.project_root, 'unity', 'Assets', 'Editor'))
#
#        with open(os.path.join(os.getcwd(), 'templates', 'languages', 'unity', 'GetUnityVersion.cs'), 'r') as input_f:
#            input_data = input_f.readlines()
#        with open(os.path.join(self.project_root, 'unity', 'Assets', 'Editor', 'GetUnityVersion.cs'), 'w') as output_f:
#            output_f.writelines(input_data)
        pass # This is no longer needed as the new cmake module simply checks the registry

###########################################################