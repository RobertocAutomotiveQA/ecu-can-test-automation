# conftest.py
# Provides fixtures: ECUSimulator thread, DBC loader and CAN bus.

import sys
import os
import pytest

# Add project root and src directory to sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for path in (ROOT, os.path.join(ROOT, 'src')):
    if path not in sys.path:
        sys.path.insert(0, path)

from ecu_simulator import ECUSimulator
from libs.dbc_loader import load_dbc
from libs.can_utils import init_bus

@pytest.fixture(scope="module", autouse=True)
def ecu_simulator():
    """Start ECUSimulator thread before tests and stop it after module."""
    sim = ECUSimulator()
    sim.start()
    yield
    sim.stop()

@pytest.fixture(scope="module")
def db():
    """Load the DBC database once per module."""
    return load_dbc('config/vehicle.dbc')

@pytest.fixture(scope="module")
def bus():
    """Initialize and yield a virtual CAN bus, then shut it down."""
    bus = init_bus()
    yield bus
    bus.shutdown()