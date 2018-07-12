import os 
from symupy.func import Simulation 

file_path = []
file_name = []

fildir = '/Users/ladino/Documents/03-Code/02-Python/ISTTT2019/Network/Merge_Demand_CAV.xml'
symdir = '/Users/ladino/Documents/03-Code/02-Python/symupy/symupy/symuvia/Contents/Frameworks/libSymuVia.dylib'

x = Simulation(fildir,symdir)
print('About to Run')
b = x.run_Simulation()
print('Finished with success!')
nI = x.set_NumberIterations(0)
print(nI)

#print(locals())