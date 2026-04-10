import pygame as pyg
from camera import create_Screen
from camera import camera
import projectiles as prj
import random as rnd

pyg.init()

# --- Notes ---
# 0,0 = top left corner of window
# -------------

# Window
gameWidth = 1600
gameHeight = 900
wallThickness = 150
window = create_Screen(gameWidth,gameHeight, "Cake Game")

# Class for player character
class Player:
    def __init__(self, img):
        self.x = camera.width // 2
        self.y = camera.height // 2
        self.surface = pyg.transform.scale(img, (img.get_width()*2, img.get_height()*2)) # sprite surface itself
        self.hitbox = pyg.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height()) # moves based on position
        self.l_facing = True
        
    def setpos(self, x, y):
        self.x = x
        self.y = y
        self.updatepos()
    
    def updatepos(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        camera.x = self.x - camera.width / 2 
        camera.y = self.y - camera.height / 2


    def turn(self):
        self.surface = pyg.transform.flip(self.surface, True, False)
        self.l_facing = not self.l_facing
        
walls = [
pyg.Rect(0,0, gameWidth, gameHeight), #top wall
pyg.Rect(0,gameHeight-wallThickness, gameWidth, wallThickness), #bottom wall
pyg.Rect(0,0, wallThickness, gameHeight), #left wall
pyg.Rect(gameWidth-wallThickness,0, wallThickness, gameHeight), #right wall
    ]

# Assets & Objects
cake_img = pyg.image.load('./assets/smcake.png').convert_alpha()
fork_img = pyg.image.load('./assets/smfork.png').convert_alpha()
knife_img = pyg.image.load('./assets/knife.png').convert_alpha()
tablecloth = pyg.image.load('./assets/tablecloth.png').convert_alpha()

cake = Player(cake_img)

clock = pyg.time.Clock()

# Initialize game state
running = True
player_velocity = 6 # pixels per frame i think
forks = []

# Game loop
while running:
    dt = clock.tick(60) / 1000 # calculate dt dynamically

    # --- INPUT ---
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    keys = pyg.key.get_pressed()
    if keys [pyg.K_LEFT]:
        cake.x -= player_velocity
        if (not cake.l_facing):
            cake.turn()
    if keys [pyg.K_RIGHT]:
        cake.x += player_velocity
        if(cake.l_facing):
            cake.turn()
    if keys [pyg.K_UP]:
        cake.y -= player_velocity
    if keys [pyg.K_DOWN]:
        cake.y += player_velocity

    for wall in walls:
        if cake.hitbox.colliderect(wall):

            # stop horizontal movement
            if cake.hitbox.right > wall.left and cake.x < wall.left:
                cake.x = wall.left - cake.surface.get_width()

            if cake.hitbox.left < wall.right and cake.x > wall.right:
                cake.x = wall.right

            # stop vertical movement
            if cake.hitbox.bottom > wall.top and cake.y < wall.top:
                cake.y = wall.top - cake.surface.get_height()

            if cake.hitbox.top < wall.bottom and cake.y > wall.bottom:
                cake.y = wall.bottom

    #print("cake",cake.x, cake.y) # for debugging
    #pyg.time.delay(100)
    #print("cake hitbox",cake.hitbox.x,cake.hitbox.y)
    mpos = pyg.mouse.get_pos()

    # --- UPDATE ---
    cake.updatepos()
    
    # spawn projectiles
    # spawn bursts along outside edges of map
    if rnd.random() < 0.01:
        #top and bottom
        forks += prj.burst(fork_img, rnd.randint(0,1600), rnd.randint(0,150), 1)
        forks += prj.burst(fork_img, rnd.randint(0,1600), rnd.randint(750,900), 1)
    if rnd.random() < 0.005:
        #left and right
        forks += prj.burst(fork_img, 75, rnd.randint(0,1600), 1)
        forks += prj.burst(fork_img, 1525, rnd.randint(0,1600), 1)
    #spawn knife
    if rnd.random() < 0.005:
        #left and right
        forks.append(prj.Projectile(knife_img, 75, rnd.randint(150,1450), 5, 1, 0))
        forks.append(prj.Projectile(knife_img, 1525, rnd.randint(150,1450), 5, -1, 0))
    prj.moveprojectiles(forks)
    prj.collisioncheck(forks, cake)

    # --- DRAW ---
    window.blit(tablecloth, (-camera.x, -camera.y)) # bg

    window.blit(cake.surface, (cake.x - camera.x, cake.y - camera.y)) #show cake at position (x, y)
    
    # draw projectiles
    for f in forks:
        window.blit(f.surface, (f.x - camera.x, f.y - camera.y))
    
    #to see hitbox
    cake_hitbox = pyg.draw.rect(window, (255, 0, 0), cake.hitbox.move(-camera.x,-camera.y), 1) # draw with border 2

    pyg.display.flip() # update window