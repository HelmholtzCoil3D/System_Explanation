# -*- coding: utf-8 -*-
"""
This is a template that simulate a 3D helmholtz coil
in field amplitude and angle, it shows the 3D model of the 3D Coil

Author: Tarcis Becher
"""
#%% imports
import numpy as np
from numpy import pi
import magpylib as magpy
from magpylibUtils import helmholtzCoil,plotBxyz, constructAccess, desiredCoilDiameter

np.set_printoptions(suppress=True)

#%% Configuration of the coils

# via datasheet AWG23 https://docs-emea.rs-online.com/webdocs/157f/0900766b8157f396.pdf

# ----------------------------------------------------------#
# 1 2 3 4 5 6 -> LoopsInEachEvenLayer = 6                   #
#|-----------|                                              #
#|0 0 0 0 0 0| even                                         #
#| 0 0 0 0 0 | odd                                          #
#|0 0 0 0 0 0| even (always start with even layer)          #
#|-----------|                                              #
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
zColor = 'k'

# y Second Coil configuration

yCoilCurrent = 0.5             # Amperes
yLoopsInEachEvenLayer = 6      # The number of loops in each layer
yEvenLayers = 3                # The evenlayers always have to be oddLayers + 1 or equal oddLayers
yOddLayers = 3
yDesiredField = 0.25           # The desired field in the center of the Helmholtz coil
yColor = 'k'

# x Third Coil configuration

xCoilCurrent = 0.5             # Amperes
xLoopsInEachEvenLayer = 7      # The number of loops in each layer
xEvenLayers = 3                # The evenlayers always have to be oddLayers + 1 or equal oddLayers
xOddLayers = 3
xDesiredField = 0.25           # The desired field in the center of the Helmholtz coil
xColor = 'k'

ZDESIGN = True
YDESIGN = True
XDESIGN = True

ZCOILPLOT = True
ZCOILSCONNECTORPLOT = False
YCOILPLOT = True
YCOILSCONNECTORPLOT = False
XCOILPLOT = True
XCOILSCONNECTORPLOT = False
DISPSYS = True

# zAxisFirstCoil - The collection with the first coil in the 'z' orientation
# yAxisSecondCoil - The collection with the second coil in the 'y' orientation
# xAxisThirdCoil - The collection with the second coil in the 'x' orientation
# connectorsCollection - The collection with all the access together
# zyxCoil - The collection with the coils all together
# zyxCoilandAcess - The collection with the entire system

# some setup for desiredCoilDiameter function
nIteration = 100
relativeDistance = 0.33333

# --------------------------------------------------------------------------
#%% DESIGN OF THE MAIN AXIS HELMHOLTZ COIL ('z') -----------------------------------------------------------------------------------------------
if ZDESIGN:
    # Setting input values -------------------------------------------------------------------------------------------------------------------------
   
    orientation = 'z'                                                           # The final coil orientation
    
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Finding the right coil internal diameter to have the desired field with the zCoilCurrent in A
    zCoilIntDiameter = desiredCoilDiameter(nIteration = nIteration, 
                                          breakCondition = zDesiredField/10000, 
                                          initialValue = zInitialValueCoilDiameter,
                                          desiredField = zDesiredField, 
                                          I = zCoilCurrent, 
                                          coilIntDiameter = zInitialValueCoilDiameter, 
                                          wireDiameter=AllCoilsWireDiameter, 
                                          loopsInEachEvenLayer=zLoopsInEachEvenLayer, 
                                          evenLayers=zEvenLayers, oddLayers=zOddLayers, 
                                          orientation=orientation,
                                          relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    print('For the ',zDesiredField ,' mT field you must use the internal diameter = ',zCoilIntDiameter,' mm')
    
    # Constructing the desired coil ---------------------------------------------------------------
    zAxisFirstCoil = helmholtzCoil(color = zColor,I = zCoilCurrent, 
                                   coilIntDiameter = zCoilIntDiameter, 
                                   wireDiameter=AllCoilsWireDiameter, 
                                   loopsInEachEvenLayer=zLoopsInEachEvenLayer, 
                                   evenLayers=zEvenLayers, oddLayers=zOddLayers, 
                                   coilsDistance=zCoilIntDiameter/2, 
                                   orientation=orientation, 
                                   relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    # Constructing the coils all together
    zyxCoil = magpy.Collection(zAxisFirstCoil)

    # Printing in the console the field value in the center of the coil
    Bcenterz = zAxisFirstCoil.getB([0,0,0])
    print("'z' orientation, B = [0,0,0] will be = ",Bcenterz," mTesla")
    #---------------------------------------------------------------------------------------------------
    
    
    # calculating the energy dissipation by joule effect --------------------------------------------------------------------------------------------
    coilExtDiameter = zCoilIntDiameter
    wireLenght = 0
    
    for i in range(0,zEvenLayers + zOddLayers):
        if (i % 2) == 0:
            wireLenght += coilExtDiameter*pi*zLoopsInEachEvenLayer
        elif (i % 2) == 1:
            wireLenght += coilExtDiameter*pi*(zLoopsInEachEvenLayer-1)
        coilExtDiameter += ((3)**(1/2))*AllCoilsWireDiameter
    
    wireLenghtMeters = 2*wireLenght/1000
    coilResistence = wireResistence*wireLenghtMeters
    coilMaxPower = coilResistence*(zCoilCurrent**2)
    
    print('Coil resistence ~= '+ str(coilResistence) +' ohms' )
    print('Coil power dissipation ~= '+ str(coilMaxPower) +' W')
    print('Wire lenght necessary to construct the coil ~= '+ str(wireLenghtMeters) +' m')
    
    # calculate the wire estimeted lengthBetweenCoils (approximated)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    # Putting the supply access to the coil ----------------------------------------------------------------------------------------------------------
    
    # Verifying the field that passes through the supply access ------------------------------------------------------------------------------------
    
    singleCoilWidth = 0
    
    connectorsCollection =  magpy.Collection()
    connectorsCollection =  constructAccess(I = zCoilCurrent, coilExtDiameter = coilExtDiameter, wireDiameter = AllCoilsWireDiameter, 
                           centralPointBetweenHelmCoils = [0,0,0], lengthBetweenCoils = zCoilIntDiameter/2, 
                           singleCoilWidth = singleCoilWidth, helmCoil = connectorsCollection, relativeDistance = relativeDistance)
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
#%% DESIGN OF THE SECOND HELMHOLTZ COIL ('y') -----------------------------------------------------------------------------------------------
if YDESIGN:

    yInitialValueCoilDiameter = coilExtDiameter
        
    orientation = 'y'                                                           # The final coil orientation
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    
    
    # Finding the right coil internal diameter to have the desired field with the zCoilCurrent in A
    yCoilIntDiameter = desiredCoilDiameter(nIteration = nIteration, 
                                          breakCondition = yDesiredField/10000, 
                                          initialValue = yInitialValueCoilDiameter,
                                          desiredField = yDesiredField, 
                                          I = yCoilCurrent, 
                                          coilIntDiameter = yInitialValueCoilDiameter, 
                                          wireDiameter=AllCoilsWireDiameter, 
                                          loopsInEachEvenLayer=yLoopsInEachEvenLayer, 
                                          evenLayers=yEvenLayers, oddLayers=yOddLayers, 
                                          orientation=orientation,
                                          relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    print('For the ',yDesiredField ,' mT field you must use the internal diameter = ',yCoilIntDiameter,' mm')
    # Constructing the desired coil ---------------------------------------------------------------
    yAxisSecondCoil = helmholtzCoil(color = yColor, I = yCoilCurrent, 
                                   coilIntDiameter = yCoilIntDiameter, 
                                   wireDiameter=AllCoilsWireDiameter, 
                                   loopsInEachEvenLayer=yLoopsInEachEvenLayer, 
                                   evenLayers=yEvenLayers, oddLayers=yOddLayers, 
                                   coilsDistance=yCoilIntDiameter/2, 
                                   orientation=orientation, 
                                   relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    # Constructing the coils all together
    zyxCoil.addSources(yAxisSecondCoil)
    
    # Printing in the console the field value in the center of the coil
    Bcentery = yAxisSecondCoil.getB([0,0,0.0001])
    print("'y' orientation, B = [0,0,0] will be = ",Bcentery," mTesla")
    #---------------------------------------------------------------------------------------------------
    
    
    # calculating the energy dissipation by joule effect --------------------------------------------------------------------------------------------
    coilExtDiameter = yCoilIntDiameter
    wireLenght = 0
    
    for i in range(0,yEvenLayers + yOddLayers):
        if (i % 2) == 0:
            wireLenght += coilExtDiameter*pi*yLoopsInEachEvenLayer
        elif (i % 2) == 1:
            wireLenght += coilExtDiameter*pi*(yLoopsInEachEvenLayer-1)
        coilExtDiameter += ((3)**(1/2))*AllCoilsWireDiameter
    
    wireLenghtMeters = 2*wireLenght/1000
    coilResistence = wireResistence*wireLenghtMeters
    coilMaxPower = coilResistence*(yCoilCurrent**2)
    
    print('Coil resistence ~= '+ str(coilResistence) +' ohms' )
    print('Coil power dissipation ~= '+ str(coilMaxPower) +' W')
    print('Wire lenght necessary to construct the coil ~= '+ str(wireLenghtMeters) +' m')
    
    connectorsCollection.rotate(90,[1,0,0],anchor=[0,0,0])
    connectorsCollection.rotate(180,[0,1,0],anchor=[0,0,0])
            
    connectorsCollection =  constructAccess(I = yCoilCurrent, coilExtDiameter = coilExtDiameter, wireDiameter = AllCoilsWireDiameter, 
                           centralPointBetweenHelmCoils = [0,0,0], lengthBetweenCoils = yCoilIntDiameter/2, 
                           singleCoilWidth = singleCoilWidth, helmCoil = connectorsCollection, relativeDistance = relativeDistance)
    
    connectorsCollection.rotate(180,[0,1,0],anchor=[0,0,0])
    connectorsCollection.rotate(-90,[1,0,0],anchor=[0,0,0])
    
# --------------------------------------------------------------------------------------------------


#%% DESIGN OF THE THIRD HELMHOLTZ COIL ('x') -----------------------------------------------------------------------------------------------
if XDESIGN:
    
    xInitialValueCoilDiameter = coilExtDiameter
    
    orientation = 'x'                                                           # The final coil orientation
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    
    # Finding the right coil internal diameter to have the desired field with the zCoilCurrent in A
    xCoilIntDiameter = desiredCoilDiameter(nIteration = nIteration, 
                                          breakCondition = xDesiredField/10000, 
                                          initialValue = xInitialValueCoilDiameter,
                                          desiredField = xDesiredField, 
                                          I = xCoilCurrent, 
                                          coilIntDiameter = xInitialValueCoilDiameter, 
                                          wireDiameter=AllCoilsWireDiameter, 
                                          loopsInEachEvenLayer=xLoopsInEachEvenLayer, 
                                          evenLayers=xEvenLayers, oddLayers=xOddLayers, 
                                          orientation=orientation,
                                          relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    print('For the ',xDesiredField ,' mT field you must use the internal diameter = ',xCoilIntDiameter,' mm')
    # Constructing the desired coil ---------------------------------------------------------------
    xAxisThirdCoil = helmholtzCoil(color = xColor, I = xCoilCurrent, 
                                   coilIntDiameter = xCoilIntDiameter, 
                                   wireDiameter=AllCoilsWireDiameter, 
                                   loopsInEachEvenLayer=xLoopsInEachEvenLayer, 
                                   evenLayers=xEvenLayers, oddLayers=xOddLayers, 
                                   coilsDistance=xCoilIntDiameter/2, 
                                   orientation=orientation,
                                   relativeDistance = relativeDistance)
    # ---------------------------------------------------------------------------------------------
    
    # Constructing the coils all together
    zyxCoil.addSources(xAxisThirdCoil)
    
    # Printing in the console the field value in the center of the coil
    Bcenterx = xAxisThirdCoil.getB([0,0,0.0001])
    print("'x' orientation, B = [0,0,0] will be = ",Bcenterx," mTesla")
    #---------------------------------------------------------------------------------------------------
    
    
    # calculating the energy dissipation by joule effect --------------------------------------------------------------------------------------------
    coilExtDiameter = xCoilIntDiameter
    wireLenght = 0
    
    for i in range(0,xEvenLayers + xOddLayers):
        if (i % 2) == 0:
            wireLenght += coilExtDiameter*pi*xLoopsInEachEvenLayer
        elif (i % 2) == 1:
            wireLenght += coilExtDiameter*pi*(xLoopsInEachEvenLayer-1)
        coilExtDiameter += ((3)**(1/2))*AllCoilsWireDiameter
    
    wireLenghtMeters = 2*wireLenght/1000
    coilResistence = wireResistence*wireLenghtMeters
    coilMaxPower = coilResistence*(yCoilCurrent**2)
    
    print('Coil resistence ~= '+ str(coilResistence) +' ohms' )
    print('Coil power dissipation ~= '+ str(coilMaxPower) +' W')
    print('Wire lenght necessary to construct the coil ~= '+ str(wireLenghtMeters) +' m')
    connectorsCollection.rotate(-90,[0,1,0],anchor=[0,0,0])
    
    connectorsCollection =  constructAccess(I = xCoilCurrent, coilExtDiameter = coilExtDiameter, wireDiameter = AllCoilsWireDiameter, 
                           centralPointBetweenHelmCoils = [0,0,0], lengthBetweenCoils = xCoilIntDiameter/2, 
                           singleCoilWidth = singleCoilWidth, helmCoil = connectorsCollection, relativeDistance = relativeDistance)
    
    connectorsCollection.rotate(90,[0,1,0],anchor=[0,0,0])
            
zyxCoilandAcess = magpy.Collection(zyxCoil)
zyxCoilandAcess.addSources(connectorsCollection)
    # ----------------------------------------------------------------------------------------------------------------------------------------------

#%%
    
if ZCOILPLOT:
    plotBxyz(collectionToPlot = zAxisFirstCoil, plotBounds = [-10,10,-10,10], orientation = 'y',  orderMagnitude = 'uT',
             fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Main coil ("+z")\ny = 0', 
             compareToCenter = True)
    if ZCOILSCONNECTORPLOT:
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'y',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Connectors field ("+z")\ny = 0', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'y',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 5, figureTittle = 'Connectors field ("+z")\ny = 5', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'y',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 10, figureTittle = 'Connectors field ("+z")\ny = 10', 
                 compareToCenter = True)
        
    zAxisFirstCoil.displaySystem()
    
    
if YCOILPLOT:
    plotBxyz(collectionToPlot = yAxisSecondCoil, plotBounds = [-10,10,-10,10], orientation = 'x',  orderMagnitude = 'uT',
             fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Second coil ("+y")\nx = 0', 
             compareToCenter = True)
    if YCOILSCONNECTORPLOT:
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'x',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Connectors field ("+y")\nx = 0', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'x',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 5, figureTittle = 'Connectors field ("+y")\nx = 5', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'x',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 10, figureTittle = 'Connectors field ("+y")\nx = 10', 
                 compareToCenter = True)
        
    yAxisSecondCoil.displaySystem()

if XCOILPLOT:
    plotBxyz(collectionToPlot = xAxisThirdCoil, plotBounds = [-10,10,-10,10], orientation = 'z',  orderMagnitude = 'uT',
             fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Third coil ("+x")\nz = 0', 
             compareToCenter = True)
    if XCOILSCONNECTORPLOT:
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'z',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 0, figureTittle = 'Connectors field ("+x")\nz = 0', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'z',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 5, figureTittle = 'Connectors field ("+x")\nz = 5', 
                 compareToCenter = True)
        plotBxyz(collectionToPlot = connectorsCollection, plotBounds = [-10,10,-10,10], orientation = 'z',  orderMagnitude = 'uT',
                 fieldDif = False, figureSize = [16,8], nPlotPoints = 10, xyz0 = 10, figureTittle = 'Connectors field ("+x")\nz = 10', 
                 compareToCenter = True)
        
    xAxisThirdCoil.displaySystem()
    
if DISPSYS:
    connectorsCollection.displaySystem()
    zyxCoil.displaySystem()
    zyxCoilandAcess.displaySystem()