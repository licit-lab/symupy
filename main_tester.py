import os 
from simupy import SymuViaImporter

file_path = []
file_name = []

x = SymuViaImporter()
x.load_SymuViaLib()
print(type(x))
#print(locals())