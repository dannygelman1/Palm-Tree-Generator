#willowScript.py
import maya.cmds as cmds
import random
import functools
import math


#def createUI(pWindowTitle, pApplyCallback):
#    '''
#    This is a function that creates the user interface, where users can input the x and z coordinate range
#    where they want grass to generate, the number of blades to generate, and how tall on average they want 
#    their grass to be
#    '''
#    
#    windowID = 'Grass'
#    
#    if cmds.window(windowID, exists=True):
#        cmds.deleteUI(windowID)
#    #creating UI window  
#    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
#    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,130), (2,60), (3,60)], columnOffset = [(1,'right',3)])
#    
#    #creating input fields in UI window
#    cmds.text(label='Width: ')
#    Width = cmds.intField()
#    cmds.separator(h=10,style='none')
#    cmds.text(label='Length: ')
#    Length = cmds.intField()
#    cmds.separator(h=10,style='none')
#    cmds.text(label='Density: ')
#    Density = cmds.intField()
#    cmds.separator(h=10,style='none')
    
    
    #making the apply button call the applyCallback
 #   cmds.button(label='Apply', command=functools.partial(pApplyCallback, Width, Length, Density))
    
  #  def cancelCallback(*pArgs):
 #       if cmds.window(windowID, exists=True):
 #           cmds.deleteUI(windowID)
 #   cmds.button(label='Cancel', command=cancelCallback)
  #  cmds.showWindow()
    

#def applyCallback(pWidth, pLength, pDensity, *pArgs):


#Width =  cmds.intField(pWidth, query=True,value = True)
#Length =  cmds.intField(pLength, query=True,value = True)
#Density =  cmds.intField(pDensity, query=True,value = True)

cones = cmds.polyCone(r=0.5, h=0.5, name ='original#')
cones2 = cmds.polyCone(r=0.5, h=0.5, name ='original#')
cyl = cmds.polyCylinder(r=0.03, h=0.26, name ='original#')
cylGroup = cmds.group(empty = True, name ="Group")
#cmds.move(-0.27, 0.35, 0, cyl)

cmds.scale(0.2,-1,0.01, cones)
cmds.scale(0.2,0.4,0.01, cones2)
cmds.move(0,0.35,0, cones2)
leafGroup = cmds.group(empty = True, name ="leafGroup")
cmds.parent(cones, leafGroup)
cmds.parent(cones2, leafGroup)
coneGroup = cmds.group(empty = True, name ="Group")
#cmds.scale(0.3,0.3,0.3, leafGroup)

for i in range(-10, 11):
     resInstance = cmds.instance(leafGroup, name = 'instance#')
     resInstance2 = cmds.instance(leafGroup, name = 'instance#')
     # resInstance3 = cmds.instance(cyl, name = 'instance#')
     cmds.move(0, -(1.0/2.0)*((0.2*float(i))**2), 0.2*float(i), resInstance)
     #cmds.move(-0.27, -(1.0/2.0)*((0.2*float(i))**2)+ 0.35, 0.2*float(i), resInstance3)
     cmds.rotate(0, 0, 35, resInstance)
     #lower = i - 1
     # upper = i + 1
     # lowerHeight = -(1.0/2.0)*((0.2*float(lower))**2)
     # upperHeight = -(1.0/2.0)*((0.2*float(upper))**2)
     # diffHeight = upperHeight - lowerHeight
     # angleRad = math.atan(diffHeight)
     #angleDeg = (2*angleRad*180.0)/3.14159
     #cmds.rotate(90 - angleDeg, 0, 0, resInstance3
     cmds.move(-0.55, -(1.0/2.0)*((0.2*float(i+0.5))**2), 0.2*float(i+0.5), resInstance2)
     cmds.rotate(0, 0, -35, resInstance2)
     cmds.parent(resInstance, coneGroup) 
     cmds.parent(resInstance2, coneGroup) 
cmds.delete(leafGroup)

for j in range(-20, 21):
    resInstance3 = cmds.instance(cyl, name = 'instance#')
    cmds.move(-0.27, -(1.0/2.0)*((0.1*float(j))**2)+0.35, 0.1*float(j), resInstance3)
    #lower = j - 1
    #upper = j + 1
    #lowerHeight = -(1.0/2.0)*((0.1*float(lower))**2)
    #upperHeight = -(1.0/2.0)*((0.1*float(upper))**2)
    #diffHeight = upperHeight - lowerHeight
    #angleRad = math.atan(diffHeight)
    #angleDeg = (2.0*(angleRad)*180.0)/3.14159
    
    derivative = -(0.1*float(j))
    angleRadDer = math.atan(derivative)
    angleDegDer = ((angleRadDer)*180.0)/3.14159
    cmds.rotate(90-angleDegDer, 0, 0, resInstance3)
    cmds.parent(resInstance3, cylGroup) 
cmds.delete(cyl)
#groupInstance = cmds.instance(coneGroup, name = 'groupinstance#')

branchGroup = cmds.group(empty = True, name ="branchGroup")
cmds.parent(cylGroup, branchGroup) 
cmds.parent(coneGroup, branchGroup) 
#cmds.move(0, 0, 0, branchGroup)
cmds.move(-0.27, 0.35, 0, "branchGroup.scalePivot","branchGroup.rotatePivot", absolute=True)

for k in range(1, 5):
     groupInstance = cmds.instance(branchGroup, name = 'groupinstance#')
     #groupInstance2 = cmds.instance(cylGroup, name = 'groupinstance2#')
     cmds.rotate(0, (360/10)*k, 0, groupInstance)
     # cmds.rotate(0, (360/10)*k, 0, groupInstance2)
     #cmds.scale(0, -1, 0, groupInstance2)
   
#createUI ('Grass Input', applyCallback)
    
