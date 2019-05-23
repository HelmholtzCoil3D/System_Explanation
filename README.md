# 3D Helmholtz coil system
[TOC]
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
-   Controller to control the generated field throught magnetic sensors readings
-   Interface to give properly the user commands to the controller

# Helmholtz coils design

## Simulator

To design the needed helmholtz coils, an open source python library was used, [magpylib], this library is capable to calculate magnetic field of permanent magnets and current lines or circles.

In fact the application is static, so the helmholtz can projected as current loops placed in a helmholtz coil shape.

<p align="center">
  <img src="https://i.imgur.com/Wa3sqmD.png">
</p>

 From the cross-cut section the parameters for the coils calculation can be extracted as the following figure:

<p align="center">
  <img src="https://i.imgur.com/ME0H3qo.png">
</p>

The details about the calculator can be seen in the [Helmholtz coil calculator] and [Auxiliar library] files. Giving some parameters to the calculator, it gives us the necessary coil diameter to achieve the desired field in the center of the coil and graphics that shows the field strenght in the 3 vectors of the field separeted (x,y,z) and from this an analysis can be made to determine the homogenity of the field generated by each coil, amplitude and angle error relative to the center in the desired homogeneous region. Following an example for the z axis coil.

Input parameters
# CHANGE THIS PART
#------------------------------------------------------------
``` python
# have to use a little bit bigger value than wireExternalDiameter, if not, the wire will not fit inside
AllCoilsWireDiameter = (0.56 + 0.047)*1.09   # Wire diameter in mm (from dataSheet - https://at.rs-online.com/web/p/kupferdrahte/0357750/)

minRes = 0.06736                            # Ohms/m (from dataSheet)
nominal = 0.06940                           # Ohms/m (from dataSheet)
maxRes = 0.07153                            # Ohms/m (from dataSheet)

wireResistence = maxRes                     # Ohms/m (from dataSheet)

zInitialValueCoilDiameter = 80 # Initial value for the function that calculates the precise diameter

zCoilCurrent = 0.5             # Amperes
zLoopsInEachEvenLayer = 10     # The number of loops in each layer
zEvenLayers = 7                # The evenlayers always have to be equal to oddLayers or oddLayers + 1
zOddLayers = 7
zDesiredField = 1.25           # The desired field in the center of the Helmholtz coil
```
Console results

![](https://i.imgur.com/1mMmFIL.png)

Graphic Results

<p align="center">
  <img src="https://i.imgur.com/QWl2P50.png">
  <img src="https://i.imgur.com/fIQKE3O.png">
</p>
#------------------------------------------------------------
### Simulator results

Wire External Diameter = 0.6 mm 

|Coils| Radius | Coil Width| Coil Height|
|:-:|-|-|-|
| Inner | 42.5 mm | 6.6 mm| 9.65 mm |
| Middle | 56.15 mm | 4 mm| 5.5 mm |
| External | 66.5 mm | 4.65 mm| 5.5 mm |
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

<details>
<summary> If you are viewing it in the repository</summary>

All the files for the 3DModelFiles folder in this repository

</details>

This model perfectly fits inside the coils support model, using the internal part to support the sensor of the system and the more external pegs and holes to support the sample. Notice that the external support is designed in such a way that the sample stays in the middle of the coils. If the sample change, the user can design another 3D model for the support to adapt the coil usage to an especific application

### Pegs 3D model

To attach the PCB support to the coils support some pegs was designed with diferent diameters, using the fact that the printer has more precision than $\pm$1 $\mu$m:

<p align="center">
  <img src="https://i.imgur.com/ucujuqK.png">
  <img src="https://i.imgur.com/xfdn5YZ.png">
</p>

Using 50 $\mu$m of difference between the pegs, will make it safe to fit in the previous models holes, testing which diameter is beter to use.

## 3D Print results

The company have its own 3D printers, one with really high resolutions for tiny parts and another with less resolution but with more space to print. The material is not so rigid in the high resolution printer and the prints have problems in the pos-printing process that causes some bendding problems, so for the coils support the print was made by [Reprap] Austria, that was more cheap and perfect printed than with the company printer. For the other models, the company printer was enought to do the job.

The Reprap Austria 3D printer size limit is **32**x**36**x**42** **cm**, been the largest coil external diameter around 15 cm, the printing size is fairly ok and if the company needs a bigger coil with different especification, it can be printed.

The Coils support was ordered and the result can be seen:
<details>
<summary> <b>Click here to see the Coil support print result</b> </summary>
<p align="center">
  <img src="https://i.imgur.com/snpOLTE.gif">
</p>

**There's a sensor support inside of the coils printed with the company printer, that fitted really nice inside**
</details>

The Sensor/Sample support and pegs were printed in the CTR high resolution printer:

<p align="center">
  <img src="https://i.imgur.com/pbrw9hg.png">
  
  <img src="https://i.imgur.com/d36SHwn.png">
  
  <img src="https://i.imgur.com/iP3jZjX.png">
</p>

Printed pegs:

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

## Coils winding

After doing the windings really carefull, maintaining the [wire] stretched while doing each turn, it helped to get the wire really fit in the coils support. The arrangement to stretch the wire can be seen in the next image, its an improvised tool that makes some pressure in the reel, extremely important to make the coils the most near to the simulation position of the wires.

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

 The [hot glue] was used to mantain the cables fixed in the coils suppor, the result of the 3 axis coil can be seen in the following image:

<p align="center">
  <img src="https://i.imgur.com/QoLNiNV.png">
</p>

Each of the six coils was done individualy, doing the inside coils first, and then connected with a solder point with the respective pair (2 coils in X direction to form the X helmholtz coil for example). The following image shows the connection between 2 coils:

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

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

Mesured resistence, inductance:

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png"> 
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
  <img src="https://i.imgur.com/zDgtWUj.png">  
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
  <img src="https://i.imgur.com/zDgtWUj.png"> 
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
  <img src="https://i.imgur.com/zDgtWUj.png">  
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
  <img src="https://i.imgur.com/zDgtWUj.png"> 
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

The mesured field with the 500 mA (powersupply and sensor image):

<p align="center">
  <img src="https://i.imgur.com/zDgtWUj.png">  
  <img src="https://i.imgur.com/zDgtWUj.png">  
</p>

# Magnetic sensor



# Controller

## Current controller
## Polaraty controller
## Sensor controller

## Power Supply

## H-bridges

## MCU


# Interface

# Integration




[Helmholtz coil calculator]:HelmholtzCoilCalculator.md

[Auxiliar library]:magpylibUtils.md

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

![Missing Image](https://i.imgur.com/0EmAI26.png)

![tiny Missing Image](https://i.imgur.com/zDgtWUj.png)