"""This module contains a **constants** and **default** parameters.

    These parameters can be accessed at any time by whatever of the
    modules.

    Example:
        To use the ``Constants`` import the module as::

            >>> import symupy.utils.constants as ct
            >>> ct.BUFFER_STRING # access the buffer size


    ============================  =================================
     **Variable**                 **Description**
    ----------------------------  ---------------------------------
    ``BUFFER_STRING``              Buffer size
    ``DEFAULT_LIB_OSX``            Default OS X library path
    ``DEFAULT_LIB_LINUX``          Default Linux library path
    ``FIELD_DATA``                 Vehicle trajectory data
    ``FIELD_FORMAT``               Trajectory data types
    ``HOUR_FORMAT``                Time format
    ``FIELD_FORMATAGG``            Format aggretations
    ``DCT_SIMULATION_INFO```       XML Simulation information
    ``DCT_EXPORT_INFO``            XML Export information
    ``DCT_TRAFIC_INFO``            XML Traffic information
    ``DCT_NETWORK_INFO``           XML Network information
    ``DCT_SCENARIO_INFO``          XML Scenario information
    ``TP_VEHTYPES``                Vehicle type information
    ``TP_ACCEL``                   Vehicle acceleration boundaries
    ============================  =================================

"""

# =============================================================================
# STANDARD  IMPORTS
# =============================================================================
import os
from datetime import date, datetime, timedelta
import platform

from decouple import UndefinedValueError, config
from numpy import array, float64, int32
from pathlib import Path
from collections import defaultdict

# =============================================================================
# INTERNAL IMPORTS
# =============================================================================

from symupy.utils.exceptions import SymupyError, SymupyWarning
from symupy import __version__

# =============================================================================
# CLASS AND DEFINITIONS
# =============================================================================

# Default simulator per platform

# =============================================================================
# DEFAULT PATHS TO FIND SIMULATOR PLATFORMS
# =============================================================================

# Point to ini file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Conda RTD
RTDPATH = os.getenv("RTD_ENV", config("RTD_ENV", cast=str))

# Solving conda (local,RTD)
CONDA_PREFIX = os.getenv("CONDA_PREFIX", RTDPATH)

# Default names/platform
DCT_LIBOSNAME = {
    "Darwin": "libSymuVia.dylib",
    "Linux": "libSymuVia.so",
    "Windows": "libSymuVia.dll",
}


def find_path(roots):
    for root in roots:
        if (p := Path(root)).is_dir():
            yield from p.glob(f"**/{DCT_LIBOSNAME[platform.system()]}")


# Add all root paths to search for the library here
PATHS_2_SEARCH = (CONDA_PREFIX, RTDPATH)

for path in find_path(PATHS_2_SEARCH):
    DEFAULT_PATH_SYMUVIA = path

print(f"Default path: {DEFAULT_PATH_SYMUVIA}")

if not DEFAULT_PATH_SYMUVIA:
    DEFAULT_PATH_SYMUVIA = ""
    raise SymupyWarning("No Simulator could be defined")

# =============================================================================
# DEFAULT SIMULATOR/ OS ASSOCIATION
# =============================================================================

# =============================================================================
# DATA SYMUVIA
# =============================================================================

# =============================================================================
# STREAM CONSTANTS
# =============================================================================

BUFFER_STRING = 1000000
WRITE_XML = False
TRACE_FLOW = False
LAUNCH_MODE = "lite"
TOTAL_SIMULATION_STEPS = 0

FIELD_DATA = {
    "@abs": "abscissa",
    "@acc": "acceleration",
    "@dst": "distance",
    "@id": "vehid",
    "@ord": "ordinate",
    "@tron": "link",
    "@type": "vehtype",
    "@vit": "speed",
    "@voie": "lane",
    "@z": "elevation",
    "@etat_pilotage": "driven",
}

FIELD_FORMAT = {
    "@abs": float,
    "@acc": float,
    "@dst": float,
    "@id": int,
    "@ord": float,
    "@tron": str,
    "@type": str,
    "@vit": float,
    "@voie": int,
    "@z": float,
    "@etat_pilotage": bool,
}

FLOATFORMAT = float64
INTFORMAT = int32

FIELD_FORMATAGG = {
    "abscisa": (array, FLOATFORMAT),
    "acceleration": (array, FLOATFORMAT),
    "distance": (array, FLOATFORMAT),
    "vehid": (array, INTFORMAT),
    "ordinate": (array, FLOATFORMAT),
    "link": (list, None),
    "vehtype": (list, None),
    "speed": (array, FLOATFORMAT),
    "lane": (array, INTFORMAT),
    "elevation": (array, FLOATFORMAT),
}

# =============================================================================
# XML Data
# =============================================================================

# DATE/TIME INFORMATION
HOUR_FORMAT = "%H:%M:%S"
DELTA_TIME = timedelta(minutes=1)
TIME_STEP = timedelta(seconds=1).total_seconds()
TODAY = date.today().strftime("%Y-%m-%d")
ST_TIME = datetime.now()
ED_TIME = ST_TIME + DELTA_TIME
ST_TIME_STR = ST_TIME.strftime("%H:%M:%S")
ED_TIME_STR = ED_TIME.strftime("%H:%M:%S")

# SIMULATION INFORMATION
DCT_SIMULATION_INFO = {
    "id": "simID",
    "pasdetemps": f"{TIME_STEP}",
    "debut": f"ST_TIME_STR",
    "fin": f"ED_TIME_STR",
    "loipoursuite": "exacte",
    "comportementflux": "iti",
    "date": f"today",
    "titre": "default_simulation",
    "proc_deceleration": "false",
    "seed": "1",
}

# DATA EXPORT INFORMATION
DCT_EXPORT_INFO = {
    "trace_route": "false",
    "trajectoires": "true",
    "debug": "false",
    "debug_matrice_OD": "false",
    "debug_SAS": "false",
    "csv": "true",
}

# TAFFIC INFORMATION
DCT_TRAFIC_INFO = {
    "id": "trafID",
    "accbornee": "true",
    "coeffrelax": "4",
    "chgtvoie_ghost": "false",
}

# NETWORK INFORMATION
DCT_NETWORK_INFO = {"id": "resID"}

# SCENARIO INFORMATION
DCT_SCENARIO_INFO = {
    "id": "defaultScenario",
    "simulation_id": DCT_SIMULATION_INFO.get("id"),
    "trafic_id": DCT_TRAFIC_INFO.get("id"),
    "reseau_id": DCT_NETWORK_INFO.get("id"),
    "dirout": "data",
    "prefout": "simout_ring_data",
}


TP_VEHTYPES = (
    {"id": "HDV", "w": "-5", "kx": "0.12", "vx": "25"},
    {"id": "CAV", "w": "-5", "kx": "0.12", "vx": "25"},
)

TP_ACCEL = (
    {"ax": "1.5", "vit_sup": "5.8"},
    {"ax": "1", "vit_sup": "8"},
    {"ax": "0.5", "vit_sup": "infini"},
)

# =============================================================================
# CONTROL
# =============================================================================

BUFFER_CONTROL = 10  # Amount of control samples stored in memory

# =============================================================================
# VEHICLE DYNAMICS
# =============================================================================

ENGINE_CONSTANT = 0.2

# =============================================================================
# COMMUNICATION
# =============================================================================

RADIOUS_ANT = 500

if __name__ == "__main__":
    print(DEFAULT_LIB_WINDOWS, DEFAULT_LIB_OSX, DEFAULT_LIB_LINUX)
