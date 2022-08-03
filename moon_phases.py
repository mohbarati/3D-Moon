import pygame as pg
from pygame.locals import *
from math import cos, sin

"""Starting the screen"""
wh = 900
sc = pg.display.set_mode((wh, wh))
# ----------------------------

"""Loading image of the moon"""
moon = pg.image.load("moon_transp.png")
x_s, y_s = moon.get_size()

# Downsizing the image to make it run faster
moon = pg.transform.scale(moon, (x_s / 2, y_s / 2))
x_s, y_s = moon.get_size()
# ----------------------------
"""Setting up the functions"""


def radius_calc():
    """
    Calculates radius of the moon in the image by finding
    number of bright pixles in each rwo and returning half
    of its max val. One could simply use R = y_s/2 instead.
    Returns:
        _type_: float
    """
    radii = []
    for i in range(x_s):
        R = 0
        for j in range(y_s):
            r, g, b = moon.get_at((i, j))[:3]
            if (r, g, b) != (255, 255, 255):
                R += 1
        radii.append(R)
    return max(radii) / 2 + 1  # with no addition zz becomes complex no.


def light(phi, theta):
    """Finds the three components of light ray in the
    spherical coordinate system with rho = 1. This will
    ensure normality

    Args:
        phi (float): angle (w/r to z axis) in radian
        theta (float): angle (w/r to x axis) in radian

    Returns:
        tuple: a tuple of 3 components lx,ly, and lz
    """
    return cos(phi) * cos(theta), cos(phi) * sin(theta), sin(phi)


def draw(L):
    """redrawing the moon image with the given shading

    Args:
        L (list): normalized light ray vector
    """
    lx, ly, lz = L
    for i in range(x_s):
        for j in range(y_s):
            r, g, b = moon.get_at((i, j))[:3]
            if (r, g, b) != (255, 255, 255):
                k = (R**2 - (i - x_r) ** 2 - (j - y_r) ** 2) ** 0.5
                ii = (i - x_r) / R
                jj = (j - y_r) / R
                kk = k / R
                c = lx * ii + ly * jj + lz * kk
                if c < 0:
                    sc.set_at((i + x, j + y), (-c * r, -c * g, -c * b))


# ------------------
"""setting initial values"""
phi, theta = 0, 0  # initial direction of light source

R = radius_calc()  # or y_r/2 + 1 as radius of the moon

x_r, y_r = x_s / 2, y_s / 2  # location of the moon's center

x, y = (wh - x_s) // 2, (wh - y_s) // 2  # centering the moon

change_phi, change_theta = 0, 0

"""Starting the pygame loop"""
cont = True
while cont:
    """Use arrow keys to change the direction of the lightsource and esc to quit"""
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == pg.K_UP:
                change_theta = -0.1
            if event.key == pg.K_DOWN:
                change_theta = 0.1
            if event.key == pg.K_RIGHT:
                change_phi = -0.1
            if event.key == pg.K_LEFT:
                change_phi = 0.1
        if event.type == KEYUP:
            if event.key == pg.K_UP:
                change_theta = 0
            if event.key == pg.K_DOWN:
                change_theta = 0
            if event.key == pg.K_RIGHT:
                change_phi = 0
            if event.key == pg.K_LEFT:
                change_phi = 0
            if event.key == pg.K_ESCAPE:
                cont = False

        if event.type == QUIT:
            cont = False
            pg.quit()

    phi += change_phi
    theta += change_theta

    sc.fill((0, 0, 0))  # clear the screen before each new change
    draw(light(phi, theta))  # redrawing the shape on the screen
    pg.display.update()
