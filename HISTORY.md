# History

# 1.0.0

* SymuPy is now available as a conda package 
* Default microsimulation library `SymyVia` → `SymuFlow`
* Add `MonitorApp` feature in order to monitor your network 
* New commands added: 
  * `AlterRoute` 
  * ``
* New command line interface available
  * `symuflow` 
  * `symymaster` 

## 0.5.1 (2021-02-15)

* Now detection of symuflow is based on default installation of symuflow (via conda)
* Pining python version

## 0.5.0 (2020-12-8)

* XML buffer parser has a new implementation 
* Now you can trace vehicle data inside the connector via `connector.vehicles`
* Observer patterns to handle vehicle list 
* Sorted frozen sets to handle subset of vehicles


## 0.4.2 (2020-11-09)

* Refactoring configurator
* Updating constants
* Changing signature of connector 

## 0.4.1 (2020-10-06)

* Adding basic tutorials

## 0.4.0 (2020-10-05)

* The API is in process to be cleaned. 
* Tests are now launched in pytest 

## 0.3.4 (2020-06-04)

* Fix bug retrieve text from simulator request 


## 0.3.3 (2020-05-23)

* Now `get_total_travel_distance/get_total_travel_time` support list of sensors 


## 0.3.2 (2020-05-23)

* Fix bug of Network Add Control Zone.

## 0.3.1 (2020-04-22)

* Fix bug of Network Control Zone by introducing `SymApplyControlZonesEx`

## 0.3.0 (2020-04-22)

* Now a configurator can be declared at the declaration of a Simulator via multiple parameters
* You can launch a simulation by passing a `string` to `run_simulation` method or `register_simulation` method
* State machine has been internally implemented. Some Fixes are required in order to 
* Filenames are now handled by the scenario. 
* Simulation ends now by calling the method `SymUnloadCurrentNetworkEx`

## 0.2.5 (2020-04-10)

* Fixes an error when creating an instance of `Simulator`
* Adds documentation to the `Simulator` class

## 0.2.4 (2020-04-09)

* A basic state machine has been implemented to handle simulation status
* Now [documentation](https://symupy.readthedocs.io/en/latest/) is available 
* A configurator has been added to handle execution of the functions 
  `SymRunNextStepLiteEx` and `SymRunNextStepEx`


## 0.2.3 (2020-03-27)

* Fix bug entries on add/ modify control zone
* Fix bug now `simulationtime` accessible before starting simulation

## 0.2.2 (2020-03-25)

* Fix bug on vehicle time creation

## 0.2.1 (2020-03-20)

* Adding control zones 
* Creating vehicles with routes
* Extract indicators such as TTT, TTD and SPD for zones 
* Makefile now tests distribution

## 0.2.0 (2020-02-20)

* Standardizing python package 
* Adding documentation 
* Makefile is now available for `testing`, `cleaning`, `building`, `installing` 

## 0.1.1 (2019-06-14)

* Small fixes on basic interfacing

## 0.1.0 (2019-06-19)

* First release on PyPI.















  