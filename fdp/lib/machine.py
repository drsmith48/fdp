# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 12:05:14 2015

@author: ktritz
"""
from __future__ import print_function
from builtins import str, map, range
from collections import Sized, Iterable, Container, deque
import os
from warnings import warn
import numpy as np
import MDSplus as mds

from . import logbook
from . import parse
from .shot import Shot
from .globals import FDP_DIR, FdpError, FdpWarning
from .datasources import machineAlias, MDS_SERVERS, EVENT_SERVERS



def machineFactory(name=''):
    machine_name = machineAlias(name)
    class_name = 'Machine' + machine_name.capitalize()
    cls = type(class_name, (Machine, ), {})
    cls._name = machine_name
    parse.parse_method(cls, level='top')
    parse.parse_method(cls, level=cls._name)
    return cls


class Machine(Sized, Iterable, Container):
    """
    Factory root class that contains shot objects and MDS access methods.

    **Usage**::

        >>> import fdf
        >>> nstxu = fdf.nstxu()
        >>> nstxu.s140000.logbook()
        >>> nstxu.s140000.mpts.plot()

    """

    # Maintain a dictionary of cached MDS server connections to speed up
    # access for multiple shots and trees. This is a static class variable
    # to avoid proliferation of MDS server connections
    _connections = []
    _parent = None
    _modules = None
    _name = ''

    def __init__(self, shotlist=None, xp=None, date=None):
        self._shots = {}  # shot dictionary with shot number (int) keys
        self._classlist = {}
        self._logbook = logbook.Logbook(name=self._name, root=self)
        event_server = EVENT_SERVERS[self._name]
        self._eventConnection = mds.Connection('{}:{}'.format(event_server['hostname'],
                                                              event_server['port']))
        if len(self._connections) is 0:
            mds_server = MDS_SERVERS[self._name]
            for _ in range(2):
                connection = mds.Connection('{}:{}'.format(mds_server['hostname'],
                                                           mds_server['port']))
                connection.tree = None
                self._connections.append(connection)
        self.s0 = Shot(0, root=self, parent=self)
        if shotlist or xp or date:
            self._addshot(shotlist=shotlist, xp=xp, date=date)

    def __getattr__(self, name):
        try:
            shot = int(name.split('s')[1])
            return self[shot]
        except:
            raise AttributeError('bad attr: {}'.format(name))
    
    def __repr__(self):
        return '<machine {}>'.format(self._name.upper())

    def __iter__(self):
        # iterate over Shot objects in _shots.values()
        # (not over shot numbers in _shots.keys())
        return iter(self._shots.values())

    def __contains__(self, key):
        return key in self._shots

    def __len__(self):
        return len(self._shots)

    def __delitem__(self, key):
        del self._shots[key]

    def __getitem__(self, shot):
        if not isinstance(shot, int):
            raise TypeError('expect integer shot number: {} type: {}'.format(shot, type(shot)))
        if shot == 0:
            return self.s0
        if shot not in self:
            self._shots[shot] = Shot(shot, root=self, parent=self)
        return self._shots[shot]

    def __setitem__(self, item, value):
        pass

    def __dir__(self):
        return ['s{}'.format(shot) for shot in self._shots.keys()]

    def _get_logbook_credentials(self):
        # override with methods/<machine>/_get_logbook_credentials.py
        pass

    def _get_connection(self, shot, tree):
        for connection in self._connections:
            if connection.tree == (tree, shot):
                self._connections.remove(connection)
                self._connections.insert(0, connection)
                return connection
        connection = self._connections.pop()
        try:
            connection.closeAllTrees()
        except:
            pass
        try:
            connection.openTree(tree, shot)
            connection.tree = (tree, shot)
        except:
            connection.tree = (None, None)
        finally:
            self._connections.insert(0, connection)
        return connection

    def _get_mdsshape(self, signal):
        if signal.shot is 0:
            print('No MDS data exists for model tree')
            return tuple()
        try:
            connection = self._get_connection(signal.shot, signal._mdstree)
            usage_code = connection.get('getnci({},"USAGE")'.format(signal._mdsnode)).data()
            length = connection.get('getnci({},"LENGTH")'.format(signal._mdsnode)).data()
            if usage_code != 6 or length < 1:
                raise ValueError
            data = connection.get('shape({})'.format(signal._mdsnode)).data()
            return tuple(data)
        except:
            msg = 'MDSplus connection error for shot {}, tree {}, and node {}'.format(
                signal.shot, signal._mdstree, signal._mdsnode)
            warn(msg, FdpWarning)
            return tuple()

    def _get_mdsdata(self, signal):
        shot = signal.shot
        if shot is 0:
            print('No MDS data exists for model tree')
            return np.zeros(0)
        connection = self._get_connection(shot, signal._mdstree)
        try:
            data = connection.get(signal._mdsnode)
        except:
            msg = 'MDSplus connection error for shot {}, tree {}, and node {}'.format(
                signal.shot, signal._mdstree, signal._mdsnode)
            warn(msg, FdpWarning)
            return np.zeros(0)
        if getattr(signal, '_raw_of', None) is not None:
            data = data.raw_of()
        if getattr(signal, '_dim_of', None) is not None:
            data = data.dim_of()
        data = data.value_of().value
        if signal._transpose is not None:
            data = data.transpose(signal._transpose)
        if hasattr(signal, '_postprocess'):
            data = signal._postprocess(data)
        return data

    def _get_modules(self):
        if self._modules is None:
            module_dir = os.path.join(FDP_DIR, 'diagnostics', self._name)
            self._modules = [module for module in os.listdir(module_dir)
                             if os.path.isdir(os.path.join(module_dir, module)) and
                             module[0] is not '_']
        return self._modules

    def _addshot(self, shotlist=None, date=None, xp=None):
        """
        Load shots into the Machine class

        **Usage**

            >>> nstxu._addshot([140000 140001])
            >>> nstxu._addshot(xp=1032)

        Note: You can reference shots even if the shots have not been loaded.

        """
        shots = []
        if shotlist:
            if not isinstance(shotlist, (list, tuple)):
                shotlist = [shotlist]
            shots.extend(list(shotlist))
        if date:
            if not isinstance(date, (list, tuple)):
                date = [date]
            shots.extend(self._logbook.get_shotlist(date=list(date)))
        if xp:
            if not isinstance(xp, (list, tuple)):
                xp = [xp]
            shots.extend(self._logbook.get_shotlist(xp=list(xp)))
        for shot in np.unique(shots):
            if shot not in self._shots:
                self._shots[shot] = Shot(shot, root=self, parent=self)

    def _addxp(self, xp=None):
        self._addshot(xp=xp)

    def _adddate(self, date=None):
        self._addshot(date=date)

    def _shotlist(self):
        keys = self._shots.keys()
        keys.sort()
        for shotkey in keys:
            shot = self._shots[shotkey]
            print('{} in XP {} on {}'.format(shot.shot, shot.xp, shot.date))
        return keys

    def _setevent(self, event, shot_number=None, data=None):
        event_data = bytearray()
        if shot_number is not None:
            shot_data = shot_number // 256**np.arange(4) % 256
            event_data.extend(shot_data.astype(np.ubyte))
        if data is not None:
            event_data.extend(str(data))
        mdsdata = mds.mdsdata.makeData(np.array(event_data))
        event_string = 'setevent("{}", {})'.format(event, mdsdata)
        status = self._eventConnection.get(event_string)
        return status

    def _wfevent(self, event, timeout=0):
        event_string = 'kind(_data=wfevent("{}",*,{})) == 0BU ? "timeout"' \
                       ': _data'.format(event, timeout)
        data = self._eventConnection.get(event_string).value
        if type(data) is str:
            raise FdpError('Timeout after {}s in wfevent'.format(timeout))
        if not data.size:
            return None
        if data.size > 3:
            shot_data = data[0:4]
            shot_number = np.sum(shot_data * 256**np.arange(4))
            data = data[4:]
            return shot_number, ''.join(map(chr, data))
        return data

    def _find(self, tag, obj=None):
        root = getattr(self, '_root', self)
        find_list = set([])
        for module in root.s0._modules:
            module_obj = getattr(root.s0, module)
            container_queue = deque([module_obj])
            while True:
                try:
                    container = container_queue.popleft()
                    container._get_dynamic_containers()
                    container_queue.extend(list(container._containers.values()))
                    if obj is None or obj.lower() == 'signal':
                        for signal in list(container._signals.values()):
                            if signal._contains(tag):
                                branch_str = '.'.join([signal._get_branch(),
                                                       signal._name])
                                find_list.add(branch_str)
                    if obj is None or obj.lower() == 'axis':
                        for signal in list(container._signals.values()):
                            for axis_str in signal.axes:
                                axis = getattr(signal, axis_str)
                                if axis._contains(tag):
                                    branch_str = '.'.join([signal._get_branch(),
                                                           signal._name, axis._name])
                                    find_list.add(branch_str)
                    if obj is None or obj.lower() == 'container':
                        if container._contains(tag):
                            find_list.add(container._get_branch())
                except IndexError:
                    break
        find_list = list(find_list)
        find_list.sort()
        return find_list

    def _filter_shots(self, date=None, xp=None):
        """
        Get a Machine-like object with an immutable shotlist for XP(s)
        or date(s)
        """
        self._addshot(xp=xp, date=date)
        return ImmutableMachine(xp=xp, date=date, parent=self)


class ImmutableMachine(Sized, Iterable, Container):
    """
    An immutable Machine-like class for dates and XPs.

    The shotlist is auto-loaded based on date or XP, and the shotlist
    can not be modified.

    Machine.filter_shots() returns an ImmutableMachine object.

    **Usage**::

        >>> xp1013 = fdp.nstxu.filter_shots(xp=1013)
        >>> for shot in xp1013:
        ...     shot.mpts.te.plot()
        ...

    """

    def __init__(self, xp=None, date=None, parent=None):
        self._shots = {}
        self._parent = parent
        self._name = self._parent._name
        shotlist = self._parent.get_shotlist(xp=xp, date=date)
        for shot in shotlist:
            self._shots[shot] = getattr(self._parent, 's{}'.format(shot))

    def __getattr__(self, name):
        try:
            shot = int(name.split('s')[1])
            return self._shots[shot]
        except:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                type(self), name))

    def __repr__(self):
        return '<immutable machine {}>'.format(self._name.upper())

    def __iter__(self):
        return iter(list(self._shots.values()))

    def __contains__(self, value):
        return value in self._shots

    def __len__(self):
        return len(list(self._shots.keys()))

    def __delitem__(self, item):
        pass

    def __getitem__(self, item):
        pass

    def __dir__(self):
        return ['s{}'.format(shot) for shot in self._shots]

    def _logbook(self):
        for shotnum in self._shots:
            shot = self._shots[shotnum]
            shot.logbook()

    def _listshots(self):
        for shotnum in self._shots:
            shot = self._shots[shotnum]
            print('{} in XP {} on {}'.format(shot.shot, shot.xp, shot.date))
