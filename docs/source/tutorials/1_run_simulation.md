# Tutorials 

## Running a simulation in Symupy 

In order to run a simulation you need two main elements. A symuvia library. To retrieve one please retrieve the 

```{python}
from sympy.api import Simulator, Simulation 

path_simulator = "path/to/simulator/libSymuVia.dylib"
path_simulation = "path/to/simulation/scenario.xml" 
```

### Via with an automatic initializer 

You can run a simulation by using one of the specific constructors designed to run the simulation. 

```{python}
simulator = Simulator.from_path(path_simulator,path_simulation)
simulator.run()
```

### Via with a custom installation 

You can also use your own simulator. In this case you may also enable other flags

```{python}
simulator = Simulator(libraryPath = path_simulator, 
                      traceFlow = True, # Export trajectory
                      writeXML = True, # Write output XML
                    )
simulator.register_simulation(path_simulation)
simulator.run()
```

### Via a simulation by steps 

You may run a simulation by executing step by step simulations. Activities to control and manipulate vehicles can be executed while launching step by step simulations. 

```{python}
simulator = Simulator.from_path(path_simulator,path_simulation)
with simulator as s: 
    while s.do_next:
        s.run_step()
```