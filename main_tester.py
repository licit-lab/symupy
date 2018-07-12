import os 
from symupy.func import Simulation 

file_path = []
file_name = []

fildir = '/Users/ladino/Documents/03-Code/02-Python/ISTTT2019/Network/Merge_Demand_CAV.xml'
symdir = '/Users/ladino/Documents/03-Code/02-Python/symupy/symupy/symuvia/Contents/Frameworks/libSymuVia.dylib'
#symdir = '/Users/ladino/Documents/03-Code/02-Python/ISTTT2019/Symuvia/Contents/Frameworks/libSymuVia.dylib'

x = Simulation(fildir,symdir)
print('Load Simulation')
r = x.load_Simulation()
print(f'Load sim {r}')
print('About to Run')
b = x.run_Simulation()
print('Finished with success!')


print('Runing single step Simulation')
r = x.load_Simulation()
print(f'Load sim {r}')
# #x.run_SimulationbyStep()
print('Init')
x.init_Simulation()
print('State')
print(x.bSuccess)
print('Advance')
x.run_Step()
s = x.query_DataStep()
print(s)
print(x.bSuccess)
x.run_Step()
s = x.query_DataStep()
print(s)
print(x.bSuccess)
#print(locals())


print('Runing iterative Simulation')
nI = x.set_NumberIterations(120)
print(nI)
r = x.load_Simulation()
print(f'Load sim {r}')
print('Init')
x.init_Simulation()
print('State')
print(x.bSuccess)
print(f'Advance {nI} steps')
x.run_SimulationbyStep()