# 3D Helmholtz coil system

## Objective of the project

This project aim is to prototype some kind of system control it automaticaly and make some fields setups in static applications.

The idea behind this project is to create a homogeneous field in some defined region where magnetic samples can be tested with a totaly known field

<p align="center">
  <img src="https://i.imgur.com/ytuayWB.png/">
</p>

<p align="center">
  <img src="https://i.imgur.com/5vaQXRf.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/cQSHDOd.png">
</p>

The desired features in this case would be a region with errors bellow 1%, the maximium difference of the magnetic field strenght in two different points and angles with less than 1° of difference between two different points of the homogeneous region. A magnetic flux density range of 1 uT to 1 mT is desired in this region.

The region defined for the prototype at first is a 20 mm³ region

**The system itself just generate the field**, the magnetic sample must have its own system to generate the data for posterior analysis. Analisys can be made based in the known direction and amplitude of the homogeneous region magnetic field.

## Base Knowledge

To create a homogeneous field in some free space region, the concept used was the [Helmholtz coil] that can create a homogeneous field inward from the coils to the geometric center of the estructure, the more in the center, the more homogeneous the field is.

Exitating the coils with a known current generates a known [magnetic field] (H) that is related to the magnetic flux density (B) by the permeability ($\mu$) of the material, in this case the air ([1.00000037])

The B can [saturate] depending on the material, in this case it will not happen so there are no linearity problems

Knowing that the magnetic field will be linear, so a 3 axis Helmholtz coil can be design to generate the arbitrary homogeneous magnetic field, remembering that this system must compensate the [earth magnetic field]

##  Blocks diagram

The system blocks diagram can be represented as follows:

![](https://i.imgur.com/3Lv7iL5.png)

The main parts of the system:
-   Helmholtz coils to generate the field
-   Controller to control the generated field throught magnetic sensors readings
-   Interface to give properly the user commands to the controller

## Helmholtz coils design

To design the needed helmholtz coils, an open source python library was used, [magpylib], this library is capable to calculate magnetic field of permanent magnets and current lines or circles.

In fact the application is static, so the helmholtz can projected as current loops placed in a helmholtz coil shape.

<p align="center">
  <img src="https://i.imgur.com/Wa3sqmD.png">
</p>

 From the cross-cut section the parameters for the coils calculation can be extracted as the following figure:

<p align="center">
  <img src="https://i.imgur.com/2rMNDIl.png">
</p>





[magpylib]:https://github.com/magpylib/magpylib

[Helmholtz coil]:https://en.wikipedia.org/wiki/Helmholtz_coil

[magnetic field]:https://en.wikipedia.org/wiki/Magnetic_field

[earth magnetic field]:https://en.wikipedia.org/wiki/Earth%27s_magnetic_field

[1.00000037]:https://en.wikipedia.org/wiki/Permeability_(electromagnetism)

[saturate]:https://en.wikipedia.org/wiki/Saturation_(magnetic)