class Car:
    
    #The contructor
    def __init__(self, name, F, m):
        
        # self.F = 800.0
        # self.m = 600.0
        # deze niet meer meegeven, omdat we nu de betreffende variabelen in de 'def __init__' zitten
        
        self.F = F
        self.m = m
        
        self.x = 0.0
        self.v = 0.0
    
        #self.name = 
    def move(self, dt):
        print(dt)
        a = self.F / self.m
        print(a)
        dv = a * dt
        self.v = self.v + dv
        print("v: ", self.v)

        dx = self.v * dt
        print(str(dx)+'__')
        self.x = self.x + dx
        print('x: ', self.x)