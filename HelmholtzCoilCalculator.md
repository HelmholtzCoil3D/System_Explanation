# 3D Helmholtz coil simulations

Here there's a python script integrated to a custom library that calculates the necessary measures to construct a 3D helmholtz coil with desired parameters.

for example the setting parameters:

```python
# ----------------------------------------------------------#
# 1 2 3 4 5 6 -> LoopsInEachEvenLayer = 6                   #
#|-----------|                                              #
#|0 0 0 0 0 0| even                                    |0 ..#
#| 0 0 0 0 0 | odd                                     |    #
#|0 0 0 0 0 0| even (always start with even layer)     |0 ..#
#|-----------|                 ...                     |----#
#            V                                         V    #
#           edge                                      edge  #
# *cross-cut of the windings where each "0" is a winding    #
#-----------------------------------------------------------#

# have to use wireExternalDiameter*1.1
AllCoilsWireDiameter = (0.56 + 0.047)*1.1   # Wire diameter in mm (from dataSheet)

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
Results in the console:

![](https://i.imgur.com/TJTAAUR.png)\
**\* The distance between coils must be from edge to edge, not center to center (diameter/2)**

Coil in Z direction results:

![](https://i.imgur.com/mBnbwau.png)
![](https://i.imgur.com/lYC8y8B.png)

Coil in Y direction results:

![](https://i.imgur.com/Oxp6UT9.png)
![](https://i.imgur.com/3rvZ79g.png)

Coil in X direction results:

![](https://i.imgur.com/Xb9SszS.png)
![](https://i.imgur.com/I9bfdnk.png)

The three coils together:

![](https://i.imgur.com/eHWeNZj.png)