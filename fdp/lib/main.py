#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:50:13 2018

@author: drsmith
"""

from .machine import Machine
from .parse import parse_method
from .datasources import machineAlias

def machineFactory(name=''):
    machine_name = machineAlias(name)
    class_name = 'Machine' + machine_name.capitalize()
    cls = type(class_name, (Machine, ), {})
    cls._name = machine_name
    parse_method(cls, level='top')
    parse_method(cls, level=cls._name)
    return cls


Nstxu = machineFactory('nstxu')
