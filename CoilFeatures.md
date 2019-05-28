
```python
# -*- coding: utf-8 -*-

import numpy as np

theoreticalValue = [1250, 250, 250]

initialInner = [[12.75, 12.82, 12.88],[19.57, 19.55, 19.54],[48.76, 48.71, 48.74]]
initialMiddle = [[13.09, 12.77, 12.76],[19.76, 19.82, 19.80],[48.77, 48.76, 48.71]]
initialExternal = [[12.39, 12.40],[18.77, 18.79],[48.27, 48.34]]

finallInner = [[-1223.72, -1223.54, -1223.68],[16.45, 16.44, 16.44],[48.69, 48.68, 48.74]]
finalMiddle = [[7.86, 7.82, 7.82],[-230.55, -230.53, -230.47],[50.31, 50.33, 50.29]]
finalExternal = [[11.32, 11.57, 11.51],[15.59, 15.45, 15.43],[-205.35,-205.28,-205.38 ]]

for i in range(0,3):
    initialInner[i] = np.mean(initialInner[i])
    initialMiddle[i] = np.mean(initialMiddle[i])
    initialExternal[i] = np.mean(initialMiddle[i])

for i in range(0,3):
    finallInner[i] = np.mean(finallInner[i])
    finalMiddle[i] = np.mean(finalMiddle[i])
    finalExternal[i] = np.mean(finalExternal[i])
    
fieldInner = [0,0,0]
fieldMiddle = [0,0,0]
fieldExternal = [0,0,0]

for i in range(0,3):
    fieldInner[i] = finallInner[i] - initialInner[i]
    fieldMiddle[i] = finalMiddle[i] - initialMiddle[i]
    fieldExternal[i] = finalExternal[i] - initialExternal[i]

print('Field on inner coil with 500 mA')
print(fieldInner)

print('\nField on middle coil with 500 mA')
print(fieldMiddle)

print('\nField on external coil with 500 mA')
print(fieldExternal)

print('\nNorm of the fields:')
print(np.linalg.norm(fieldInner))
print(np.linalg.norm(fieldMiddle))
print(np.linalg.norm(fieldExternal))

print('\nError from theoretical values')
print(str((np.linalg.norm(fieldInner) - theoreticalValue[0])/theoreticalValue[0]*100) + ' %')
print(str((np.linalg.norm(fieldMiddle) - theoreticalValue[1])/theoreticalValue[1]*100) + ' %')
print(str((np.linalg.norm(fieldExternal) - theoreticalValue[2])/theoreticalValue[2]*100) + ' %')

