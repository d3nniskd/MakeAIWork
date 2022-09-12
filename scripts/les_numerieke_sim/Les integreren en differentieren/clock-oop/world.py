import time as tm

from car import Car

class World:
    
    #Constructor
    def __init__(self):
        self.t = 0.0
        self.dt = 0.1
        
        self.running = True
        self.car = Car("Tesla", 800.0, 600.0)
    
    def bang(self):
        
        while self.running:
            
            self.t += self.dt
            
            self.car.move(self.dt)
            
            print('Time: ', self.t)
            
            tm.sleep(self.dt)
            
            if self.car.x > 100.0:
                
                self.running = False
            
            
    
   # def stop(self):