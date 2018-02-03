# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 08:43:55 2016

@author: drsmith
"""

from ....lib.utilities import isContainer


def preprocess(self):
    if isContainer(self) and self._name == 'magnetics':
        if self.shot < 200000:
            self.highn._mdstree = 'ops_pc'
            for signal in self.highn:
                signal._mdstree = 'ops_pc'
                signal.time._mdstree = 'ops_pc'
                signal.__init__()
