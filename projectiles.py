import pygame as pyg

class Projectile:
    def __init__(self, img, x, y, velocity, xdir, ydir):
        self.x = x
        self.y = y
        self.velocity = velocity
        
        # direction: +1 = forward (positive dir), 0 = no movement along this axis, -1 = backward (negative dir)
        self.xdir = xdir 
        self.ydir = ydir
        self.angle = 0
        if xdir == -1 and ydir == 0: # move left
            self.angle = 0
        elif xdir == -1 and ydir == -1: # move down left
            self.angle = 315
        elif xdir == 0 and ydir == -1: # move down
            self.angle = 270
        elif xdir == 1 and ydir == -1: # move down right
            self.angle = 225
        elif xdir == 1 and ydir == 0: # move right
            self.angle = 180
        elif xdir == 1 and ydir == 1: # move up right
            self.angle = 135
        elif xdir == 0 and ydir == 1: # move up
            self.angle = 90
        elif xdir == -1 and ydir == 1: # move up left
            self.angle = 45
        
        self.surface = pyg.transform.scale(img, (img.get_width()*2, img.get_height()*2))   
        self.surface = pyg.transform.rotate(self.surface, self.angle) # face correct direction
        self.hitbox = pyg.mask.from_surface(self.surface)

''' 
move projectiles based on direction facing
projectiles = array of projectile objects
'''
def moveprojectiles(projectiles):
    for p in projectiles:
        if p.x in range(-50,1600) and p.y in range(-50,1600): # if projectile in screen boundaries, plus extra for boundaries
            # if moving horizontally
            if p.xdir != 0:
                p.x += p.velocity * p.xdir
            # if moving vertically
            if p.ydir != 0:
             p.y += p.velocity * p.ydir
             
        else: # despawn
            projectiles.pop(projectiles.index(p))
            
# Generate bullet patterns
def burst(img, x, y, velocity): # all directions
    bullets = []
    dirs = [-1,0,1]
    
    for xd in dirs:
        for yd in dirs:
            if not(xd == 0 and yd == 0): # avoid stationary bullet
                bullets.append(Projectile(img, x, y, velocity, xd, yd))
            
    return bullets

def vertwall():
    bullets = []
    
    #bullets.append(Projectile(img, x, y, velocity, xd, yd))
            
    return bullets