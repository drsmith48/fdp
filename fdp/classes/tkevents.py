# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:17:41 2016

@author: drsmith
"""

from future import standard_library
standard_library.install_aliases()
import sys
if sys.version_info[0] < 3:
    import tkinter as tk
else:
    import tkinter as tk


class AddShotEvent(tk.Event):
    pass
