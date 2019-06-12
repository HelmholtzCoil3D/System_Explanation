# 3D Helmholtz coil system

This document explains how the system was made and how it works, with the purpose to make the reproduction of the project possible.

- [3D Helmholtz coil system](#3d-helmholtz-coil-system)
- [Objective of the project](#objective-of-the-project)
- [Base Knowledge](#base-knowledge)
- [Blocks diagram](#blocks-diagram)
- [Helmholtz coils design](#helmholtz-coils-design)
  - [Simulator](#simulator)
    - [Input parameters:](#input-parameters)
    - [Console results](#console-results)
    - [Graphical Results](#graphical-results)
    - [Simulator results](#simulator-results)
  - [3D models](#3d-models)
    - [3 axis helmholtz coil 3D model](#3-axis-helmholtz-coil-3d-model)
    - [Sensor and sample support 3D model](#sensor-and-sample-support-3d-model)
    - [Pegs 3D model](#pegs-3d-model)
    - [3 feet support 3D model](#3-feet-support-3d-model)
  - [3D Print results](#3d-print-results)
    - [Coils support print](#coils-support-print)
    - [Sensor/Sample support](#sensorsample-support)
    - [Pegs](#pegs)
  - [3 Feet support](#3-feet-support)
  - [Coils winding](#coils-winding)
  - [Practical results](#practical-results)
    - [Inner coil](#inner-coil)
    - [Middle coil](#middle-coil)
    - [External coil](#external-coil)
    - [Data analysis](#data-analysis)
- [Magnetic sensor](#magnetic-sensor)
- [Controller](#controller)
  - [Power Supply](#power-supply)
  - [H-bridges](#h-bridges)
  - [MCU](#mcu)
  - [New system Block Diagram](#new-system-block-diagram)
- [Integration](#integration)
  - [system_current_finder.py and system_measurement_procedure.py](#systemcurrentfinderpy-and-systemmeasurementprocedurepy)
  - [system_plot.py](#systemplotpy)
  - [system_realtime_field_adjusting.py](#systemrealtimefieldadjustingpy)
  - [System validation](#system-validation)
- [PCBs](#pcbs)
  - [Sensor PCB](#sensor-pcb)
  - [System PCB](#system-pcb)
- [Final result](#final-result)
- [System applications](#system-applications)

# Objective of the project

This project aim is to prototype some kind of system control it automaticaly and make some fields setups in static applications.

The idea behind this project is to create a homogeneous field in some defined region where magnetic samples can be tested with a totaly known field

<p align="center">
  <img src="https://i.imgur.com/ytuayWB.png/">
  <img src="https://i.imgur.com/5vaQXRf.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/cQSHDOd.png">
</p>


The desired features in this case would be a region with errors bellow 1%, the maximium difference of the magnetic field strenght in two different points and angles with less than 1° of difference between two different points of the homogeneous region. A magnetic flux density range of 1 uT to 1 mT is desired in this region.

The region defined for the prototype at first is a **20 mm³**  region

**The system itself just generate the field**, the magnetic sample must have its own system to generate the data for posterior analysis. Analisys can be made based in the known direction and amplitude of the homogeneous region magnetic field.

# Base Knowledge

To create a homogeneous field in some free space region, the concept used was the [Helmholtz coil] that can create a homogeneous field inward from the coils to the geometric center of the estructure, the more in the center, the more homogeneous the field is.

Exitating the coils with a known current generates a known [magnetic field] (H) that is related to the magnetic flux density (B) by the permeability ($\mu$) of the material, in this case the air ([1.00000037])

The B can [saturate] depending on the material, in this case it will not happen so there are no linearity problems

Knowing that the magnetic field will be linear, so a 3 axis Helmholtz coil can be design to generate the arbitrary homogeneous magnetic field, remembering that this system must compensate the [earth magnetic field]

#  Blocks diagram

The system blocks diagram can be represented as follows:
<p align="center">
  <img src="https://i.imgur.com/3Lv7iL5.png">
</p>

The main parts of the system:
-   Helmholtz coils to generate the field
-   Controller to control the generated field throught magnetic sensors readings and current supply for the coils
-   Interface to give properly the user commands to the controller

# Helmholtz coils design

## Simulator

To design the needed helmholtz coils, an open source python library was used, [magpylib], this library is capable to calculate magnetic field, through analytical solutions, of permanent magnets and current lines or current loops.

In fact the application is static, so the helmholtz can projected as current loops placed in a helmholtz coil shape.

<p align="center">
  <img src="https://i.imgur.com/Wa3sqmD.png">
</p>

 From the cross-cut section the parameters for the coils calculation can be extracted as the following figure:

<p align="center">
  <img src="https://i.imgur.com/ME0H3qo.png">
</p>

The details about the calculator can be seen in the [Helmholtz coil calculator] and [Auxiliar library] files. Giving some parameters to the calculator, it gives us the necessary coil diameter to achieve the desired field in the center of the coil and graphics that shows the field strenght in the 3 vectors of the field separeted (x,y,z) and from this an analysis can be made to determine the homogenity of the field generated by each coil, amplitude and angle error relative to the center in the desired homogeneous region. Following the input and the results in this project.

### Input parameters:

Those are the input parameters for the calculator to find the diameter necessary the design each coil, following previous figure standards.

``` python
# have to use a little bit bigger value than wireExternalDiameter, if not, the wire will not fit inside
AllCoilsWireDiameter = (0.56 + 0.047)*1.09   # Wire diameter in mm (from dataSheet)

minRes = 0.06736                            # Ohms/m (from dataSheet)
nominal = 0.06940                           # Ohms/m (from dataSheet)
maxRes = 0.07153                            # Ohms/m (from dataSheet)

wireResistence = maxRes                     # Ohms/m (from dataSheet)


# z First Coil configuration

zInitialValueCoilDiameter = 80 # Initial value for the function that calculates the precise diameter


zCoilCurrent = 0.5             # Amperes
zLoopsInEachEvenLayer = 10     # The number of loops in each layer
zEvenLayers = 7                # The evenlayers always have to be equal to oddLayers or oddLayers + 1
zOddLayers = 7
zDesiredField = 1.25           # The desired field in the center of the Helmholtz coil

# y Second Coil configuration

yCoilCurrent = 0.5             # Amperes
yLoopsInEachEvenLayer = 6      # The number of loops in each layer
yEvenLayers = 3                # The evenlayers always have to be oddLayers + 1 or equal oddLayers
yOddLayers = 3
yDesiredField = 0.25           # The desired field in the center of the Helmholtz coil

# x Third Coil configuration

xCoilCurrent = 0.5             # Amperes
xLoopsInEachEvenLayer = 7      # The number of loops in each layer
xEvenLayers = 3                # The evenlayers always have to be oddLayers + 1 or equal oddLayers
xOddLayers = 3
xDesiredField = 0.25           # The desired field in the center of the Helmholtz coil
```

### Console results

Those are the results that shows up in the standard output, in this case the console of spyder, those results can estimate how much wire in meters and the power in watts that will be dissipated on each helmholtz coil individualy.

![](https://i.imgur.com/5LN3UF7.png)

### Graphical Results

Those are the graphical results of the calculator. For each coil a graphic is generated with the amplitude of the magnetic field of a slice in the center of the coil, this slice must have the region of interest, it also displays a 3D graphic of what the system looks like. Those graphics can help to estimate the homogenity level of the whole region.

<p align="center">
  <img src="https://i.imgur.com/wLzB2G6.png">
  <img src="https://i.imgur.com/yHOCoEb.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/GD7dLiL.png">
  <img src="https://i.imgur.com/YyC5epl.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/DbHoJWf.png">
  <img src="https://i.imgur.com/ByeGGDB.png">
</p>

As can be seen in the next figures, the calculator estimates the interference of the cables used to bring the current to the coils, the current passing throught them generates a field and it can be compared with the field generated for each coil. Just the field of the connectors is showed in the graphics. Another that can be seen is if the coils will be inside each other in the 3D representation, it's shown in the 3 coils figure that the coils don't touch each other in this case.

<p align="center">
  <img src="https://i.imgur.com/bi9lrz0.png">
  <img src="https://i.imgur.com/nGmvyGo.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/zuLQytt.png">
  <img src="https://i.imgur.com/QZL5wMg.png">
  <img src="https://i.imgur.com/Mi18fzv.png">
</p>

### Simulator results

After checking all the homogenity and interference stuff, the interested parameters to construct the coils support are shown in the next table:

Wire External Diameter = 0.6 mm

|Coils| Radius | Coil Width| Coil Height|
|:-:|-|-|-|
| Inner | 42.5 mm | 6.6 mm | 9.65 mm |
| Middle | 56.15 mm | 4 mm | 5.5 mm |
| External | 66.5 mm | 4.65 mm | 5.5 mm |
**\* rouded values**

## 3D models

With the high precision of the 3D printers ($\pm$ 1 $\mu$m) the idea was doing the 3 helmholtz coils all together in the same mechanical part, 1 piece. With this, the misalignment problems would desappear.

Misalignment example:
<p align="center">
  <img src="https://i.imgur.com/UBLSEGI.png">
</p>

To design the 3D model the utilized software was [solidWorks], a comercial software for 3D models design, good for geometric models. The design was made based in the simulating results. Besides the coils, the sensor and sample placement should be designed together with the coil, to make it easier to think the supports was separated and connected throught holes and pegs.

### 3 axis helmholtz coil 3D model

The 3 axis helmholtz coil 3D model design can be seen in the following images:

<p align="center">
  <img src="https://i.imgur.com/1w3yt66.png">
  <img src="https://i.imgur.com/ZZijRJx.png">
  <img src="https://i.imgur.com/SFO0BPS.png">
</p>

It has some holes inside to attach the sensor support and a bigger hole in the middle for the cables to link the sensor to the system. In the bottom some support points to make the coil stable in the table.

### Sensor and sample support 3D model

After some tests, the model achieved for the PCB support is shown in the following image:

<p align="center">
  <img src="https://i.imgur.com/OIBXMG0.png">
  <img src="https://i.imgur.com/UGoYnNm.png">
</p>


This model perfectly fits inside the coils support model, using the internal part to support the sensor of the system and the more external pegs and holes to support the sample. Notice that the external support is designed in such a way that the sample stays in the middle of the coils. If the sample change, the user can design another 3D model for the support to adapt the coil usage to an especific application

### Pegs 3D model

To attach the PCB support to the coils support some pegs was designed with diferent diameters, using the fact that the printer has more precision than $\pm$1 $\mu$m:

<p align="center">
  <img src="https://i.imgur.com/ucujuqK.png">
  <img src="https://i.imgur.com/xfdn5YZ.png">
</p>

Using 50 $\mu$m of difference between the pegs, will make it safe to fit in the previous models holes, testing which diameter is beter to use.

### 3 feet support 3D model

To avoid some induction fields problems that could appear for some kind of measurements, a 3 feet support for the coils support was design that the coils support just fits inside of the 3 feet support and make some distance between the table metal supports and the coils.

<p align="center">
  <img src="https://i.imgur.com/32UAFZo.png">
  <img src="https://i.imgur.com/8IpZaQa.png">
  <img src="https://i.imgur.com/kGm5bcq.png">
</p>


## 3D Print results

The company have its own 3D printers, one with really high resolutions for tiny parts and another with less resolution but with more space to print. The material is not so rigid in the high resolution printer and the prints have problems in the pos-printing process that causes some bendding problems, so for the coils support the print was made by [Reprap] Austria, that was more cheap and perfect printed than with the company printer. For the other models, the company printer was enought to do the job.

The Reprap Austria 3D printer size limit is **32**x**36**x**42** **cm**, been the largest coil external diameter around 15 cm, the printing size is fairly ok and if the company needs a bigger coil with different especification, it can be printed.

### Coils support print

The Coils support was ordered and the result can be seen:
<details>
<summary> <b>Click here to see the Coil support print result</b> </summary>
<p align="center">
  <img src="https://i.imgur.com/snpOLTE.gif">
</p>

**There's a sensor support inside of the coils printed with the company printer, that fitted really nice inside**
</details>

### Sensor/Sample support

Printed in the CTR high resolution printer:

<p align="center">
  <img src="https://i.imgur.com/mr3jVFE.png">
  <img src="https://i.imgur.com/0J0pVPR.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/FMYslBA.png">
  <img src="https://i.imgur.com/d5Cf9GZ.png">
</p>

### Pegs

Printed in the CTR high resolution printer:

<p align="center">
  <img src="https://i.imgur.com/mdp87lR.png">
</p>

## 3 Feet support

Following figure shows the 3 feet suppport printed in the lower resolution printer, that is also very good and it's used for bigger 3D models.

<p align="center">
  <img src="https://i.imgur.com/0nlz94t.png">
</p>

## Coils winding

After doing the windings really carefull, maintaining the [wire] stretched while doing each turn, it helped to get the wire really fit in the coils support. The arrangement to stretch the wire can be seen in the next image, its an improvised tool that makes some pressure in the reel, extremely important to make the coils the most near to the simulation position of the wires.

<p align="center">
  <img src="https://i.imgur.com/IUi05BB.png">
  <img src="https://i.imgur.com/KXlm8cY.png">
</p>

 The [hot glue] was used to mantain the cables fixed in the coils suppor, the result of the 3 axis coil can be seen in the following image:

<p align="center">
  <img src="https://i.imgur.com/l0JHXrs.png">
  <img src="https://i.imgur.com/IkDBRM8.png">
</p>

Each of the six coils was done individualy, doing the inside coils first, and then connected with a solder point with the respective pair (2 coils in X direction to form the X helmholtz coil for example)

## Practical results

To validate the python calculator, some measurements was made, like the resistence, inductance and generated field for each coil. Each coil is named now by inner, middle and external coil. The measurements are discussed subsequently.

### Inner coil

This coil is the most inside coil (inner), it has the most intense field of the 3 coils, that's why it's the inside coil and the one that have more windings.

Coil teorethical features:
|Feature| Value |
|-|-|
|Current| 0 ~ 0.5 *A*|
|Magnetic field generated| 0 ~ 1.25 *mT* |
|MagField/Current ration| 2.5 |
|Coil resistence| 5.264 $\Omega$|

Mesured resistence ($\Omega$), inductance (mH):

<p align="center">
  <img src="https://i.imgur.com/x8iIYAy.png">
  <img src="https://i.imgur.com/LVjreJY.png">
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/nDOGn0i.png">
  <img src="https://i.imgur.com/XJ9kA3F.png">
</p>

### Middle coil

The middle coil is the one in between other 2 coils and its purpose is to cancel the earth magnetic field.

Coil teorethical features:
|Feature| Value |
|-|-|
|Current| 0 ~ 0.5 *A*|
|Magnetic field generated| 0 ~ 0.25 *mT* |
|MagField/Current ration| 0.5 |
|Coil resistence| 1.689 $\Omega$|

Mesured resistence, inductance:

<p align="center">
  <img src="https://i.imgur.com/q5UDi7a.png">
  <img src="https://i.imgur.com/MBkaaHd.png">
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/IYxx4Vd.png">
  <img src="https://i.imgur.com/6W8auCz.png">
</p>

### External coil

External coil is the name of the further coil from the center, the biggest, same purpose as middle coil.

Coil teorethical features:
|Feature| Value |
|-|-|
|Current| 0 ~ 0.5 *A*|
|Magnetic field generated| 0 ~ 0.25 *mT* |
|MagField/Current ration| 0.5 |
|Coil resistence| 2.356 $\Omega$|

Mesured resistence, inductance:

<p align="center">
  <img src="https://i.imgur.com/Za583Jh.png">
  <img src="https://i.imgur.com/A6V55Mt.png">
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/ennhagm.png">
  <img src="https://i.imgur.com/627mrrd.png">
</p>

### Data analysis

In the previous images can be seen the current to excitate the coils and the magnetic field read from the sensor in **$\mu$T** (The sensor will be explained in the next topic), the magnetic field is already a mean of 30 measurements. The sensor can not be positioned perfectly aligned with the coils directions, then the norm of the difference should be taken to express the real value of the field generated by the coils. 

A python script ([Coil Features]) was made to handle those simple calculations and the results are shown in the next image.

![](https://i.imgur.com/2pE7k2O.png)

As seen, the field error is really tiny (bellow 2%), maybe because the windings somehow are no perfectly round and it can be reflected in this tiny error.

In the resistance the error was quite big, but for an estimative could be helpfull to have some power dissipation notion.

# Magnetic sensor

The magnetic sensor is a really important part of the project, because it will provide the measurements to understand if the coils are working properly or not and the closes some loop to adjust the field if necessary. Some research was done and some sensors was tried. The first solution encounted was the [LIS3MDL] sensor, it's for compass application and had a good range of measurement for the application, but with some tests it showed really bad response to offset errors, so another one was tried, an upgraded version of this sensor from the same company ([ST]), [LSM303D], but somehow there was the same problems. Then researched for another companies that would be specialized in magnetic sensors and then found [MEMSIC], and searching for magnetic sensors, found one that fitted in the application, [MMC3416].

The sensor have I²C interface, also have a really interesting measurement procedure, where the [set/reset] operation can be applied to extract a better measurement, the downside of this procedure is that it takes time. In this project is not a problem because the application is static.

![](https://i.imgur.com/z9eIjbb.png)

A usefull thing to do is buy the evaluation board in this case, that have everything in hardware set up to just use the sensor. To project, order and solder the PCB takes time, so to develop it faster the [MMC3416 evaluation board] was used.

![](https://i.imgur.com/vEXt4Uy.png)

# Controller

The controller part of the blocks diagram could be anything that could:

-   Control the coils field
-   Read the sensor measurements
-   Interpret the user commands

For those tasks more especificaly was needed something that could have some: 
-   I²C comunication (sensor) 
-   Current source adjustable with a good resolution, to achieve the field resolution bellow 1 uT
-   A way to change the current polarity in the coils
-   Kind of USB communication to stablish comunication with the computer (where the user interface would be implemented)

It's difficult to have all those tasks already integrated so some research was done to what to use.

## Power Supply

In one way or another, a power supply must be used to provide the energy for the coils, can be as a voltage source or a current source. Operating in the voltage source mode would imply some external controller to adjust the right current for the coils, in other way with the current source mode, the power supply must have some kind of electronic current control integrated to use this in the system. After some research found [Rigol DP800] series, specifically the 831A model, that have 0.1 mA resolution of current control with 3 channels and can be controlled by software, perfect for this application.

The software control can be done through the [python visa] that are some special libraries used to control mesurement equipaments.


[python visa]:https://pyvisa.readthedocs.io/en/latest/

<p align="center">
  <img src="https://i.imgur.com/gZmzW8N.png">
</p>


## H-bridges

To control the current polarity in the coils, a classical but really good solution can be used, the [H-bridge] control.

 ![](https://i.imgur.com/AZOmCl6.png) ![](https://i.imgur.com/uztRrHg.png) ![](https://i.imgur.com/wAxmOd2.png) 

It's system composed by 2 switches, as shown in the first figure of this section. The circuit have 3 possible states, that are shown in the figures, one state is everything open (turn off), and the other two is the current flowing to one direction of the load and the other the current is flowing in the another direction.

A lot of research was done, and most of the integrated H bridges have underload protection what is not desirable for this project, but one was found with the potential to be used, the [DRV8838DSGR] IC.

![](https://i.imgur.com/o9l9z6b.png)

This IC works with 2 digital pins to control the states and is based on N-Mosfets. It can operate in 0~11 V range which fit the application. The only downside is the fact that the load supply is not isolated from the control supply.

The power supply choosed for the current control has one of its channels a negative voltage source that is internaly connected to another positive channel. In this case the [DRV8838DSGR] H-bridge the internal connection in the references of the supply for the logic (Vcc) and the supply for the load (VM) would cause a short circuit between the negative voltage and the reference in the power supply.

For this specific channel, a different solution to also isolate the channel must be implemented. After some research the best solution would be use 4 relays to do the switch role controlling it in such a way to stay in the 3 possible states of the H-bridge. The component choosed for the switch was [CPC1002N], it's a solid-state relay, basicaly an optocoupler with more current capacity than a normal optocoupler.

![](https://i.imgur.com/tdPA7C5.png)


## MCU

To control the H-bridges and the sensor a microcontroller can be used. The microcontroller must have:
-   I²C interface peripherical
-   At least 6 free digital pins (H bridges)
-   USB comunication peripherical

And for this the [STM32L4] was choosed because of the versatility, powerful processing, easy usage and low cost, And it has all the features necessary for the system.

[STM32L4]:https://www.st.com/resource/en/datasheet/stm32l432kc.pdf

To program this controller the [stm32CUBE] was used to generate the base code and the [atollic] to edit, compile, debug and program the code.

The main code developed for the microcontroller is in those files:

-   [main.c]
-   [main.h]
-   [lib_aux.c]
-   [lib_aux.h]
-   [MCC3416_def.h]

To have more robustness the system was developed in a [finite state machine] shape, with one state for each operation.

When the microcontroller starts-up the first thing that it does is asking throught USB comunication, the size of the mean for each measurement and the time (ms) to do it, of course the bigger the measurements number, bigger the overhead will be.

After the 2 responses, the system start to operate in the state machine where there are 9 possible states besides Iddle:

|State symbol| Description of the state|
|:-:|:-|
|'D'| Procedure mean size of measurements and return the mean in the USB comunication getting back to iddle after|
|'I'| Sets the polarity to 'set' in the H-bridge connected to the channel 2 and sends back "'I' done!"|
|'i'| Sets the polarity to 'reset' in the H-bridge connected to the channel 2 and sends back "'i' done!"|
|'M'| Sets the polarity to 'set' in the H-bridge connected to the channel 3 and sends back "'M' done!"|
|'m'| Sets the polarity to 'reset' in the H-bridge connected to the channel 3 and sends back "'m' done!"|
|'E'| Sets the polarity to 'set' in the H-bridge connected to the channel 1  and sends back "'E' done!"|
|'e'| Sets the polarity to 'reset' in the H-bridge connected to the channel 1 and sends back "'e' done!"|
|'S'| Set all the polarities to a reference and sends back "'S' done!"|
|'C'| Perform continuos measurement procedures and send then to the USB comunication without getting back to the IDDLE state|

<p align="center">
  <img src="https://i.imgur.com/5ZJICKJ.png">
</p>

The 'I', 'i', 'E' and 'e' states control just the digital pin for the [DRV8838DSGR] H-bridge, the 'M' and 'm' states control 4 digital pins to control the H-bridge formed by the relays [CPC1002N].

After a state sending, the system response with a '"state" done!' for debug and flow control. The exception on this is the 'D' and 'C' states that respond with the data directly.

The USB comunication is based on UART, the baud rate of the comunication is 256000 bauds

## New system Block Diagram

With the definition of how the control will be done and with what, The blocks diagram can be redrawed into the following image:

<p align="center">
  <img src="https://i.imgur.com/lGi1RIw.png">
</p>

# Integration

With a research about how to integrate the VISA application and the USB data from microcontroller, the conclusion was to use python libraries to get the information from USB and to control the power supply, using a structered diferent scripts to do some procedure with this.

The main python libraries used for USB communication:
-   [pyvisa]
-   [pyserial]

for some data processing and to show graphics:
-   [numpy]
-   [matplotlib]

and used some standard libraries as:
-   [time]
-   [csv]
-   [re]



The existing scripts until now following:
-   [auxLib.py]
-   [system_current_finder.py]
-   [system_measurement_procedure.py]
-   [system_realtime_field_adjusting.py]
-   [spinning_Compass.py]
-   [system_plot.py]

auxLib is the library with the <s>Black Magic</s> functions that do all the work on the others scripts.

## system_current_finder.py and system_measurement_procedure.py

It calculates the necessary current to have a range of field from 'lowerFieldLimit' to 'upperFieldLimit' field, with a step of 'fieldResolution'. Running the system current finder script gives a `csv` file that contains the information to later apply it with the system measurement procedure file.

Something important to **take care** is that to calculate the currents, the coil must not move and must not have any magnetic object near to this, then in the measurement procedure, without moving the coil, just put the sample inside and apply the fields.

The calculated currents will be applied one at once, typing 'Enter' to go into the next calculated current.

## system_plot.py

Takes the `csv` file generated by [system_current_finder.py] and transform the information from text to graphics.

## system_realtime_field_adjusting.py

Set some field in the input code, 3 axis field, and then run the code. It will keep trying to adjust the field of the coils to reach the desired field inside the main region in closed-loop.

## System validation

After testing all the hardware, the scripts was developed 

**\* image of the system with the evaluation boards**

![tiny Missing Image](https://i.imgur.com/zDgtWUj.png)

Following the graphic generated by [system_plot.py] from a rotating x,y field found by [system_current_finder.py] for example:

<p align="center">
  <img src="https://i.imgur.com/OvBXIcY.png">
  <img src="https://i.imgur.com/cbLqncm.png">
</p>


# PCBs

With the validated hardware, the next step would be doing a PCB to have a more reliable and less noisy system. The PCB's were ordered from [Eurocircuits Gmbh] using the PCB eagle files.

## Sensor PCB

To make things faster, a PCB for the sensor was made, but not attaching the sensor to it, because it's hard to solder it by hand, instead it was designed to attach the evaluation board to it using a SMD connector that clicks the cable to the PCB, reducing noise problems in the I²C communication.

[Eurocircuits Gmbh]:https://www.eurocircuits.com/

The schematic and layout:
<p align="center">
  <img src="https://i.imgur.com/K3De7Ns.png">
  <img src="https://i.imgur.com/h4xlgdN.png">
</p>

## System PCB
The results after soldered:
<p align="center">
  <img src="https://i.imgur.com/iOp6hKP.png">
  <img src="https://i.imgur.com/zlb893Q.png">
</p>


The schematic and layout:
<p align="center">
  <img src="https://i.imgur.com/B85BN9M.png">
  <img src="https://i.imgur.com/tkJYENF.png">
</p>


The results after soldered:
<p align="center">
  <img src="https://i.imgur.com/33onxWX.png">
  <img src="https://i.imgur.com/1eaJG9P.png">
</p>

The cable with some twisted pairs for the noise reduction:
<p align="center">
  <img src="https://i.imgur.com/R0zvZy2.png">
</p>

The final result of the system:
<p align="center">
  <img src="https://i.imgur.com/qHP6Xhr.png">
</p>




# Final result

[order list]

<p align="center">
  <img src="https://i.imgur.com/o32hRec.png">
  <img src="https://i.imgur.com/eogJmTj.png">
</p>


<p align="center">
  <img src="https://i.imgur.com/8XdFvad.png">
</p>


# System applications

**\* Using the [system_realtime_field_adjusting.py]**
<details>
<summary> <b>Click here to see the procedure to set the zero field</b> </summary>
<p align="center">
  <img src="https://i.imgur.com/YYwEtKX.gif">
</p>

</details>
<details>
<summary> <b>Click here to see the compass in the zero field</b> </summary>
<p align="center">
  <img src="https://i.imgur.com/6OjJ9gG.gif">
</p>
</details>

</details>
<details>
<summary> <b>Click here to see the automatic measurements (fluxgate)</b> </summary>
<p align="center">

  System working

  <img src="https://i.imgur.com/YpFL2j4.gif">

  Procedure flowChart

  <img src="https://i.imgur.com/TYIyrnF.png">

  Current finder results (-180 uT to 180 uT, 0.5 uT step)

  <img src="https://i.imgur.com/hhaMBcf.png">

  Data from osciloscope

  <img src="https://i.imgur.com/CLOcnu2.png">

  Data analysis

  <img src="https://i.imgur.com/8HJcHRR.png">
  <img src="https://i.imgur.com/kUJt71W.png">

  result comparition (neosha work)
  <img src="https://i.imgur.com/6ziGVu8.png">
  <img src="https://i.imgur.com/6dymBwM.png">
  
  
</p>
</details>


<details>
<summary> <b>Youtube videos</b> </summary>

[Compass zero field demonstration]

<iframe width="560" height="315" src="https://www.youtube.com/embed/eRR1c4607lU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

[Compass zero field procedure]
<iframe width="560" height="315" src="https://www.youtube.com/embed/aR3ZOZWw4vM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

[Automatic measurements]
<iframe width="560" height="315" src="https://www.youtube.com/embed/5FVGol-J0HI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


</details>



[Automatic measurements]:https://www.youtube.com/watch?v=5FVGol-J0HI

[order list]:ComponnentsListToOrder.md

[auxLib.py]:System_integration/auxLib.py

[system_current_finder.py]:System_integration/system_current_finder.py

[system_realtime_field_adjusting.py]:System_integration/system_realtime_field_adjusting.py

[system_measurement_procedure.py]:System_integration/system_measurement_procedure.py

[spinning_Compass.py]:System_integration/spinning_Compass.py

[system_plot.py]:System_integration/system_plot.py



[re]:https://docs.python.org/3/library/re.md?highlight=re#module-re
[csv]:https://docs.python.org/3/library/csv.md?highlight=csv#module-csv
[time]:https://docs.python.org/3/library/time.md
[matplotlib]:https://matplotlib.org/
[numpy]:https://www.numpy.org/
[pyvisa]:https://pyvisa.readthedocs.io/en/latest/
[pyserial]:https://pyserial.readthedocs.io/en/latest/pyserial.md

[MMC3416 evaluation board]:ttps://media.digikey.com/pdf/Data%20Sheets/MEMSIC%20PDFs/MMC3416PJ-B_UG.pdf

[set/reset]:http://www.seraphim.com.tw/upfiles/c_supports01284968029.pdf

[main.c]:Microcontroller/main.c

[main.h]:Microcontroller/main.h

[lib_aux.h]:Microcontroller/lib_aux.h

[lib_aux.c]:Microcontroller/lib_aux.c

[MCC3416_def.h]:Microcontroller/MCC3416_def.h

[CPC1002N]:http://www.ixysic.com/home/pdfs.nsf/www/CPC1002N.pdf/$file/CPC1002N.pdf

[DRV8838DSGR]:http://www.ti.com/lit/ds/symlink/drv8838.pdf


[H-bridge]:https://en.wikipedia.org/wiki/H_bridge

[Rigol DP800]:http://beyondmeasure.rigoltech.com/acton/attachment/1579/f-01c1/1/-/-/-/-/DP800%20Datasheet.pdf

[Compass zero field demonstration]:https://www.youtube.com/watch?v=eRR1c4607lU

[Compass zero field procedure]:https://www.youtube.com/watch?v=aR3ZOZWw4vM&t=

[Helmholtz coil calculator]:helmholtzCoilsSimulations/HelmholtzCoilCalculator.md

[Auxiliar library]:helmholtzCoilsSimulations/magpylibUtils.md

[Coil Features]:CoilFeatures.md

[magpylib]:https://github.com/magpylib/magpylib

[Helmholtz coil]:https://en.wikipedia.org/wiki/Helmholtz_coil

[magnetic field]:https://en.wikipedia.org/wiki/Magnetic_field

[earth magnetic field]:https://en.wikipedia.org/wiki/Earth%27s_magnetic_field

[1.00000037]:https://en.wikipedia.org/wiki/Permeability_(electromagnetism)

[saturate]:https://en.wikipedia.org/wiki/Saturation_(magnetic)

[coil img 1]:https://i.imgur.com/AkZzpYJ.jpg

[solidWorks]:https://www.solidworks.com/

[Reprap]:https://www.reprap.cc/

[hot glue]:https://en.wikipedia.org/wiki/Hot-melt_adhesive

[Missing Image]:https://i.imgur.com/0EmAI26.png

[wire]:https://at.rs-online.com/web/p/kupferdrahte/0357750/

[LSM303D]:https://www.pololu.com/file/0J703/LSM303D.pdf

[LIS3MDL]:https://www.st.com/resource/en/datasheet/lis3mdl.pdf


[MMC3416]:http://www.memsic.com/userfiles/files/Datasheets/Magnetic-Sensors-Datasheets/MMC3416xPJ_Rev_C_2013_10_30.pdf

[MEMSIC]:https://www.memsic.com/

[ST]:https://www.st.com/content/st_com/en.md


[Missing Image]:(https://i.imgur.com/0EmAI26.png)

[tiny Missing Image]:(https://i.imgur.com/zDgtWUj.png)
