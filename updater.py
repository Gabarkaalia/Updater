from subprocess import call
import os, sys
from os import path
from Tkinter import *
from threading import *
import tkFileDialog
import logging
from logging import handlers

## This file implements the project downloadeer.
## It is used for pulling and building all of my software
##
## @author Daniel J. Finnegan
## @date July 2017

####################################################################

version_number = 1.0 # Updater version number
author_name = 'Daniel J. Finnegan'

class ProjectGenerator():

    def __init__(self, proj_root):
        self.initialize(proj_root)

    def initialize(self, proj_root):
        self.project_root = proj_root

    def write_cmake_file(self):
        file_contents = (
            '# Automatically generated by Updater v' + str(version_number) + '\n'
            '# @author ' + author_name + '\n'
            '\n'
            'cmake_minimum_required (VERSION 2.8)\n'
            'cmake_policy (SET CMP0048 NEW)\n'
            '\n'
            'project (\n'
            '\t\"Test\"\n'
            '\tVERSION\n'
            '\t\t1.0\n'
            ')\n'
            '\n'
            'set (\n'
            '\tSOURCE_FILES\n'
            '\t\t\"src/main.cpp\"\n'
            ')\n'
            '\n'
            'add_executable (\n'
            '\tmain\n'
            '\t${SOURCE_FILES}\n'
            ')'
        )

        with open(os.path.join(self.project_root, 'CMakeLists.txt'), 'w') as cmake_lists:
            cmake_lists.write(file_contents)

    def write_readme_file(self):
        file_contents = (
            '# ' + os.path.basename(self.project_root) +'\n'
            'Put your README information here'
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
            '\n####################################################################'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', 'build_project.py'), 'w') as build_module:
            build_module.write(file_contents)

    def write_sample_source_file(self):
        file_contents = (
            '/**\n'
            '\tAutomatically generated by Updater v' + str(version_number) + '\n'
            '\t@author ' + author_name + '\n'
            '*/\n'
            '\n'
            '#include <iostream>\n'
            '\n'
            'int main(int argc, char **argv)\n'
            '{\n'
            '\tstd::cout << \"Hello World\\n\" << std::endl;\n'
            '\treturn 0;\n'
            '}\n'
        )

        with open(os.path.join(self.project_root, 'src', 'main.cpp'), 'w') as sample_source:
            sample_source.write(file_contents)

    def write_init_file(self):
        file_contents = (
            '# __init__ file for module\n'
            '# @author ' + author_name + '\n'
            '\n'
            '__all__ = [\'build_project\']'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', '__init__.py'), 'w') as init_module:
            init_module.write(file_contents)

    def generate_project(self):
        if os.path.isdir(self.project_root):
            self.logger.info('Project already exists! Aborting...')
            return 1
        else:
            os.mkdir(self.project_root)
            os.mkdir(os.path.join(self.project_root, 'src'))
            os.mkdir(os.path.join(self.project_root, 'scripts'))
            os.mkdir(os.path.join(self.project_root, 'scripts', 'builder'))

            self.write_init_file()
            self.write_readme_file()
            self.write_build_file()
            self.write_cmake_file()
            self.write_sample_source_file()
            return 0

###########################################################

class App(Tk):

    def __init__(self, master):
    	self.frame = Frame(master, height=640, width=480)
    	self.initialize()

    def initialize(self):
    	self.frame.grid()
    	self.init_vars()
    	self.init_controls()
    	self.init_gui()

    def init_vars(self):
        self.project_table = {
            'Spatiotemporal-Study': 'https://github.bath.ac.uk/djf32/spatiotemporal_study.git',
            'Updater': 'https://github.bath.ac.uk/djf32/Updater.git',
            'Test': 'https://github.bath.ac.uk/djf32/Test.git'
        }
        self.project_titles = sorted(self.project_table.keys()) # Get a sorted list of the keys

        self.branches = ['master', 'testing']
        self.project_root = 'C:\\'

        # Set the logger      
        if sys.platform == 'darwin':
            self.logger = logging.getLogger()
            syslogH = handlers.SysLogHandler(address='/var/run/syslog', facility='local1')
            syslogH.ident = 'updater_application:'
            self.logger.addHandler(syslogH)
        else: # Handle the Windows case
            self.logger = logging.getLogger('updater_application')

        self.logger.setLevel(logging.INFO)

    def init_controls(self):
    	self.project_root_text = StringVar()
    	self.project_root_text.set(self.project_root)

    	self.project_titles_var = StringVar()
    	self.project_titles_var.set(self.project_titles[0])

        self.branches_var = StringVar()
        self.branches_var.set(self.branches[0])

    def init_gui(self):
    	# Option box for selecting the project to install
    	self.project_label = Label(self.frame, text='Branch to Install or Update:')
    	self.projects_options = OptionMenu(self.frame, self.project_titles_var, *self.project_titles)
    	self.project_label.grid(column=0, row=0, sticky='W')
    	self.projects_options.grid(column=1, columnspan=3, row = 0, sticky='W')

        # Option box for selecting the project to install
        self.project_label = Label(self.frame, text='Project to Install or Update:')
        self.projects_options = OptionMenu(self.frame, self.branches_var, *self.branches)
        self.project_label.grid(column=0, row=1, sticky='W')
        self.projects_options.grid(column=1, columnspan=3, row = 1, sticky='W')

    	# Entry for specifying the directory to install the project
    	# Complete with side label and action button
    	self.directory_label = Label(self.frame, text='Project Directory to Install or Update:')
    	self.directory_entry = Entry(self.frame, textvariable=self.project_root_text, width=50)
    	self.set_directory_button = Button(self.frame, text="Set Directory", command=self.find_dir)
    	self.directory_label.grid(column=0, row=2, sticky='EW')
    	self.directory_entry.grid(column=1, columnspan=2, row=2, sticky='EW')
    	self.set_directory_button.grid(column=3, row=2, sticky='EW')

    	# Action button for updating
    	self.update_button = Button(self.frame, text='Update', command=self.do_task)
        self.create_button = Button(self.frame, text='Create', command=self.create_project)
    	self.update_button.grid(column=0, row=3, sticky='EW')
        self.create_button.grid(column=1, row=3, sticky='EW')

        # Text box for log output
        self.log = Text(self.frame, height=20, takefocus=0)
        self.log.grid(column=0, columnspan=4, row=4, sticky='EW')

    def find_dir(self):
    	self.project_root = tkFileDialog.askdirectory()
    	if self.project_root is None:
            return

    	self.project_root_text.set(self.project_root)

    def build_project(self):
        self.log_message('Building the software package...')
        os.chdir(self.project_root) # Move to the root of the directory

        self.log_message('Building the project...')
        sys.path.append(os.getcwd() + '/scripts/')

        # Import the build script as a python module and then build it
        # If no custom build operation is specified, then make a standard call to cmake
        from builder import build_project
        if build_project.UPDATER_BUILD_CUSTOM:
            build_project.build_full_package(self.project_root) # Pass in the root directory 
        else:
            if os.path.isdir(os.path.join(self.project_root, 'bin')):
                shutil.rmtree(os.path.join(self.project_root, 'bin'))

            os.mkdir(os.path.join(self.project_root, 'bin'))
            os.chdir(os.path.join(self.project_root, 'bin'))
            rc = call(['cmake'] + build_project.UPDATER_CMAKE_ARGS + ['..'])
            if rc != 0:
                self.log_message(message='Project is missing a CMakeLists.txt file. Contact the package maintainer')
            else:
                call(['cmake', '--build', '.'])

        self.log_message('Project built!')

    def update_project(self):
        self.log_message(message='Updating the software package...')
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the master branch
        call(['git', '-C', self.project_root, 'pull', 'origin', self.branches_var.get()]) # Pull the changes made in the project from the repo
        self.log_message('Software updated!')

    def download_project(self):
        self.log_message(message='Downloading the software...')
        project_url = self.project_table[self.project_titles_var.get()]
        call(['git', '-C', self.project_root, 'clone', project_url, self.project_titles_var.get()]) # Clone the project from the remote repo
        
        self.project_root = os.path.join(self.project_root, self.project_titles_var.get()) # Update the directory name to reflect the downloaded package
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the branch
        self.log_message('Software downloaded!')

    def do_task(self):

        # Add paths
        if sys.platform == 'darwin':
            # sys.path.append('/usr/local/bin')
            os.environ['PATH'] += ':' + '/usr/local/bin' # Patch for homebrew installations
        elif sys.platform == 'win32':
            self.log_message(message='Windows is buggy. Please report any issues')
        else:
            self.log_message(message='Platform unsupported. Aborting')
            return

    	rc = call(['git', '-C', self.project_root, 'status']) # Run git status
    	if rc == 0:
            def update_in_thread():
                self.update_button.config(state=DISABLED)
                self.create_button.config(state=DISABLED)

                self.update_project()
                self.build_project() # Pass in the project root folder

                self.update_button.config(state=ACTIVE)
                self.create_button.config(state=ACTIVE)
                return

            thread = Thread(target=update_in_thread)
            thread.start()
            return thread
    	else:
            def download_in_thread():
                self.update_button.config(state=DISABLED)
                self.create_button.config(state=DISABLED)

                self.download_project()
                self.build_project()

                self.update_button.config(state=ACTIVE)
                self.create_button.config(state=ACTIVE)
                return

            thread = Thread(target=download_in_thread)
            thread.start()
            return thread

    def create_project(self):
        def create_in_thread():
            self.update_button.config(state=DISABLED)
            self.create_button.config(state=DISABLED)

            project_generator = ProjectGenerator(self.project_root_text.get())
            self.log_message(message='Generating the project...')
            rc = project_generator.generate_project()
            if rc == 0:
                self.log_message('Project generated!')
            else:
                self.log_message('Project not generated. Check log for issues')

            self.update_button.config(state=ACTIVE)
            self.create_button.config(state=ACTIVE)

        thread = Thread(target=create_in_thread)
        thread.start()
        return thread


    def log_message(self, message=''):
        self.logger.info(message) # Log to the logger too
    	self.log.insert(INSERT, message)
        self.log.insert(INSERT, '\n')
    	self.log.see(END)

if __name__ == '__main__':
	root = Tk()
	root.title('Experiment Updater (Testing branch)')
	app = App(root)
	root.mainloop()
	# root.destroy()