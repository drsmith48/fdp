# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 19:35:36 2015

@author: ktritz
"""
from __future__ import print_function
#from builtins import object

from .machine import Machine
from .parse import parse_method
#from .globals import VERBOSE, FdpError
#from .datasources import machineAlias, MACHINES


#class Fdp(object):
#    """
#    The primary data object in FDP and the top-level container for machines.
#    """
#
#    def __init__(self, *args, **kwargs):
#        self.args = args
#        self.kwargs = kwargs
#
#    def __getattr__(self, attribute):
#        if VERBOSE:
#            print('{}.__getattr__({})'.
#                  format(self.__class__, attribute))
#        machine_name = machineAlias(attribute)
#        if machine_name not in MACHINES:
#            raise FdpError('Invalid machine name')
#        # subclass machine.Machine() for <machine_name>
#        MachineClassName = 'Machine' + machine_name.capitalize()
#        MachineClass = type(MachineClassName, (Machine, ), {})
#        MachineClass._name = machine_name
#        # parse fdp/methods and fdp/methods/<machine_name>
#        parse_method(MachineClass, level='top')
#        parse_method(MachineClass, level=machine_name)
#        return MachineClass(machine_name, *self.args, **self.kwargs)
#
#    def __dir__(self):
#        return MACHINES


Nstxu = type('MachineNstx', (Machine, ), {})
Nstxu._name = 'nstxu'
parse_method(Nstxu, level='top')
parse_method(Nstxu, level=Nstxu._name)

#class Nstx(Machine):
#
#    def __init__(self, name='nstx', *args, **kwargs):
#        super(Nstx, self).__init__(name=name, *args, **kwargs)
#        parse_method(self, level='top')
#        parse_method(self, level=name)
