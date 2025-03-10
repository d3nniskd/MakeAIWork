import time as tm
import traceback as tb # als iets grijs kleurt in vsc wordt ie niet gebruikt
import math as mt
import sys as ss
import os
import socket as sc
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)] 

import socket_wrapper as sw
import parameters as pm

# lokatie deze file ->     /Users/dennis/Repo/MakeAIWork/simulations/car/control_client/nncoded_client.py
# lokatie pickeld_model -> /Users/dennis/Repo/MakeAIWork/projects/p1/pickle_model.pkl
model_sonar = pickle.load(open('../../../projects/p1/pickle_model.pkl', 'rb'))
# dit verderop in de code aanroepen -> pickled_model.predict(X_test)

class NncodedClient:
    def __init__ (self):
        self.steeringAngle = 0
        self.model = None

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
        sensors = self.socketWrapper.recv () # waar ben ik in de wereld. en stop die info in de sensoren. Tip: zet hier breakpoint, zodat je kan zien wat er in sensors zit

        if not self.halfApertureAngle: # we beginnen op false, zodat we altijd deze loop in gaan
            self.halfApertureAngle = sensors ['halfApertureAngle']
            self.sectorAngle = 2 * self.halfApertureAngle / pm.lidarInputDim
            self.halfMiddleApertureAngle = sensors ['halfMiddleApertureAngle'] # pm is parameter
            
        if 'lidarDistances' in sensors:
            self.lidarDistances = sensors ['lidarDistances']
        else:
            self.sonarDistances = sensors ['sonarDistances']
            if self.model == None:
                self.model = model_sonar

    def lidarSweep (self): # we kijken in dit stukje code steeds naar 2 pionnen. Dit stukje van de code is hetgeen we echt zelf moeten gaan herschrijven
        nearestObstacleDistance = pm.finity # hier setten we die op 20, dus hij ziet pionnen tot 20m
        nearestObstacleAngle = 0
        
        nextObstacleDistance = pm.finity
        nextObstacleAngle = 0

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle): # we gaan hier van links naar rechts door de sectoren van de aperture, graad voor graad (dus die 16 sectoren is ergens anders voor)
            lidarDistance = self.lidarDistances [lidarAngle] # voor elke lidar angle hebben we een distance (=de afstand tot pylon voor deze specifieke hoek)
            
            if lidarDistance < nearestObstacleDistance: # als hier blijkt dat de afstand kleiner is dan 20, dan is dit dus interessant
                nextObstacleDistance =  nearestObstacleDistance # we hebben er hierboven 1 gevonden die dichterbij dan we hadden, en dus maken we de dichtsbijzijnde nu de op 1 na dichtsbijzijnde. Dit is nog steeds belangrijke info die we dus willen bewaren
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
        steeringangle = self.model.predict(np.array([self.sonarDistances]))
        self.steeringAngle = float(steeringangle[0]) # koppelen
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle)
        # dit is stuk code dat door de NN moet worden bestuurd als ik het goed begrijp
        # obstacleDistances = [pm.finity for sectorIndex in range (3)]
        # obstacleAngles = [0 for sectorIndex in range (3)]
        
        # for sectorIndex in (-1, 0, 1):
        #     sonarDistance = self.sonarDistances [sectorIndex]
        #     # sonarAngle = 2 * self.halfMiddleApertureAngle * sectorIndex
        #     sonarAngle = 2 * self.halfMiddleApertureAngle * sectorIndex
            
        #     if sonarDistance < obstacleDistances [sectorIndex]:
        #         obstacleDistances [sectorIndex] = sonarDistance
        #         obstacleAngles [sectorIndex] = sonarAngle

        # if obstacleDistances [-1] > obstacleDistances [0]:
        #     leftIndex = -1
        # else:
        #     leftIndex = 0
           
        # if obstacleDistances [1] > obstacleDistances [0]:
        #     rightIndex = 1
        # else:
        #     rightIndex = 0
           
        # # self.steeringAngle = (obstacleAngles [leftIndex] + obstacleAngles [rightIndex]) / 2
        # self.steeringAngle = sks.predictions(self.sonarDistances) # of zoiets
        

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

    def logLidarTraining (self): # dit gaat over hoe je je default.sample vult
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

NncodedClient ()
