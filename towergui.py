import maya.cmds as cmds
import random

def pyramidTower(floors, w, d, h):
    towerParts=[]
    for i in range(0, floors):
        story=cmds.polyCube(name='pytFloor', width=w, depth=d, height=h)
        cmds.xform(translation=[0, h/2+h*i, 0], scale=[0.8**i, 1, 0.8**i], relative=True)
        towerParts.append(story[0])
    
    cmds.group(em=True, name='pyramidTower')
    for i in towerParts:
        cmds.parent(i, 'pyramidTower')
        


def pyTduplicates(number, minX, maxX, minZ, maxZ):
    builtUp=[]
    builtUp.append('pyramidTower')
    for i in range(0, number):
        clone=cmds.duplicate('pyramidTower', smartTransform=smart)
        builtUp.append(clone[0])
    cmds.group(em=True, name='pyTowers')
    for i in builtUp:
        cmds.parent(i, 'pyTowers')
        cmds.xform(scale=[random.uniform(0.5, 2.0), random.uniform(0.5, 2.0), random.uniform(0.5, 2.0)]) 
        
    for i in range(0, len(builtUp)/4):
        cmds.move(-random.randint(minX, maxX), 0, -random.randint(minZ, maxZ), builtUp[i], r=False)
    for i in range(len(builtUp)/4, len(builtUp)/2):
        cmds.move(-random.randint(minX, maxX), 0, random.randint(minZ, maxZ), builtUp[i], r=False)
    for i in range(len(builtUp)/2, 3*len(builtUp)/4):
        cmds.move(random.randint(minX, maxX), 0, random.randint(minZ, maxZ), builtUp[i], r=False)
    for i in range(3*len(builtUp)/4, len(builtUp)):
        cmds.move(random.randint(minX, maxX), 0, -random.randint(minZ, maxZ), builtUp[i], r=False)


def gui():
    houseGen = cmds.window( title='City Generator', iconName='City Generator', widthHeight=(800, 800) )
    cmds.columnLayout( adjustableColumn=True, rowSpacing=30, columnWidth=250)
    cmds.text('Create Pyramid Towers for Inner City Area') 
    
    global pyTFloors
    pyTFloors = cmds.intSliderGrp('intSlider_pyTFloors', label = 'Number of Floors', field=True, minValue=1, maxValue=50)
    
    global pyTWidth
    pyTWidth = cmds.floatSliderGrp('floatSlider_pyTWidth', label = 'Width of Floor', field=True, minValue=1.0, maxValue=50.0)
    
    global pyTDepth
    pyTDepth = cmds.floatSliderGrp('floatSlider_pyTDepth', label = 'Depth of Floors', field=True, minValue=1.0, maxValue=50.0)
    
    global pyTHeight
    pyTHeight = cmds.floatSliderGrp('floatSlider_pyTHeight', label = 'Height of Floors', field=True, minValue=1.0, maxValue=50.0)
       
    cmds.button(label='Create Pyramid Tower', command='pyramidTower(cmds.intSliderGrp(pyTFloors, query=True, value=True), cmds.floatSliderGrp(pyTWidth, query=True, value=True), cmds.floatSliderGrp(pyTDepth, query=True, value=True), cmds.floatSliderGrp(pyTHeight, query=True, value=True))')    
    
    global pyTduplicates
    pyTduplicates = cmds.intSliderGrp('intSlider_pyTduplicates', label = 'Number of Towers', field=True, minValue=1, maxValue=200) 
        
    global pyTduplicatesMinX
    pyTduplicatesMinX = cmds.floatSliderGrp('floatSlider_pyTduplicatesMinX', label='Minimum X Direction', field=True, minValue=-500.0, maxValue=0, value=1)
    
    global pyTduplicatesMaxX
    pyTduplicatesMaxX = cmds.floatSliderGrp('floatSlider_pyTduplicatesMaxX', label='Maximum X Direction', field=True, minValue=0, maxValue=500.0, value=1)   

    global pyTduplicatesMinZ
    pyTduplicatesMinZ = cmds.floatSliderGrp('floatSlider_pyTduplicatesMinZ', label='Minimum Z Direction', field=True, minValue=-500.0, maxValue=0, value=1)

    global pyTduplicatesMaxZ
    pyTduplicatesMaxZ = cmds.floatSliderGrp('floatSlider_pyTduplicatesMaxZ', label='Maximum Z Direction', field=True, minValue=0, maxValue=500.0, value=1)
    
    cmds.button(label='Scatter Towers', command='pyTduplicates(cmds.intSliderGrp(pyTduplicates, query=True, value=True), cmds.floatSliderGrp(pyTduplicatesMinX, query=True, value=True),cmds.floatSliderGrp(pyTduplicatesMaxX, query=True, value=True),cmds.floatSliderGrp(pyTduplicatesMinZ, query=True, value=True),cmds.floatSliderGrp(pyTduplicatesMaxZ, query=True, value=True))') 
    
    cmds.showWindow(houseGen)


gui()
