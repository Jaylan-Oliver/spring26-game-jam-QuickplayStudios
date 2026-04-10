import pygame as pyg
import game

class Projectile:
    def __init__(self, img, velocity, xdir, ydir):
        self.x = 50
        self.y = 50
        self.velocity = velocity
        
        # direction: +1 = forward (positive dir), 0 = no movement along this axis, -1 = backward (negative dir)
        self.xdir = xdir 
        self.ydir = ydir
        self.angle = 0
        if xdir == -1:
            angle = 0
        elif xdir == -1 and ydir == -1:
            angle = 45
        elif ydir == -1:
            angle = 90
        elif xdir == 1 and ydir == -1:
            angle = 135
        elif xdir == 1:
            angle = 180
        elif xdir == 1 and ydir == 1:
            angle = 225
        elif ydir == 1:
            angle = 270
        
        self.surface = pyg.transform.scale(img, (img.get_width()*2, img.get_height()*2))   
        self.surface = pyg.transform.rotate(self.surface, angle) # face correct direction
        self.hitbox = pyg.mask.from_surface(self.surface)

''' 
move projectiles horizontally
projectiles = array of projectile objects
'''
def moveprojectiles(projectiles):
    for p in projectiles:
        if p.x in range(0, 650) and p.y in range(0,650): # if projectile in screen boundaries, plus extra for boundaries
            # if moving horizontally
            if p.xdir != 0:
                p.x += p.velocity * p.xdir
            # if moving vertically
            if p.ydir != 0:
             p.y += p.velocity * p.ydir
             
        else: # despawn
            projectiles.pop(projectiles.index(p))
            
