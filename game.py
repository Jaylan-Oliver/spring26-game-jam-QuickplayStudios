import pygame as pyg
pyg.init()




# Window
screen = pyg.display.set_mode((640, 640))

# Assets
cake_img = pyg.image.load('./assets/cake.png').convert_alpha()
cake = pyg.transform.scale(cake_img, 
                             (cake_img.get_width()*2, cake_img.get_height()*2))

clock = pyg.time.Clock()

# Game state
running = True
moving = False
x = 0

# Game loop
while running:
    dt = clock.tick(60) / 1000 # calculate dt dynamically

    # --- INPUT ---
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_d:
                moving = True

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_d:
                moving = False

    mpos = pyg.mouse.get_pos()

    # --- UPDATE ---
    if moving:
        x += 200 * dt

    cake_hitbox = pyg.Rect(x, 40, cake.get_width(), cake.get_height())
    obstacle = pyg.Rect(300, 10, 160, 280)

    cake_collide_obst = cake_hitbox.colliderect(obstacle)
    m_collide_obst = obstacle.collidepoint(mpos)

    # --- DRAW ---
    screen.fill((0, 0, 0)) #fill window black

    screen.blit(cake, (x, 40)) #show cake

    pyg.draw.rect( # draw the rect to the screen surface
        screen,
        (255 * cake_collide_obst, 255 * m_collide_obst, 255),
        obstacle
    )

    pyg.display.flip() # update screen