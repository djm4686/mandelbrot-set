from __future__ import division
from pygame.locals import *
import cmath
import pygame


MAX_DIVERGENCE = 2
MAX_ITERATIONS = 100
RESOLUTION = 500


def make_matrix(startx, starty, endx, endy, resolution):
    mm = []
    dx = endx - startx
    ndx = dx / (3 * resolution)
    dy = endy - starty
    ndy = dy / (2 * resolution)
    currx = startx
    curry = starty
    mm = []
    boolm = []
    while currx < endx:
        mm.append([])
        boolm.append([])
        curry = starty
        while curry > endy:
            mm[-1].append((currx, curry))
            boolm[-1].append(mandelbrot(0, complex(currx, curry)))
            curry += ndy
        currx += ndx
    return mm, boolm
def main():
    #mandel_matrix = []
    #for x in range(-2 * RESOLUTION, RESOLUTION):
    #    mandel_matrix.append([])
    #    for y in range(-RESOLUTION, RESOLUTION):
    #        print x/RESOLUTION, y/RESOLUTION
    #        base_c = complex(x/RESOLUTION, -y/RESOLUTION)
    #        mandel_matrix[x+(2*RESOLUTION)].append(mandelbrot(0, base_c))
    mm, mandel_matrix = make_matrix(-2, 1, 1, -1, RESOLUTION)
    pygame.init()
    surface = pygame.display.set_mode((3*RESOLUTION, 2*RESOLUTION))

    surface.fill((255,255,255))
    pxa = pygame.PixelArray(surface)
    print "before loop"
    for i, x in enumerate(mandel_matrix):
        for j, y in enumerate(x):
            print i, j, y
            try:
                if j < RESOLUTION * 2 and i < RESOLUTION * 3:
                    pxa[i][j] = (int(255 * y), int(255 * y/2), int(255 * y/3))
            except:
                print i, j
    print "after loop"
    s = pxa.make_surface()
    del pxa
    print "got here"
    surface.blit(s, pygame.Rect((0, 0), (100, 100)))
    print "got here 2"
    mouse_point = 0, 0
    start_point = 0, 0
    holding = False
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_point = event.pos
                start_point = event.pos
                holding = True
            elif event.type == MOUSEMOTION:
                mouse_point = event.pos
            elif holding and event.type == MOUSEBUTTONUP:
                holding = False
                mm = make_surface(surface, RESOLUTION, mm[start_point[0]][start_point[1]], mm[mouse_point[0]][mouse_point[1]])
        if holding:
            w, h = mouse_point[0] - start_point[0], mouse_point[1] - start_point[1]
            s = pygame.Surface((abs(w), abs(h)))
            pygame.draw.rect(s, (100, 100, 100), pygame.Rect((0, 0), (w, h)))
            s.set_alpha(100)
            surface.blit(s, pygame.Rect(start_point, (w, h)))

        pygame.display.update()


def make_surface(surface, res, startpt, endpt):
    surface.fill((255, 255, 255))
    mm, mandel_matrix = make_matrix(startpt[0], startpt[1], endpt[0], endpt[1], res)
    print len(mandel_matrix), len(mandel_matrix[0])
    pxa = pygame.PixelArray(surface)
    for i, x in enumerate(mandel_matrix):
        for j, y in enumerate(x):
            try:
                pxa[i][j] = (255 * y, 255 * y/2, 255 * y/3)
            except:
                print "i, j = ", i, j
                print "len(mm), len(x) = ", len(mandel_matrix), len(x)

    s = pxa.make_surface()
    del pxa
    surface.blit(s, pygame.Rect((0, 0), (100, 100)))
    return mm

def mandelbrot(z, base_c, curr_iter=0, max_iterations=MAX_ITERATIONS, max_divergence=MAX_DIVERGENCE):
    if curr_iter > max_iterations:
        return 1
    elif abs(z.real) > max_divergence:
        return curr_iter / max_iterations
    return mandelbrot(z**2 + base_c, base_c, curr_iter + 1, max_iterations, max_divergence)


if __name__ == "__main__":
    main()
