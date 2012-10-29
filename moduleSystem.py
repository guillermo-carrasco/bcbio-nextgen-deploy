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
import sets

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
        module_list = 'module bash avait -t'
        print "Obtaining information of the modules in the system..."
        output = subprocess.check_output(module_list, shell = True, \
                                         stderr=subprocess.STDOUT)
        #Prepare the list of modules
        output = output.split()
        moduleList = dict()
        for module in output:
            if module[-1] != ':':
                try:
                    (software, version) = module.split('/')
                except ValueError:
                    (software, version) = module, None
                if moduleList.has_key(software):
                    moduleList[software].add(version)
                else:
                    moduleList[software] = set([version])
        self.moduleList = moduleList
        print "Module manager initialized correctly!"

