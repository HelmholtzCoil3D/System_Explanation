'''
This script calculates the current necessary to get a field range set by the 
user. The currents are calculated to generate a range from lowerFieldLimit to 
upperFieldLimit with fieldResolution steps. It also saves the data in a 
csv file to be read later.

@author: Tarcis Becher
'''

#%% Imports

import numpy as np
from time import sleep
import csv
from auxLib import  rotationMatrixCalculator, storeDataObj, writeDataOnFile, CurrentCalculatorObj, setField, startupCoilsPolarity, closeFile, closeSerialObj, createAndOpenFile, WhatTimeIsIt, makeDir, createSerialObj, COMdetect, changeCoilPolarity, measurementNtransformation, setPowerSupplyChVoltage, setPowerSupplyAllChVoltage, setPowerSupplyAllChCurrent, setupMCU, closingPowerSupplyChannel, startUpPowerSupply, getMeasurement, setPowerSupplyChCurrent

# To show numbers in console in the raw representation
np.set_printoptions(suppress=True)

try:
#%% User code
    
    # Setup information to the microcontroller, must be in binary format "b'information'"
    samplesPerMean = b'30'
    timeBetweenSamples = b'300'
    
    # information for closedloop processing
    samplingTime = 0.1
    gain = 4
    
    # File name and folder to be created and store the data
    fileDir = "./csvData/"
    fileName = '85to135Re0-5'
    
    # Diferent ways of calculating field (not implemented yet)
    pattern = 'straight'
    #pattern = 'Circular'
    
    # Magnetic field in uT
    lowerFieldLimit = -150
    upperFieldLimit = 150
    fieldResolution = 0.5
    
#%% Start up code 
    
    # calculates the steps
    steps = round((upperFieldLimit - lowerFieldLimit)/fieldResolution) + 1
    
    # Teorethical values for field/current ration
    xTeo = 0.5
    yTeo = 2.5
    zTeo = 0.5
    
    # opening MCU comunication
    COM = COMdetect()
    serialObj = createSerialObj(COM)
    
    # Opening the MCU comunication channel
    setupMCU(serialObj, samplesPerMean, timeBetweenSamples)
    sleep(0.1)
    startupCoilsPolarity(serialObj)
    
    # Opening PS comunication channel
    resource_name = 'USB0::0x1AB1::0x0E11::DP8A203800261::0::INSTR'   
    
    # specific for this dp800, you can find to another using
    '''
    rm = visa.ResourceManager() # To connect the wraper to the USB driver
    print(rm.list_resources_info()) # to take the resource name
    '''
    
    # Creating VISA objects
    rm, dp800 = startUpPowerSupply(resource_name)


#%% Rotation matrix
    
    # calculating the rotation matrix and the relationship of current and field
    rotationMatrix, CurrentToField, FieldToCurrent, er = rotationMatrixCalculator(dp800, serialObj, [xTeo,yTeo,zTeo])
    
    # diference about practical and theoretical values
    print("field/current ration error (%) for each coil")
    print(er)
    
#%% Setup of current manangers
    
    # Data for the zero field reference
    fData = getMeasurement(serialObj)
    zeroField = np.matmul(rotationMatrix, fData)
    
    # Creates the current calculator object that calculates the current in openloop 
    coilCurrentCalculatorObj = [(CurrentCalculatorObj(i+1, zeroField[i], FieldToCurrent[i], CurrentToField[i])) for i in range(0,3)]
    
#%% Setting the desired field
    
    # Creating the csv data manager
    dataManager = storeDataObj(rotationMatrix)
    
    # Calculates the currents for zero field and stores it on the csv file
    for i in range(2,-1,-1):
        fieldMeasurement, current, control = setField(dp800, serialObj, coilCurrentCalculatorObj[i], samplingTime*gain, float(0), rotationMatrix)
        dataManager.storeData(fieldMeasurement, current, i+1,zeroField[i], control)
        
    print("zeroField :\n"+str(zeroField))
    print("fieldMeasurement : \n"+str(fieldMeasurement))
    #-----------
    
    if pattern == 'straight':
        # Creates the linspace for each field value to be calculated (only in the channel 2, index 1)
        innerCoilFieldVector = np.linspace(lowerFieldLimit, upperFieldLimit, steps)    
        
        # loop of the current calculating in closed-loop and storage
        for j in range(0, len(innerCoilFieldVector)):
            
            # Calculation and storage
            fieldMeasurement, current, control = setField(dp800, serialObj, coilCurrentCalculatorObj[1], samplingTime*gain, float(innerCoilFieldVector[j]), rotationMatrix, breakCondition = float(innerCoilFieldVector[j]/500), maxIterations = 40)
            dataManager.storeData(fieldMeasurement, current, 2,zeroField[1], control)
            
            # Field value found by the closed-loop
            print("fieldMeasurement : \n"+str(fieldMeasurement))
            
            # Error of the found value and the desired value
            if (innerCoilFieldVector[j] != 0):
                fieldError = np.linalg.norm((fieldMeasurement[1] - innerCoilFieldVector[j])/innerCoilFieldVector[j])*100
            else:
                fieldError = float('inf')
                
            print("error (%) between desired and achieved field: \n"+str(fieldError))
            
    '''
    # not well implemented yet
    elif pattern == 'Circular':
        radius = 200
        size = 200
        teta = np.linspace(0,2*np.pi,size)
        innerCoilFieldVector = np.sin(teta)*radius
        midCoilFieldVector = np.cos(teta)*radius
        
        for j in range(0, len(innerCoilFieldVector)):
            # Send the command to set the current

            fieldMeasurement, current, control = setField(dp800, serialObj, coilCurrentCalculatorObj[1], samplingTime*gain, float(innerCoilFieldVector[j]), rotationMatrix, breakCondition = 1, maxIterations = 40)
            fieldMeasurement2, current2, control2 = setField(dp800, serialObj, coilCurrentCalculatorObj[2], samplingTime*gain, float(midCoilFieldVector[j]), rotationMatrix, breakCondition = 1, maxIterations = 40)
            
            dataManager.storeData(fieldMeasurement, current, 2,zeroField[1], control)
            dataManager.storeData(fieldMeasurement2, current2, 3,zeroField[2], control2)
            
            print("fieldMeasurement : \n"+str(fieldMeasurement))
         
    
    else:
        print("Please choose a existing parttern")
    #------------
    '''  
    
    # Storing the data in the csv file
    dataManager.createCSVfile(fileDir, fileName)
    
    # Closing the resources and file
    closeSerialObj(serialObj)
    closingPowerSupplyChannel(dp800, rm)

#%% If errors occur in the process    
except Exception as error:

    print(error)
    # Closing the resources and file 
    closeSerialObj(serialObj)
    closingPowerSupplyChannel(dp800, rm)
    