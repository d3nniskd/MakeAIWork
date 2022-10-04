'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import time as tm # wordt gebruikt voor pauze in te lassen
import traceback as tb # wordt niet gebruikt
import math as mt # wordt niet gebruikt
import sys as ss
import os
import socket as sc

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)] # voegt zoekpaden toe

import socket_wrapper as sw
import parameters as pm

class HardcodedClient: # wordt helemaal onderaan aangeroepen
    def __init__ (self):
        self.steeringAngle = 0

        with open (pm.sampleFileName, 'w') as self.sampleFile: # open file met schrijfrechten
            with sc.socket (*sw.socketType) as self.clientSocket: # socketwrapper maakt connectie tussen wereld en auto
                self.clientSocket.connect (sw.address)
                self.socketWrapper = sw.SocketWrapper (self.clientSocket)
                self.halfApertureAngle = False # roep je vast aan, maar wordt nog niet gebruikt

                while True: # programma blijft draaien totdat niet meer aan de voorwaarden wordt voldaan (bv stoppen van het programma)
                    self.input ()
                    self.sweep () # we zeggen hier nog niet lidar of sonar
                    self.output ()
                    self.logTraining ()
                    tm.sleep (0.02) # om de zoveel tijd krijgt ie nieuwe stuurhoek en snelheid

    def input (self): # dit doet voornamelijk data ontvangen. kan dus ook gelijk blijven als we met neural network aan de slag gaan.
        sensors = self.socketWrapper.recv () # dus, waar ben ik in de wereld. en stop die info in de sensoren. Tip: zet hier breakpoint, zodat je kan zien wat er in sensors zit

        if not self.halfApertureAngle: # we beginnen op false, zodat we altijd deze loop in gaan
            self.halfApertureAngle = sensors ['halfApertureAngle']
            self.sectorAngle = 2 * self.halfApertureAngle / pm.lidarInputDim # pm is parameter
            self.halfMiddleApertureAngle = sensors ['halfMiddleApertureAngle']
            
        if 'lidarDistances' in sensors:
            self.lidarDistances = sensors ['lidarDistances']
        else:
            self.sonarDistances = sensors ['sonarDistances']

    def lidarSweep (self): # we kijken in dit stukje code steeds naar 2 pionnen. Dit stukje van de code is hetgeen we echt zelf moeten gaan herschrijven
        nearestObstacleDistance = pm.finity # hier setten we die op 20, dus hij ziet pionnen tot 20m
        nearestObstacleAngle = 0
        
        nextObstacleDistance = pm.finity
        nextObstacleAngle = 0

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle): # we gaan hier van links naar rechts door de sectoren van de aperture, graad voor graad (dus die 16 sectoren is ergens anders voor)
            lidarDistance = self.lidarDistances [lidarAngle] # voor elke lidar angle hebben we een distance (=de afstand tot pylon voor deze specifieke hoek)
            
            if lidarDistance < nearestObstacleDistance: # als hier blijkt dat de afstand kleiner is dan 20, dan is dit dus interessant
                nextObstacleDistance =  nearestObstacleDistance # we hebben er hierboven 1 gevonden dan we hadden, en dus maken we de dichtsbijzijnde nu de op 1 na dichtsbijzijnde. Dit is nog steeds belangrijke info die we dus willen bewaren
                nextObstacleAngle = nearestObstacleAngle
                
                nearestObstacleDistance = lidarDistance 
                nearestObstacleAngle = lidarAngle

            elif lidarDistance < nextObstacleDistance: # hier wordt nog gekeken naar de op-1-na dichtsbijzijnde
                nextObstacleDistance = lidarDistance
                nextObstacleAngle = lidarAngle
           
        targetObstacleDistance = (nearestObstacleDistance + nextObstacleDistance) / 2 # ik weet de hoek tussen beide pylonnen, en ga daar midden tussendoor rijden

        self.steeringAngle = (nearestObstacleAngle + nextObstacleAngle) / 2 # wordt bepaald door 2 pionnen
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle) # bepaald snelheid op basis van stuurhoek

    def sonarSweep (self):
        obstacleDistances = [pm.finity for sectorIndex in range (3)]
        obstacleAngles = [0 for sectorIndex in range (3)]
        
        for sectorIndex in (-1, 0, 1):
            sonarDistance = self.sonarDistances [sectorIndex]
            sonarAngle = 2 * self.halfMiddleApertureAngle * sectorIndex
            
            if sonarDistance < obstacleDistances [sectorIndex]:
                obstacleDistances [sectorIndex] = sonarDistance
                obstacleAngles [sectorIndex] = sonarAngle

        if obstacleDistances [-1] > obstacleDistances [0]:
            leftIndex = -1
        else:
            leftIndex = 0
           
        if obstacleDistances [1] > obstacleDistances [0]:
            rightIndex = 1
        else:
            rightIndex = 0
           
        self.steeringAngle = (obstacleAngles [leftIndex] + obstacleAngles [rightIndex]) / 2
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle)

    def sweep (self):
        if hasattr (self, 'lidarDistances'): # afhankelijk van de aangeboden data, wordt hier bepaald of we lidar of sonar gaan gebruiken
            self.lidarSweep ()
        else:
            self.sonarSweep ()

    def output (self): # hier gaan we ahv berekeningen gegevens terugsturen naar auto (via socketwrapper). deze functie komt precies zo in mijn eigen programma
        actuators = {
            'steeringAngle': self.steeringAngle,
            'targetVelocity': self.targetVelocity
        }

        self.socketWrapper.send (actuators)

    def logLidarTraining (self): # dit gaat over hoe je je deafault.sample vult
        sample = [pm.finity for entryIndex in range (pm.lidarInputDim + 1)]

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle):
            sectorIndex = round (lidarAngle / self.sectorAngle)
            sample [sectorIndex] = min (sample [sectorIndex], self.lidarDistances [lidarAngle])

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)

    def logSonarTraining (self):
        sample = [pm.finity for entryIndex in range (pm.sonarInputDim + 1)]

        for entryIndex, sectorIndex in ((2, -1), (0, 0), (1, 1)):
            sample [entryIndex] = self.sonarDistances [sectorIndex]

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)

    def logTraining (self):
        if hasattr (self, 'lidarDistances'):
            self.logLidarTraining ()
        else:
            self.logSonarTraining ()

HardcodedClient ()
