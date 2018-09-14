#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:28:09 2018

@author: drsmith
"""

import fdp
nstx = fdp.Nstxu()
s = nstx[141711]
ip = s.engineering.ip
ip[:]
print(ip.size, ip.max())