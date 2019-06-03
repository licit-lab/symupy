import sys
from ctypes import cdll, create_string_buffer, c_int, byref, c_double
import os


def hola():
    print("Say hi")


# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
try:
    os.chdir(os.path.join(os.getcwd(
    ), '../../../../../Dropbox/03-Teaching/01-ITS Course/2018-1/Material ITS - Background/SymuVia osx'))
    print(os.getcwd())
except:
    pass

# %%

# lib_path = '/Volumes/Data/Dropbox/DEV_PLATEFORME_SYMUVIA/SymubruitDLL/Release/osx/'
# lib_name = 'libSymuVia.dylib'

# full_name = lib_path+lib_name

full_name = "/Users/ladino/Documents/01-Platforms/01-Symuvia/05-SymuViaModPos/darwin/libSymuVia.dylib"
print(full_name)

symuvialib = cdll.LoadLibrary(full_name)

if symuvialib is None:
    print('Impossible de charger libSymuVia.dylib !')

print('\n Library loaded\n')

# inputfile_path = '/Volumes/Data/Dropbox/Partage_Lafayette/resaux/'
# inputfile_name = 'LafayetteVOpenSource.xml'

# full_inputfile = inputfile_path+inputfile_name

full_inputfile = "/Users/ladino/Documents/03-Code/02-Python/practices/demo-scoop/data/xml/1_scenario_hdv_90_chdv_10.xml"
print(full_inputfile)

m = symuvialib.SymLoadNetworkEx(full_inputfile.encode('UTF8'))
print('\n Network loaded\n')

sFlow = create_string_buffer(10000)
bEnd = c_int()

time = range(60)
for s in time:

    # For all vehicle connected if created:
    # symuvialib.SymDriveVehiculeEx(Id,sTroncon, nVoie, dPos, bForce)

    bResult = symuvialib.SymRunNextStepEx(sFlow, 1, byref(bEnd))
    print('Instant:', s+1)

    stype = 'VL'
    sOrigin = 'E_Moliere_S'
    sDestination = 'S_Moliere_N'
    nVoie = c_int(1)
    dbTime = c_double(0.2)
    nIdVeh = symuvialib.SymCreateVehicleEx(stype, sOrigin.encode(
        'UTF8'), sDestination.encode('UTF8'), nVoie, dbTime)
    print('Vehicle created', nIdVeh)

dPos = 15
sLink = 'Rue_Moliere_SN_1'
nVoie = c_int(1)

time2 = range(5)

bResult = symuvialib.SymRunNextStepEx(sFlow, 1, byref(bEnd))
nIdVeh = 59
nres = symuvialib.SymDriveVehicleEx(
    nIdVeh, sLink.encode('UTF8'), nVoie, dPos, 1)
bResult = symuvialib.SymRunNextStepEx(sFlow, 1, byref(bEnd))

print('Drive ', nres)

for s in time2:

    dPos = dPos + 2
    nres = symuvialib.SymDriveVehicleEx(
        nIdVeh, sLink.encode('UTF8'), nVoie, c_double(dPos), 1)
    print('Drive ', nres)

    bResult = symuvialib.SymRunNextStepEx(sFlow, 1, byref(bEnd))

for s in time:

    bResult = symuvialib.SymRunNextStepEx(sFlow, 1, byref(bEnd))
    print('Instant:', s+1)

del symuvialib


# %%


# %%


# %%
