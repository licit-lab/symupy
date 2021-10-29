# Traffic XML Input File

## General structure

Simulations within `SymuFlow` require of two main components:

1. The traffic simulation library which can be obtained from [anaconda](https://anaconda.org/licit-lab/symuflow) or directly by compiling the [source code](https://github.com/licit-lab/symuflow).
2. An [XML File](#input-xml-file-description) containing a set of fields to launch a traffic simulation

The purpose of this document is to introduce the main fields so that a traffic simulation can be reproduced.

## Input XML File description:

A formal description of each one of the fields wi file can be found [here](https://github.com/licit-lab/symuflow/blob/master/symuvia/config/reseau.xsd)

### Initial structure

Define this to provide the general configuration.

```xml
<ROOT_SYMUBRUIT
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="path/to/reseau.xsd"
version="2.05">
  <SIMULATIONS/>
  <RESEAUX/>
  <SCENARIOS/>
  <TRAFICS/>
</ROOT_SYMUBRUIT>
```

### Simulation information

This tag defines information regarding the simulation.

#### `<SIMULATIONS/>`

```xml
<SIMULATIONS>
    <SIMULATION
    id="simID"
    pasdetemps="1"
    debut="00:00:00"
    fin="00:01:30"
    loipoursuite="exacte"
    comportementflux="iti"
    date="1985-01-17"
    titre=""
    proc_deceleration="false"
    seed="1">
        <RESTITUTION
        trace_route="false"
        trajectoires="true"
        debug="false"
        debug_matrice_OD="false"
        debug_SAS="false"/>
    </SIMULATION>
</SIMULATIONS>
```

| Parameter           |            Description            | Default value  |
| ------------------- | :-------------------------------: | :------------: |
| `id`                |           Simulation id           |   `"simID"`    |
| `pasdetemps`        |     Simulation time step [s]      |     `"1"`      |
| `debut`             |            Start time             |  `"00:00:00"`  |
| `fin`               |             Stop time             |  `"00:01:30"`  |
| `loipoursuite`      |      CF (`exacte`,`estimee`)      |   `"exacte"`   |
| `comportementflux`  | Flow behavior (`dir`,`des`,`iti`) |    `"iti"`     |
| `date`              |          Simulation date          | `"1985-01-17"` |
| `titre`             |         Simulation title          |      `""`      |
| `proc_deceleration` |       Relaxatoin procedure        |   `"false"`    |
| `seed`              |           Initial seed            |     `"1"`      |

##### `<RESTITUTION/>`

Restitution data relates information that can be exported after the simulation is executed.

| Parameter        |         Description         | Default value |
| ---------------- | :-------------------------: | :-----------: |
| trace_route      |   Export vehicles routes    |   `"false"`   |
| trajectoires     | Export vehicle trajectories |   `"true"`    |
| debug            |          Log mode           |   `"false"`   |
| debug_matrice_OD |         Log OD data         |   `"false"`   |
| debug_SAS        |        Log SAS data         |   `"false"`   |
| csv              |   Safe data in csv format   |   `"false"`   |


### Traffic information

This tag defines information regarding the simulation.

#### `<TRAFICS/>`

```xml
<TRAFICS>
  <TRAFIC
  id="trafID"
  accbornee="true"
  coeffrelax="0.55"
  chgtvoie_dstfin="50"
  chgtvoie_ghost="false">
    <TRONCONS/> <!-- check below subsection for details -->
    <TYPES_DE_VEHICULE/>
    <EXTREMITES/>
    <PARAMETRAGE_CAPTEURS/>
    <CONTROLEURS_DE_FEUX/>
  </TRAFIC>
 </TRAFICS>
```

| Parameter                             |                       Description                       | Default value |
| ------------------------------------- | :-----------------------------------------------------: | :-----------: |
| `id`                                  |             identifier for traffic scenario             |  `"trafID"`   |
| `accbornee`                           |                  bounded acceleration                   |   `"true"`    |
| `coeffrelax`                          |                 relaxation coefficient                  |     `"1"`     |
| `chgtvoie_dstfin`                     | distance before section  end to force a lane change [m] |    `"50"`     |
| `chgtvoie_dstfin_force`               | forced distance before the end for a lane change   [m]  |      --       |
| `chgtvoie_dstfin_force_phi`           |  phi value lane change within `chgtvoie_dstfin_force`   |     `"1"`     |
| `agressivite`                         |                     aggressive mode                     |   `"false"`   |
| `chgtvoie_ghost`                      |      continuous lane changing mode (phantom mode)       |     `"0"`     |
| `chgtvoie_ghost_durationMin`          |         minimal time duration in ghost lane [s]         |     `"0"`     |
| `chgtvoie_ghost_durationMax`          |         maximal time duration in ghost lane [s]         |     `"8"`     |
| `chgtvoie_ghost_lenghtBevel`          |  distance before end for lane change(ghost mode)  [m]   |    `"20"`     |
| `PeriodeAgregationCapteurs`           |           Aggregation period for sensors [s]            |    `"30"`     |
| `Gamma`                               |                      Gamma factor                       |     `"1"`     |
| `Mu`                                  |                  Priority coefficient                   |     `"1"`     |
| `Beta`                                |     Roundabout only: free flowinsertion probability     |    `"0.5"`    |
| `BetaInt`                             |    Roundabout only: detect veh insertion probability    |    `"0.3"`    |
| `pos_cpt_Av`                          |     Sensor position w.r.t  downstream section  [m]      |    `"20"`     |
| `ti`                                  |                     Insertion time                      |     `"0"`     |
| `tt`                                  |                      Crossing time                      |     `"0"`     |
| `depassement`                         |     Overtaking (by passing on the opposite section)     |   `"false"`   |
| `traversees`                          |         global management of crossing conflicts         |   `"false"`   |
| `meso_nb_vehicules_chgt_voie`         | meso: # non-priority vehicles to be considered per lane |     `"1"`     |
| `mode_depassement_chgt_direction`     | active congestion mode: overtake allowed w.r.to leader  |   `"false"`   |
| `distance_depassement_chgt_direction` |       distance to perform active congestion mode        |    `"20"`     |

#### `<TRONCONS/>`

```xml
<TRONCONS>
    <TRONCON
    id="TR01"/>
    <TRONCON
    id="TR02"/>
</TRONCONS>
```

| Parameter |               Description                | Default value |
| --------- | :--------------------------------------: | :-----------: |
| `id`      | identifier for the section link [string] |      --       |

#### `<TYPES_DE_VEHICLE/>`

```xml
<TYPES_DE_VEHICULE>
    <TYPE_DE_VEHICULE
    id="VL"
    w="-5.8823"
    kx="0.17"
    vx="25">
      <ACCELERATION_PLAGES>
        <ACCELERATION_PLAGE
        ax="1.5"
        vit_sup="5.8"/>
        <ACCELERATION_PLAGE
        ax="1"
        vit_sup="8"/>
        <ACCELERATION_PLAGE
        ax="0.5"
        vit_sup="infini"/>
      </ACCELERATION_PLAGES>
</TYPES_DE_VEHICULE>
```

| Parameter           |               Description               | Default value |
| ------------------- | :-------------------------------------: | :-----------: |
| `id`                |        [vehicle type][] [string]        |      --       |
| `w`                 |       congestion wave speed [m/s]       |      --       |
| `w_dispersion`      | variance of congestion wave speed [m/s] |      --       |
| `w_min`             |        min congestion wave [m/s]        |      --       |
| `w_max`             |        max congestion wave [m/s]        |      --       |
| `kx`                |        maximum density [veh/km]         |      --       |
| `inv_kx_dispersion` |               `1/kx` [km]               |      --       |
| `kx_min`            |    lower bound max density [veh/km]     |      --       |
| `kx_max`            |    upper bound max density [veh/km]     |      --       |
| `vx`                |      vehicle free flow speed [m/s]      |      --       |
| `vx_dispersion`     |     variance free flow speed [m/s]      |      --       |
| `vx_min`            |      min veh free flow speed [m/s]      |      --       |
| `vx_max`            |      max veh free flow speed [m/s]      |      --       |
| `ax`                |       max veh acceleration [m/s²]       |      --       |
| `deceleration`      |       veh decceleration [m/s²] >0       |      --       |

##### `<ACCELERATION_PLAGES/>`

Defines a acceleration/map speed threshold

| Parameter |            Description            | Default value |
| --------- | :-------------------------------: | :-----------: |
| `ax`      | acceleartion to be applied [m/s²] |      --       |
| `vit_sup` |    current vehicle speed [m/s]    |      --       |


#### `<EXTREMITES/>`

This tag defines the vehicle creation for an extreme point in the network. Check [network information](#network-information) for more details on the network topology.

```xml
<EXTREMITES>
  <EXTREMITE
  id="Ext_Out"
  typeCreationVehicule="distributionExponentielle">
    <CREATION_VEHICULES/>
    <FLUX_GLOBAL/>
    <FLUX_TYPEVEHS/>
    <CAPACITES/>
  </EXTREMITE>
<EXTREMITES>
```

| Parameter              |                     Description                     | Default value |
| ---------------------- | :-------------------------------------------------: | :-----------: |
| `id`                   |              extreme point identifier               |      --       |
| `typeCreationVehicule` | `distributionExponentielle`: exponential generation |      --       |
|                        |           `listeVehicules`: explicit list           |      --       |


##### `<CREATION_VEHICULES>`

This tag describes the way vehicles can be individually generated by hand

```xml
<CREATION_VEHICULES>
    <CREATION_VEHICULE
    typeVehicule="VL"
    destination="Ext_Out"
    instant='1.00'/>
</CREATION_VEHICULES>
```

| Parameter      |                     Description                      | Default value |
| -------------- | :--------------------------------------------------: | :-----------: |
| `typeVehicule` | vehicle type should match [vehid](#types_de_vehicle) |      --       |
| `destination`  |      vehicle destination [extreme](#extremites)      |      --       |
| `instant`      |                instant time creation                 |      --       |
| `num_voie`     |                     lane number                      |     `"1"`     |
| `route`        |    route a vehicle can take see [routes](#routes)    |      --       |

##### `<FLUX_GLOBAL/>`

This tag describes vehicle generation based on `exponential distribution` for all vehicle types

```xml
 <FLUX_GLOBAL>
    <FLUX/>
    <REP_TYPEVEHICULES/>
</FLUX_GLOBAL>
```
###### `<FLUX/>`

This tag defines the demand generation of vehicles:

```xml
<FLUX>
  <DEMANDES/>
  <REP_DESTINATIONS/>
</FLUX>
```

| Parameter         |                     Description                      | Default value |
| ----------------- | :--------------------------------------------------: | :-----------: |
| `id_typevehicule` | vehicle type should match [vehid](#types_de_vehicle) |      --       |

A couple of tags are required once `<FLUX/>` is defined:

- **`<DEMANDES/>`**

  ```xml
  <DEMANDES>
    <DEMANDE niveau="0.8" duree="200"/>
    <DEMANDE niveau="0.2" duree="100"/>
  </DEMANDES>
  ```

  This tag defines the amount of vehicles to be generated. `<DEMAND>` tags are cumulative in time so in the previoius example a demand of `0.8` will be generated during `200` seconds and then a demand of `0.2` will be generated for `100`s afterwards.

  | Parameter |     Description      | Default value |
  | --------- | :------------------: | :-----------: |
  | `niveau`  | vehicle flow [veh/h] |      --       |
  | `duree`   |  time duration [s]   |      --       |

- **`<REP_DESTINATIONS/>`**

  This tag defines the destinations of specific vehicle types

  ```xml
  <REP_DESTINATIONS>
    <REP_DESTINATION>
        <DESTINATION coeffOD="1" sortie="Ext_Out">
            <ROUTE coeffAffectation="1" id="R01"/>
        </DESTINATION>
    </REP_DESTINATION>
  </REP_DESTINATIONS>
  ```

    - ***`<REP_DESTINATION/>`***

      | Parameter         |                           Description                           | Default value |
      | ----------------- | :-------------------------------------------------------------: | :-----------: |
      | `sortie`          |           vehicle destination [extreme](#extremites)            |      ---      |
      | `coeffOD`         | Coefficient of the OD matrix for the origin (current extremity) |      --       |
      | `coefAffectation` |  Assignment coefficient for vehicles taking a [route](#route)   |      --       |


###### `<REP_TYPEVEHICULES/>`

This tag defines the vehicle assignment in time. The sum of `coeffs` should be `1`.
```xml
    <REP_TYPEVEHICULES>
        <REP_TYPEVEHICULE duree="60" coeffs="1 0"/>
        <REP_TYPEVEHICULE duree="10" coeffs="0 1"/>
    </REP_TYPEVEHICULES>
```

| Parameter |                                   Description                                   | Default value |
| --------- | :-----------------------------------------------------------------------------: | :-----------: |
| `duree`   |                   vehicle destination [extreme](#extremites)                    |      ---      |
| `coeffs`  | list of assignment coefficient per [vehid](#types_de_vehicle) e.g (`"0.2 0.8"`) |      --       |


##### `<FLUX_TYPEVEHS/>`

This tag describes vehicle generation based on `exponential distribution` for a specific vehicle type

```xml
<FLUX_TYPEVEHS>
  <FLUX_TYPEVEH
  id_typevehicule="VL">
    <FLUX/>
  </FLUX_TYPEVEH>
</FLUX_TYPEVEHS>
```

Check the [flux](#flux) tag for moe information regarding the way vehicles can be generated.


##### `<CAPACITES/>`

This tag defines the output flow of a specific link towards the downstream.

```xml
<CAPACITES>
  <CAPACITE valeur="1" duree="200"/>
  <CAPACITE valeur="0.2" duree="200"/>
<CAPACITES/>
```

| Parameter |          Description           | Default value |
| --------- | :----------------------------: | :-----------: |
| `valeur`  |     value of the capacity      |      --       |
| `duree`   | duration of the capacity value |      --       |


#### `<CONNEXIONS_INTERNES/>`

This tag defines internal network connections that tie two different road segments

```xml
<CONNEXIONS_INTERNES>
    <CONNEXION_INTERNE id="CAF_0_0"/>
    <CONNEXION_INTERNE id="CAF_0_1"/>
<CONNEXIONS_INTERNES/>
```
| Parameter |              Description               | Default value |
| --------- | :------------------------------------: | :-----------: |
| `id`      | internal conection identifier [string] |      --       |

#### `<PARAMETRAGE_CAPTEURS/>`

This tag defines parametrization for traffic sensors within the network:

```xml
<PARAMETRAGE_CAPTEURS periodeagregation="180" t0="0">
  <CAPTEURS>
    <CAPTEUR_LONGITUDINAL/>
    <CAPTEUR_EDIE/>
    <CAPTEUR_MFD/>
    <CAPTEUR_BLUETOOTH/>
    <CAPTEUR_RESERVOIR/>
  <CAPTEURS/>
<PARAMETRAGE_CAPTEURS/>
```

| Parameter                        |                         Description                          | Default value |
| -------------------------------- | :----------------------------------------------------------: | :-----------: |
| `periodeagregation`              |           aggregation time period of a sensor [s]            |      --       |
| `t0`                             |          time after which the sensor aggregates [s]          |     `"0"`     |
| `periodeagregationEdie`          |               aggregation time period for Edie               |      --       |
| `t0Edie`                         |     time after which the Edie sensor aggregates data [s]     |     `"0"`     |
| `periodeagregationLongitudinale` |          aggregation time period for Longitudinale           |      --       |
| `t0Longitudinal`                 | time after which the Longitudinal sensor aggregates data [s] |     `"0"`     |
| `periodeagregationMFD`           |               aggregation time period for MFD                |      --       |
| `t0MFD`                          |     time after which the MFD sensor aggregates data [s]      |     `"0"`     |
| `periodeagregationBlueTooth`     |            aggregation time period for BlueTooth             |      --       |
| `t0BlueTooth`                    |     time after which the Blue sensor aggregates data [s]     |     `"0"`     |
| `t0Reservoir`                    |  time after which the Reservoir sensor aggregates data [s]   |     `"0"`     |

##### `<CAPTEUR_LONGITUDINAL/>`
##### `<CAPTEUR_EDIE/>`
##### `<CAPTEUR_MFD/>`

```xml
<CAPTEUR_MFD id="sensor_zone_1_1">
      <TRONCONS>
        <TRONCON id="T_OE_4_5" />
        <TRONCON id="T_EO_4_24" />
        <TRONCON id="T_NS_5_4" />
      <TRONCONS/>
    <CAPTEUR_MFD/>
```

##### `<CAPTEUR_BLUETOOTH/>`
##### `<CAPTEUR_RESERVOIR/>`



#### `<CONTROLEURS_DE_FEUX>`

```xml
<CONTROLEURS_DE_FEUX>
                <CONTROLEUR_DE_FEUX id="CDF_CAF_0_0">
```

### Network information

This tag defines information regarding network connectivity and internal flow management. This results on allowed directions, link connections etc.

```xml
<RESEAU id="resID">
  <TRONCONS/>
  <CONNEXIONS/>
```
#### `<TRONCONS>`

This tag defines the connection between road segments a.k.a links

```xml
<TRONCONS>
    <TRONCON
    id="T_EO_0_0"
    id_eltamont="E_EO_0"
    id_eltaval="CAF_0_28"
    extremite_amont="8997.000000 307.500000"
    extremite_aval="8703.000000 307.500000"
    largeur_voie="3">
    <POINTS_INTERNES>
      <POINT_INTERNE coordonnees="-8.715574274765817 199.61946980917457"/>
      <POINT_INTERNE coordonnees="-17.364817766693033 198.4807753012208"/>
      <POINT_INTERNE coordonnees="-25.881904510252074 196.59258262890683"/>
    <POINTS_INTERNES/>
    <TRONCON
    id="T_EO_0_1"
    id_eltamont="CAF_0_28"
    id_eltaval="CAF_0_27"
    extremite_amont="8697.000000 307.500000"
    extremite_aval="8403.000000 307.500000"
    largeur_voie="3"/>
<TRONCONS/>

```
| Parameter       |                                Description                                 | Default value |
| --------------- | :------------------------------------------------------------------------: | :-----------: |
| id              |                  link id should match [linkid](#troncons)                  |      --       |
| id_eltamont     |                id of previous (upstream) link or extremity                 |      --       |
| id_eltaval      |                 id of next (downstream ) link or extremity                 |      --       |
| extremite_amont | abcissa, ordinate of the upstream point of link (Lambert93) e.g (`"0 0"` ) |      --       |
| extremite_aval  |         abcissa, ordinate of the downstream point link (Lambert93)         |      --       |
| largeur_voie    |                                 lane width                                 |      --       |
| vit_reg         |                        max speed regulation in link                        |      ""       |


##### `<POINTS_INTERNES>`

This tag defines internal connection points of the link to model curved links:

| Parameter    |                                Description                                 | Default value |
| ------------ | :------------------------------------------------------------------------: | :-----------: |
| `coordonees` | abcissa, ordinate of the upstream point of link (Lambert93) e.g (`"0 0"` ) |      --       |

#### `<CONNEXIONS/>`

This tag defines network connectivity and available routing within the traffic network

```xml
<CONNEXIONS>
  <ROUTES/>
  <EXTREMITES/>
  <REPARTITEURS/>
  <GIRATOIRES/>
  <CARREFOURSAFEUX/>
<CONNEXIONS/>
```
For each tag details are:

##### `<ROUTES>`

This tag defines a specific route a vehicle can follow

```xml
<ROUTES>
  <ROUTE description="From In to Out" id="R01">
    <TRONCONS_>
        <TRONCON_ id="First_link"/>
        <TRONCON_ id="Second_link"/>
    </TRONCONS_>
  </ROUTE>
</ROUTES>
```

##### `<EXTREMITES>`

This tag defines the list of extreme points of the network. An extreme point is an entering or exiting point of vehicles in the network:

```xml
<EXTREMITES>
    <EXTREMITE id="Ext_In"/>
    <EXTREMITE id="Ext_Out"/>
</EXTREMITES>
```

| Parameter |           Description            | Default value |
| --------- | :------------------------------: | :-----------: |
| `id`      | extremity of the network [sring] |      ---      |

##### `<REPARTITEURS/>`

This tag defines the interconnection of several roads. Crossings, intersections are modeled here

```xml
<REPARTITEURS>
  <REPARTITEUR id="AC_to_B">
    <MOUVEMENTS_AUTORISES>
        <MOUVEMENT_AUTORISE id_troncon_amont="Zone_A">
            <MOUVEMENT_SORTIES>
                <MOUVEMENT_SORTIE id_troncon_aval="Zone_B"/>
            </MOUVEMENT_SORTIES>
        </MOUVEMENT_AUTORISE>
        <MOUVEMENT_AUTORISE id_troncon_amont="Zone_C">
            <MOUVEMENT_SORTIES>
                <MOUVEMENT_SORTIE id_troncon_aval="Zone_B"/>
            </MOUVEMENT_SORTIES>
        </MOUVEMENT_AUTORISE>
    </MOUVEMENTS_AUTORISES>
</REPARTITEUR>
```


| Parameter          |                   Description                    | Default value |
| ------------------ | :----------------------------------------------: | :-----------: |
| `id_troncon_amont` |   link upstream (from) of the network [sring]    |      ---      |
| `id_troncon_aval`  | link downstream (towards) of the network [sring] |      ---      |

****
##### `<GIRATOIRES/>`

##### `<CARREFOURSAFEUX/>`

This tag describe the parameter setup for a traffic light.

```xml
<CONTROLEURS_DE_FEUX>
    <CARREFOURAFEUX vit_max="15" controleur_de_feux="CDF_CAF_0_0" id="CAF_0_0">
        <MOUVEMENTS_AUTORISES>
            <MOUVEMENT_AUTORISE id_troncon_amont="T_SN_28_0">
                <MOUVEMENT_SORTIES>
                    <MOUVEMENT_SORTIE id_troncon_aval="T_SN_29_0"/>
                    <MOUVEMENT_SORTIE id_troncon_aval="T_OE_0_1"/>
                    <MOUVEMENT_SORTIE id_troncon_aval="T_EO_0_29"/>
                </MOUVEMENT_SORTIES>
            </MOUVEMENT_AUTORISE>
<CONTROLEUR_DE_FEUX id="CDF_CAF_0_0">
  <PLANS_DE_FEUX>
    <PLAN_DE_FEUX id="p_CDF_CAF_0_0_1" debut="00:00:00">
      <SEQUENCES>
        <SEQUENCE duree_totale="30">
            <SIGNAUX_ACTIFS>
                <SIGNAL_ACTIF
                duree_retard_allumage="0"
                duree_vert="30"
                troncon_entree="T_OE_0_0"
                troncon_sortie="T_SN_29_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_OE_0_0" troncon_sortie="T_OE_0_1"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_OE_0_0" troncon_sortie="T_NS_1_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_EO_0_28" troncon_sortie="T_SN_29_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_EO_0_28" troncon_sortie="T_NS_1_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_EO_0_28" troncon_sortie="T_EO_0_29"/>
            </SIGNAUX_ACTIFS>
        </SEQUENCE>
        <SEQUENCE duree_totale="30">
            <SIGNAUX_ACTIFS>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_SN_28_0" troncon_sortie="T_SN_29_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_SN_28_0" troncon_sortie="T_OE_0_1"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_SN_28_0" troncon_sortie="T_EO_0_29"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_NS_0_0" troncon_sortie="T_OE_0_1"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_NS_0_0" troncon_sortie="T_NS_1_0"/>
                <SIGNAL_ACTIF duree_retard_allumage="0" duree_vert="30" troncon_entree="T_NS_0_0" troncon_sortie="T_EO_0_29"/>
            </SIGNAUX_ACTIFS>
        </SEQUENCE>
      </SEQUENCES>
    </PLAN_DE_FEUX>
  </PLANS_DE_FEUX>
</CONTROLEUR_DE_FEUX>
```

#### `<PARAMETRAGE_VEHICULES_GUIDES/>`

### Scenario information

This tag defines information regarding the scenario to be simulated. An scenario consist on choices of simulation, traffic and network information.

```xml
<SCENARIOS>
  <SCENARIO
  id="defaultScenario"
  simulation_id="simID"
  trafic_id="trafID"
  reseau_id="resID"
  dirout="test_output"
  prefout="bottleneck_1truck"/>
</SCENARIOS>
```
| Parameter       |   Description    |    Default value    |
| --------------- | :--------------: | :-----------------: |
| `id`            |   scenario id    | `"defaultScenario"` |
| `simulation_id` |  simulation id   |      `"simID"`      |
| `trafic_id`     |    traffic id    |     `"trafID"`      |
| `reseau_id`     |    network id    |      `"resID"`      |
| `dirout`        | output directory |       `"OUT"`       |
| `prefout`       |  output prefix   |        `""`         |