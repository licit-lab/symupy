"""
    This module contains a **constants** and **default** parameters. These parameters can be accessed 
    at any time by whatever of the modules. 

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

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from datetime import date, datetime, timedelta
from decouple import config, UndefinedValueError
import platform
import os
from numpy import array, float64, int32

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .exceptions import SymupyError


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

# Default simulator per platform

# *****************************************************************************
# DEFAULT PATHS TO FIND SIMULATOR PLATFORMS
# *****************************************************************************
DEFAULT_LIB_LINUX = DEFAULT_LIB_OSX = DEFAULT_LIB_WINDOWS = ""

if platform.system() == "Darwin":
    try:
        DEFAULT_LIB_OSX = config("DEFAULT_LIB_OSX")
    except UndefinedValueError:
        DEFAULT_LIB_OSX = "/Users/andresladino/Documents/01-Code/04-Platforms/dev-symuvia/build/lib/libSymuVia.dylib"
elif platform.system() == "Linux":
    try:
        DEFAULT_LIB_LINUX = config("DEFAULT_LIB_LINUX")
    except UndefinedValueError:
        DEFAULT_LIB_LINUX = "/home/build-symuvia/build/symuvia/libSymuVia.so"
elif platform.system() == "Windows":
    try:
        DEFAULT_LIB_WINDOWS = config("DEFAULT_LIB_WINDOWS")
    except UndefinedValueError:
        DEFAULT_LIB_WINDOWS = ""
else:
    raise SymupyError("Platform could not be determined")

# *****************************************************************************
# DEFAULT SIMULATOR/ OS ASSOCIATION
# *****************************************************************************

DCT_SIMULATORS = {"Darwin": "symuvia", "Linux": "symuvia", "Windows": "symuvia"}

# Feasible Simulator/Platform Paths/Libs

DCT_DEFAULT_PATHS = {
    ("symuvia", "Darwin"): DEFAULT_LIB_OSX,
    ("symuvia", "Linux"): DEFAULT_LIB_LINUX,
    ("symuvia", "Windows"): DEFAULT_LIB_WINDOWS,
}

# *****************************************************************************
# DATA SYMUVIA
# *****************************************************************************

# *****************************************************************************
# STREAM CONSTANTS
# *****************************************************************************

BUFFER_STRING = 1000000
WRITE_XML = False
TRACE_FLOW = False
LAUNCH_MODE = "lite"
TOTAL_SIMULATION_STEPS = 0

FIELD_DATA = {
    "@abs": "abscisa",
    "@acc": "acceleration",
    "@dst": "distance",
    "@id": "vehid",
    "@ord": "ordinate",
    "@tron": "link",
    "@type": "vehtype",
    "@vit": "speed",
    "@voie": "lane",
    "@z": "elevation",
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
}

FLOAT_SELECT = float64
INT_SELECT = int32

FIELD_FORMATAGG = {
    "abscisa": (array, FLOAT_SELECT),
    "acceleration": (array, FLOAT_SELECT),
    "distance": (array, FLOAT_SELECT),
    "vehid": (array, INT_SELECT),
    "ordinate": (array, FLOAT_SELECT),
    "link": (list, None),
    "vehtype": (list, None),
    "speed": (array, FLOAT_SELECT),
    "lane": (array, INT_SELECT),
    "elevation": (array, FLOAT_SELECT),
}

# *****************************************************************************
# XML Data
# *****************************************************************************

# DATE/TIME INFORMATION
HOUR_FORMAT = "%H:%M:%S"
DELTA_TIME = timedelta(minutes=1)
TIME_STEP = timedelta(seconds=1).total_seconds()
today = date.today().strftime("%Y-%m-%d")
st_time = datetime.now()
ed_time = st_time + DELTA_TIME
st_time_str = st_time.strftime("%H:%M:%S")
ed_time_str = ed_time.strftime("%H:%M:%S")

# SIMULATION INFORMATION
DCT_SIMULATION_INFO = {
    "id": "simID",
    "pasdetemps": f"{TIME_STEP}",
    "debut": f"st_time_str",
    "fin": f"ed_time_str",
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
DCT_TRAFIC_INFO = {"id": "trafID", "accbornee": "true", "coeffrelax": "4", "chgtvoie_ghost": "false"}

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


TP_VEHTYPES = ({"id": "HDV", "w": "-5", "kx": "0.12", "vx": "25"}, {"id": "CAV", "w": "-5", "kx": "0.12", "vx": "25"})

TP_ACCEL = ({"ax": "1.5", "vit_sup": "5.8"}, {"ax": "1", "vit_sup": "8"}, {"ax": "0.5", "vit_sup": "infini"})

# *****************************************************************************
# CONTROL
# *****************************************************************************

BUFFER_CONTROL = 10  # Amount of control samples stored in memory

# *****************************************************************************
# VEHICLE DYNAMICS
# *****************************************************************************

ENGINE_CONSTANT = 0.2

# *****************************************************************************
# COMMUNICATION
# *****************************************************************************

RADIOUS_ANT = 500

if __name__ == "__main__":
    print(os.environ.get("SYMUVIALIB"))
