import pygame as pyg
from camera import create_Screen
from camera import camera
import projectiles as prj
import random as rnd
import time

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
        # stop camera leaving background
        camera.x = max(0, min(camera.x, gameWidth - camera.width))
        camera.y = max(0, min(camera.y, gameHeight - camera.height))


    def turn(self):
        self.surface = pyg.transform.flip(self.surface, True, False)
        self.l_facing = not self.l_facing
        
walls = [
    pyg.Rect(0, 0, gameWidth, wallThickness),                       # top
    pyg.Rect(0, gameHeight - wallThickness, gameWidth, wallThickness), # bottom
    pyg.Rect(0, 0, wallThickness, gameHeight),                      # left
    pyg.Rect(gameWidth - wallThickness, 0, wallThickness, gameHeight) # right
]

# Assets & Objects
cake_img = pyg.image.load('./assets/smcake.png').convert_alpha()
fork_img = pyg.image.load('./assets/smfork.png').convert_alpha()
knife_img = pyg.image.load('./assets/knife.png').convert_alpha()
tablecloth = pyg.image.load('./assets/tablecloth.png').convert_alpha()
lose_screen = pyg.image.load('./assets/lose screen.png').convert_alpha()
void = pyg.image.load('./assets/void.png').convert_alpha()

cake = Player(cake_img)

clock = pyg.time.Clock()

# Initialize game state
running = True
player_velocity = 6 # pixels per frame i think
forks = []
game_over = False

# Game loop
while running:
    dt = clock.tick(60) / 1000 # calculate dt dynamically

    # Window x button
    for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False

    if not game_over:
        
        # --- INPUT ---

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
            # collision from left
            if cake.hitbox.right > wall.left and cake.hitbox.left < wall.left:
                cake.x = cake.x - cake.hitbox.width

            # collision from right
            if cake.hitbox.left < wall.right and cake.hitbox.right > wall.right:
                cake.x = wall.right

            # collision from top
            if cake.hitbox.bottom > wall.top and cake.hitbox.top < wall.top:
                cake.y = wall.top - cake.hitbox.height

            # collision from bottom
            if cake.hitbox.top < wall.bottom and cake.hitbox.bottom > wall.bottom:
                cake.y = wall.bottom

        print("cake",cake.x, cake.y) # for debugging
        pyg.time.delay(10)
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
        if prj.collisioncheck(forks, cake):
            game_over = True
            pyg.mixer.music.load('./assets/squish.mp3')
            pyg.mixer.music.play()

    # --- DRAW ---
    if not game_over:
        window.blit(tablecloth, (-camera.x, -camera.y)) # bg

        window.blit(cake.surface, (cake.x - camera.x, cake.y - camera.y)) #show cake at position (x, y)
        
        # draw projectiles
        for f in forks:
            window.blit(f.surface, (f.x - camera.x, f.y - camera.y))
            #pyg.draw.rect(window, (255, 0, 0), f.hitbox.move(-camera.x,-camera.y), 1) # to see hitbox
        
        #to see player hitbox
        #cake_hitbox = pyg.draw.rect(window, (255, 255*(collision), 0), cake.hitbox.move(-camera.x,-camera.y), 1) # draw with border 2    
        
        # world border
        window.blit(void, (-camera.x, -camera.y))
        
    else:
        window.blit(lose_screen,(0,0))
    
    pyg.display.flip() # update window
    
    
