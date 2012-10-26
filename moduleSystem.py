import os
import subprocess

class moduleManager:
    """Class to list and manage the different modules in a session
       (modules.sourceforge.net)
    """
    def __new__(self):
        """Check if the module system is installed before cerating an instance
           of the class
        """
        try:
            os.environ['modules_shell']
        except KeyError:
            raise RuntimeError('No module system found!')

    def __init__(self):
        self.env = dict(os.environ)
        print self.env
        module_list = 'module ' + str(self.env['modules_shell']) + ' avait -t'
        self.moduleList = subprocess.check_output(module_list, \
                                                  stderr=subprocess.STDOUT)
