# History

## 0.1.0 (2019-06-19)

* First release on PyPI.

## 0.1.1 (2019-06-14)

* Small fixes on basic interfacing

## 0.2.0 (2020-02-20)

* Standardizing python package 
* Adding documentation 
* Makefile is now available for `testing`, `cleaning`, `building`, `installing` 

## 0.2.1 (2020-03-20)

* Adding control zones 
* Creating vehicles with routes
* Extract indicators such as TTT, TTD and SPD for zones 
* Makefile now tests distribution

## 0.2.2 (2020-03-25)

* Fix bug on vehicle time creation

## 0.2.3 (2020-03-27)

* Fix bug entries on add/ modify control zone
* Fix bug now `simulationtime` accessible before starting simulation

## 0.2.4 (2020-04-09)

* A basic state machine has been implemented to handle simulation status
* Now [documentation](https://symupy.readthedocs.io/en/latest/) is available 
* A configurator has been added to handle execution of the functions 
  `SymRunNextStepLiteEx` and `SymRunNextStepEx`

## 0.2.5 (2020-04-10)

* Fixes an error when creating an instance of `Simulator`
* Adds documentation to the `Simulator` class