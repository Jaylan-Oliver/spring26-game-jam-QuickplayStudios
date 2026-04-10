import pygame as pyg

camera = pyg.Rect(0, 0, 0, 0)

def create_Screen(width,height, title):
    pyg.display.set_caption(title)

    screen = pyg.display.set_mode((width,height))
    camera.width = width
    camera.height = height
    return screen