#!/usr/bin/env python
# -*- coding: utf-8 -*-


# to add elements like Node or objects
import Sofa
import os
import numpy as np
import math

class FingerController(Sofa.PythonScriptController):


    def initGraph(self, node):

        self.node = node
        self.finger1Node=self.node.getChild('finger')
        self.pressureConstraint1Node = self.finger1Node.getChild('cavity')
        self.MecaObject1=self.finger1Node.getObject('tetras')
        self.Positions = self.MecaObject1.findData('position').value


        self.minimum = 0
        self.max = 0
        self.posmax = 0
        self.posmin = 0 

##  MINIMUM SEARCHING

        for i in range(0, len(self.Positions)):
            if self.Positions[i][2] >= self.minimum :
                self.minimum = self.Positions[i][2]
                self.posmin = i

## MAXIMUM SEARCHING 
        for j in range(0, len(self.Positions)):
            if self.Positions[j][2] <= self.max :
                self.max = self.Positions[j][2]
                self.posmax = j



        self.coeff = (self.Positions[self.posmax][2]-self.Positions[self.posmin][2])/(self.Positions[self.posmax][0]-self.Positions[self.posmin][0])
        self.angle = (math.atan(self.coeff))*180/math.pi


        print(str(self.Positions[self.posmin][2])+ ' ' + str(self.Positions[self.posmax][2])+' '+str(self.angle)+'\n')


        #file1 = open("/home/pasquale/Script_Sofa/Thick_finger/plot/Position1.txt","w")
        #file1.write(str(self.time)+' '+str(self.Positions[self.posmax][0])+ ' ' + str(self.Positions[self.posmax][1])+ ' '+ str(self.Positions[self.posmax][2]) + '\n' )
        #file1.close()        


        #file2 = open("/home/pasquale/Script_Sofa/Thick_finger/plot/Pressure-Angle1.txt","w")
        #file2.write(str(self.time)+' '+str(pressure)+ ' ' + str(angle) + '\n' )
        #file2.close()


    def onAnimateBeginEvent(self, event):

        a = self.finger.tetras.position.value 
        incr = self.dt*1000.0;

        self.MecaObject1=self.finger1Node.getObject('tetras')

        self.pressureConstraint1 = self.pressureConstraint1Node.get('SurfacePressureConstraint')

            
        pressureValue = self.pressureConstraint1.get('value')[0][0] + 5e-6

        if pressureValue > 0.0483:
            pressureValue = 0.0483

        self.pressureConstraint1.findData('value').value = str(pressureValue)
        print(pressureValue)

        return 0
           