# dbc_loader.py
# Loads a DBC file and returns a cantools database.

import cantools

def load_dbc(path='config/vehicle.dbc'):
    """
    Load and return a cantools database from the given .dbc file.
    """
    return cantools.database.load_file(path)