# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:11:07 2016

@author: drsmith
"""
from __future__ import print_function

import fdp

nstx = fdp.nstx()

shotlist = [204620, 204551, 141000, 204670, 204956, 204990, 333333]

nstx.addshot(shotlist)
for shot in nstx:
    print('*** {} logbook ***'.format(shot))
    shot.logbook()
    break