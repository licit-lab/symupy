from datetime import date, datetime, timedelta
from numpy import array, float64, int32

# *****************************************************************************
# CONNECTOR
# *****************************************************************************
# Buffer string size
BUFFER_STRING = 1000000


# *****************************************************************************
# DATA SYMUVIA
# *****************************************************************************
HOUR_FORMAT = "%H:%M:%S"  # Format time from xml file


# *****************************************************************************
# DATA SYMUVIA
# *****************************************************************************
RADIOUS_ANT = 500  # meters. Default distance scope antenna before

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
    "pasdetemps": f"TIME_STEP",
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

# *****************************************************************************
# DATA CONTROL
# *****************************************************************************
BUFFER_CONTROL = 10  # Amount of control samples stored in memory

# *****************************************************************************
# DATA VEHICLE DYNAMICS
# *****************************************************************************
ENGINE_CONSTANT = 0.2
