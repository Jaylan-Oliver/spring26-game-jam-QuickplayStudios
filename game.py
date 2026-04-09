import pygame as pyg
pyg.init()

# --- Notes ---
# 0,0 = top left corner of window
# -------------

# Window
window = pyg.display.set_mode((640, 640))

# Class for player character
class Player:
    def __init__(self, img):
        self.x = 50
        self.y = 50
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
    
    def turn(self):
        self.surface = pyg.transform.flip(self.surface, True, False)
        self.l_facing = not self.l_facing
        
class Projectile:
    def __init__(self, img):
        self.x = 50
        self.y = 50
        self.surface = pyg.transform.scale(img, (img.get_width()*2, img.get_height()*2))
        self.hitbox = pyg.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        
        
# Assets & Objects
cake_img = pyg.image.load('./assets/smcake.png').convert_alpha()
fork_img = pyg.image.load('./assets/smfork.png').convert_alpha()

cake = Player(cake_img)
fork = Projectile(fork_img)

clock = pyg.time.Clock()

# Initialize game state
running = True
moving = False
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
        
    # print(cake.x, cake.y) # for debugging
    mpos = pyg.mouse.get_pos()

    # --- UPDATE ---
    cake.updatepos()

    # --- DRAW ---
    window.fill((0, 0, 0)) #fill window black

    window.blit(cake.surface, (cake.x, cake.y)) #show cake at position (x, y)
    
    #to see hitbox
    pyg.draw.rect(window, (255, 0, 0), cake.hitbox, 1) # draw with border 2

    pyg.display.flip() # update window