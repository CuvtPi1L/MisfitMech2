import numpy as np
import math

# =======================================================
# Classes
# =======================================================

class Projectile:
    def __init__(self,Mass,V_x, V_y, x, y, R):
        self.M = Mass
        self.V_X = V_x
        self.V_Y = V_y
        self.X = x
        self.Y = y
        self.R = R

    def getSpeed(self):
        return((self.V_X**2 + self.V_Y**2)**(1/2))
    def getEnergy(self):
        return(self.M*self.getSpeed()**2)

    def update(self,F_X,F_Y,dt):
        """Updates the velocity for the given force and then changes its position"""
        self.V_X = self.V_X + (F_X/self.M)*dt
        self.V_Y = self.V_Y + (F_Y/self.M)*dt
        
        self.X = self.X + self.V_X*dt + 0.5*(F_X/self.M)*dt**2
        self.Y = self.Y + self.V_Y*dt + 0.5*(F_Y/self.M)*dt**2

    def Y_pos_at_X(self, x):
        """Returns the lowest point of the projectile at a given x.
        Returns equilibrium position of springs if the projectile is not present here"""
        return (self.Y-np.sqrt(abs(self.R**2-(x-self.X)**2)))

class Spring:
    def __init__(self, x, y, k, m) -> None:
        self.X = x
        self.Y = y
        self.k = k
        self.X_Equ = x
        self.Y_Equ = y
        self.V_X = 0
        self.V_Y = 0
        self.m = m

    def get_F_Y(self):
        return(self.k*(self.Y_Equ-self.Y))

    def get_F_X(self):
        return(self.k*(self.X_Equ-self.X))
        
    def update(self, F_X, F_Y, dt):
        """Inertial implementation of spring motion"""
        self.V_X = self.V_X + (F_X/self.m)*dt
        self.V_Y = self.V_Y + (F_Y/self.m)*dt
        
        self.X = self.X + self.V_X*dt + 0.5*(F_X/self.m)*dt**2
        self.Y = self.Y + self.V_Y*dt + 0.5*(F_Y/self.m)*dt**2
        
# =======================================================
# Functions
# =======================================================

def init_springs(N_springs, dx, k, m):
    springs = []
    for i in range(N_springs):
        springs.append(Spring(i*dx, 0, k, m))
    return springs

def is_touching(spring, projectile, epsilon,R=1,check_vert_only=True):
    distance = np.sqrt((projectile.Y-spring.Y)**2+(projectile.X-spring.X)**2)
    if check_vert_only:
        return (distance - R <= epsilon)
        #return(projectile.Y_pos_at_X(spring.X)-spring.Y - 1 <= epsilon)
    else:
        return (distance - R <= epsilon)
        #return(np.sqrt((projectile.Y-spring.Y)**2+(projectile.X-spring.X)**2)-projectile.R <= epsilon)

def add_forces(springs, projectile, epsilon):
    """Returns an array with the X and Y components of the force of touching springs"""
    F = [0, 0]
    for spring in springs:
        if is_touching(spring, projectile, epsilon):
            F[0] = F[0] + spring.get_F_X()
            F[1] = F[1] + spring.get_F_Y()
    return(F)

def push_outside(spring, projectile, epsilon):
    """"push the particle to the side of Projectile and set velocity to that of the projectile"""
    #spring.Y = projectile.Y_pos_at_X(spring.X)
    if projectile.V_Y < spring.V_Y:
        spring.V_Y = projectile.V_Y

# try to put in horizontal srpings, but will be very difficult 
# calculate the amount of energy that the springs are taking from the projectile
# energy discipation? term proportional to velocity 