# -*- coding: utf-8 -*-
"""
``fdp.methods`` contains methods for FDP objects (e.g. a plot method, ``>>> mpts.te.plot()``).  Methods can be specified at different levels: global, machine-specific, or diagnostic-specific.
"""

from .plot import plot
from ._netcat import _netcat
from .listmethods import listSignals, listMethods, listContainers, listAttributes
from .info import info, isSignal, isContainer, isAxis
from .fft import fft, plotfft
from .timeindex import getTimeIndex

__all__ = ['plot', '_netcat',
           'listSignals', 'listMethods', 'listContainers', 'listAttributes',
           'info', 'isSignal', 'isContainer', 'isAxis',
           'fft', 'plotfft',
           'getTimeIndex']
