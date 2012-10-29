"""ModuleSystem is a module which manages the modules system (see
modules.sourceforge.net for more information about the module system).

Currently this module is capable of:
    * List all available modules in a system
    * List already loaded modules

Future approaches:
    * List different versions of a module

Author: Guillermo Carrasco Hernandez
Contact: guillermo.carrasco.hernandez@gmail.com
"""
import os
import subprocess

class moduleManager(object):
    """Class to list and manage the different modules in a system
       (modules.sourceforge.net)
    """
    def __new__(typ, *args, **kwargs):
        """Check if the module system is installed before cerating an instance
           of the class.
        """
        try:
            os.environ['MODULESHOME']
            return object.__new__(typ, *args, **kwargs)
        except KeyError:
            raise RuntimeError('No module system found!')
            return None


    def __init__(self):
        self.env = dict(os.environ)
        try:
            self.modules_version = self.env['MODULES_REL']
        except KeyError:
            self.modules_version = 'Undefined'
        module_list = 'module ' + str(self.env['modules_shell']) + ' avait -t'
        self.moduleList = subprocess.check_output(module_list, \
                                                  stderr=subprocess.STDOUT)

