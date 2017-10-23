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
from generators import base_gen

class UnityGenerator(base_gen.ProjectGenerator):

    def __init__(self, proj_root):
        super(UnityGenerator, self).__init__(proj_root)
        self.template_name = 'unity.txt'
        self.template_keys['projname'] =  'Unity-Updater-Project'
        self.template_keys['appname'] =  'Unity-Application'
        self.template_keys['proj_languages'] = 'NONE'

    def write_sample_source_file(self):
        if not os.path.isdir(os.path.join(self.project_root, 'unity')):
            os.mkdir(os.path.join(self.project_root, 'unity'))

        file_contents = (
            'Automatically generated by Updater v' + str(self.template_keys['version_number']) + '\n'
            '@author ' + self.template_keys['author_name'] + '\n\n'
            '# Generate your Unity Project here\n'
        )

        with open(os.path.join(self.project_root, 'unity', 'README.txt'), 'w') as sample_source:
            sample_source.write(file_contents)

###########################################################