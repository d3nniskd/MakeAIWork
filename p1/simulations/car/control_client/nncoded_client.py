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
model_lidar = pickle.load(open('../../../projects/p1/lidar_model.pkl', 'rb'))
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
            if self.model == None:
                self.model = model_lidar
        else:
            self.sonarDistances = sensors ['sonarDistances']
            if self.model == None:
                self.model = model_sonar

    def lidarSweep (self): 
        sample = [pm.finity for entryIndex in range (pm.lidarInputDim + 1)]

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle):
            sectorIndex = round (lidarAngle / self.sectorAngle)
            sample [sectorIndex] = min (sample [sectorIndex], self.lidarDistances [lidarAngle])

        steeringangle = self.model.predict(np.array([sample[0:16]]))
        self.steeringAngle = float(steeringangle[0]) 
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle) #steeringAngle (stuurhoek) koppelen aan targetVelocity

        print(steeringangle)

    def sonarSweep (self):
        steeringangle = self.model.predict(np.array([self.sonarDistances]))
        self.steeringAngle = float(steeringangle[0]) # koppelen
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
