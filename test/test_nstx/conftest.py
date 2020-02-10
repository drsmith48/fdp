"""
pytest fixtures.
"""

import pytest
import fdp

from . import shotlist


@pytest.fixture(scope="module")
def setup_nstx():
    nstx = fdp.Nstxu()
    nstx.addshot(shotlist=shotlist)
    return nstx


@pytest.fixture(scope="module")
def setup_shot(setup_nstx):
    nstx = setup_nstx
    return nstx.s142301
