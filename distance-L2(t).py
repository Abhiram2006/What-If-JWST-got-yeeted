#Distance from L2 as a function of time

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

GRAVITATIONAL_CONSTANT = 6.67e-11
MASS_SUN = 1.9891e30
DELTA_TIME = 5
P_DIST = 1.4709e11
P_SPEED = 30290
L2_FACTOR = 1.011516
MASS_EARTH = 5.972e24

class Earth(object):
    acc = np.zeros(shape = 2, dtype=float)
    def __init__(self, position, velocity) -> None:
        self.pos = np.array(position, dtype=float)
        self.vel = np.array(velocity, dtype=float)
        
    def getDistance(self):
        return sqrt(pow(self.pos[0], 2) + pow(self.pos[1], 2))

    def getAcc(self):
        self.acc = (-1*GRAVITATIONAL_CONSTANT*MASS_SUN / pow(self.getDistance() ,3))*self.pos
    
class Satellite(object):
    acc = np.zeros(shape = 2, dtype=float)
    def __init__(self, position, velocity) -> None:
        self.pos = np.array(position, dtype=float)
        self.vel = np.array(velocity, dtype=float)
        
    def getDistance(self):
        return sqrt(pow(self.pos[0], 2) + pow(self.pos[1], 2))
    
    def getDistanceEarth(self, earth):
        temp_pos = self.pos - earth.pos
        return sqrt(pow(temp_pos[0], 2) + pow(temp_pos[1], 2))
    
    def getAcc(self, earth):
        self.acc =  -1*GRAVITATIONAL_CONSTANT*((MASS_SUN / pow(self.getDistance() ,3))*self.pos 
        + MASS_EARTH / pow(self.getDistanceEarth(earth), 3) *(self.pos - earth.pos))
        
def updateSpeed(bodies):
    for i in bodies:
        i.vel = i.vel + i.acc*DELTA_TIME / 2

def updatePos(bodies):
    for i in bodies:
        i.pos = i.vel*DELTA_TIME + i.pos

def getDistanceLagrange(earth, satellite):
    temp_pos = L2_FACTOR * earth.pos - satellite.pos
    return (sqrt(pow(temp_pos[0], 2) + pow(temp_pos[1],2)))
    
def main():
    earth = Earth([P_DIST, 0],[0, P_SPEED])
    satellite = Satellite([P_DIST*L2_FACTOR, 0],[0, 14470])
    bodies = [earth, satellite]
    
    time = []
    distance_lagrangian = []
    satellite_pos_x = []
    satellite_pos_y = []
    
    days = 365
    for i in range(int(days*24*60*60/DELTA_TIME)):
        if(i % (int(24*3600/DELTA_TIME)) == 0):
            time.append(i / (int(24*3600/DELTA_TIME))) 
            distance_lagrangian.append(getDistanceLagrange(earth, satellite))
            satellite_pos_x.append(satellite.pos[0])
            satellite_pos_y.append(satellite.pos[1]) 
        
        earth.getAcc()
        satellite.getAcc(earth)
        
        updateSpeed(bodies)
        updatePos(bodies)
        
        earth.getAcc()
        satellite.getAcc(earth)
        
        updateSpeed(bodies)
    
    print(f"Final position of satellite is ({satellite.pos[0]}m, {satellite.pos[1]}m) 
    
    which is at a distance of {satellite.getDistance()} from Sun") 
    
    plt.plot(time, distance_lagrangian)
    plt.ylabel = "Distance of satellite from L2"
    plt.xlabel = "Time in days"
    plt.show()
    
