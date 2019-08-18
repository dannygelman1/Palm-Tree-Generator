#willowScript.py
import maya.cmds as cmds
import random
import functools
import math


def createUI(pWindowTitle, pApplyCallback):
    '''
    This is a function that creates the user interface, where users can input the x and z coordinate range
    where they want grass to generate, the number of blades to generate, and how tall on average they want 
    their grass to be
    '''
    
    windowID = 'Grass'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    #creating UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,130), (2,60), (3,60)], columnOffset = [(1,'right',3)])
    
    #creating input fields in UI window
    cmds.text(label='Width: ')
    Width = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Branch Length: ')
    Length = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Density: ')
    Density = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Leaf Length: ')
    LeafLength = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Branch Layers: ')
    BranchLayers = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Branch Angle: ')
    BranchAngle = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Trunk Height: ')
    TrunkHeight = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Trunk Cone Angle: ')
    TrunkConeAngle = cmds.intField()
    cmds.separator(h=10,style='none')
    
    
    #making the apply button call the applyCallback
    cmds.button(label='Apply', command=functools.partial(pApplyCallback, Width, Length, Density, LeafLength, BranchLayers, BranchAngle, TrunkHeight, TrunkConeAngle))
    
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()
    

def applyCallback(pWidth, pLength, pDensity, pLeafLength, pBranchLayers, pBranchAngle, pTrunkHeight, pTrunkConeAngle, *pArgs):


    Width =  cmds.intField(pWidth, query=True,value = True)
    Length =  cmds.intField(pLength, query=True,value = True)
    Density =  cmds.intField(pDensity, query=True,value = True)
    LeafLength = cmds.intField(pLeafLength, query=True,value = True)
    BranchLayers = cmds.intField(pBranchLayers, query=True,value = True)
    BranchAngle = cmds.intField(pBranchAngle, query=True,value = True)
    TrunkHeight = cmds.intField(pTrunkHeight, query=True,value = True)
    TrunkConeAngle = cmds.intField(pTrunkConeAngle, query=True,value = True)
    
    cones = cmds.polyCone(r=0.5, h=0.5, name ='cone')
    cones2 = cmds.polyCone(r=0.5, h=0.5, name ='cones2')
    cyl = cmds.polyCylinder(r=0.05, h=0.26, name ='original#')
    cylGroup = cmds.group(empty = True, name ="Group")
    cmds.move(0, -0.25, 0, "cone.scalePivot","cone.rotatePivot", absolute=True)
    cmds.scale(0.2,-LeafLength,0.01, cones)
    cmds.scale(0.2,0.4,0.01, cones2)
    cmds.move(0,0.15,0, cones)
    leafGroup = cmds.group(empty = True, name ="leafGroup")
    cmds.move(0, 0.1, 0, "leafGroup.scalePivot","leafGroup.rotatePivot", absolute=True)
    cmds.parent(cones, leafGroup)
    cmds.parent(cones2, leafGroup)
    coneGroup = cmds.group(empty = True, name ="Group")
    
    tapperLeaf = 0.9
    for i in range(0, Length):
         resInstance = cmds.instance(leafGroup, name = 'instance#')
         resInstance2 = cmds.instance(leafGroup, name = 'instance#')
         cmds.move(0, -(1.0/Width)*((0.2*float(i))**2), 0.2*float(i), resInstance)
         cmds.rotate(-40, 0, -50, resInstance)
         cmds.move(0, -(1.0/Width)*((0.2*float(i+0.5))**2), 0.2*float(i+0.5), resInstance2)
         cmds.rotate(-40, 0, 50, resInstance2)
         if i > (Length - Length/2.0):
             cmds.scale(1, tapperLeaf, 1, resInstance)
             cmds.scale(1, tapperLeaf, 1, resInstance2)
             if i%2 == 0:
                 tapperLeaf -= 0.1
             if tapperLeaf <0.3:
                 tapperLeaf += 0.1
         cmds.parent(resInstance, coneGroup) 
         cmds.parent(resInstance2, coneGroup) 
    cmds.delete(leafGroup)
    
    tapper = 0.9
    for j in range(0, 2*Length):
        resInstance3 = cmds.instance(cyl, name = 'instance#')
        cmds.move(0, -(1.0/Width)*((0.1*float(j))**2)+0.05, 0.1*float(j)+0.1, resInstance3)
        
        derivative = -(2.0/Width)*(0.1*float(j))
        angleRadDer = math.atan(derivative)
        angleDegDer = ((angleRadDer)*180.0)/3.14159
        cmds.rotate(90-angleDegDer, 0, 0, resInstance3)
        if j>(2*Length-5):
            cmds.scale(tapper,1,tapper,resInstance3)
            tapper -=0.1
        cmds.parent(resInstance3, cylGroup) 
    cmds.delete(cyl)
    
    branchGroup = cmds.group(empty = True, name ="branchGroup")
    cmds.parent(cylGroup, branchGroup) 
    cmds.parent(coneGroup, branchGroup) 
    #cmds.move(-0.27, 0.35, 0, "branchGroup.scalePivot","branchGroup.rotatePivot", absolute=True)
    
    #cmds.rotate(-45, 0, 0, branchGroup)
    allBranchGroup = cmds.group(empty = True, name ="allbranchGroup")
    for k in range(0, Density):
         angle = -BranchAngle
         for c in range(0, BranchLayers):
             groupInstance = cmds.instance(branchGroup, name = 'groupinstance#')
             cmds.rotate(angle, (360/Density)*k+(30*c), 0, groupInstance)
             cmds.parent(groupInstance, allBranchGroup)
             if angle > (-120):
                 angle -= 90.0/BranchLayers
         #groupInstance = cmds.instance(branchGroup, name = 'groupinstance#')
         #cmds.rotate(-45, (360/Density)*k, 0, groupInstance)
         #groupInstance2 = cmds.instance(branchGroup, name = 'groupinstance#')
         #cmds.rotate(-70, (360/Density)*k + 30, 0, groupInstance2)
         #groupInstance3 = cmds.instance(branchGroup, name = 'groupinstance#')
         #cmds.rotate(-10, (360/Density)*k + 60, 0, groupInstance3)
         #cmds.parent(groupInstance, allBranchGroup)
         #cmds.parent(groupInstance2, allBranchGroup)
         #cmds.parent(groupInstance3, allBranchGroup)
    cmds.delete(branchGroup)
    
    trunk = cmds.polyCylinder(r=0.2, h=TrunkHeight, name ='trunk')
    cmds.move(0,TrunkHeight/2.0,0, trunk)
    cmds.move(0,TrunkHeight,0, allBranchGroup)
    trunkCones = cmds.polyCone(r=0.3, h=0.5, name ='trunkCones')
    cmds.scale(0.7,1, 0.7, trunkCones)
    
    
    cmds.move(0,0.25, 0, trunkCones)
    cmds.move(0, 0, 0, "trunkCones.scalePivot", "trunkCones.rotatePivot", absolute=True)#
    #cmds.rotate(45, 0, 0, trunkCones)
    #cmds.rotate(50, 0, 0, trunkCones)
    
    trunkConesGroup = cmds.group(empty = True, name ="trunkConesGroup")
    for a in range(0, 4):
        trunkConeInstance = cmds.instance(trunkCones, name = 'trunkconeinstance#')
        cmds.rotate(TrunkConeAngle, 0, (360/3)*a, trunkConeInstance)
        cmds.parent(trunkConeInstance, trunkConesGroup)
    cmds.delete(trunkCones)
    cmds.rotate(-90, 0 , 0, trunkConesGroup)
    cmds.move(0, -0.25, 0, trunkConesGroup)
    
    fullTrunk = cmds.group(empty = True, name ="fullTrunk")
    for b in range(0, int(7*TrunkHeight)):
        trunkConeGroupInstance = cmds.instance(trunkConesGroup, name = 'trunkConeGroupInstance#')
        cmds.move(0,0.15*b,0, trunkConeGroupInstance)
        if b%2== 0:
            cmds.rotate(-90, 60, 0, trunkConeGroupInstance)
        if b< (6.4*TrunkHeight)/2.0:
            cmds.select( trunkConeGroupInstance[0], r=True)
            scaleFactor = ((7*TrunkHeight)-b)*(2.0/(7*TrunkHeight))
            cmds.scale(scaleFactor, scaleFactor, scaleFactor,trunkConeGroupInstance)
        cmds.parent(trunkConeGroupInstance, fullTrunk)
    cmds.delete(trunkConesGroup)
    
createUI('palm tree', applyCallback)
    
