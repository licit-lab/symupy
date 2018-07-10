from simupy import SymuViaImporter

x = SymuViaImporter()
x.load_SymuViaLib()
print(x.fullSymPath)
print(locals())