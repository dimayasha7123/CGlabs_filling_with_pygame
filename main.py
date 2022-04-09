import math

import pygame
import time
from pygame.locals import *
from math import *

size = 1280, 720
width, height = size
pSize = 64, 36
pWidth, pHeight = pSize
drawMatrix = []
for i in range(0, pHeight):
    row = [3] * pWidth
    drawMatrix.append(row)

GRAY = (127, 127, 127)
DARK_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
DARK_GREEN = (21, 71, 52)

pygame.init()
prevTime = time.time()
fpsFont = pygame.font.SysFont('consolas.ttf', 36)


def printFPS(console=True):
    global prevTime
    currTime = time.time()
    fps = 'inf'
    try:
        fps = str(round(1 // (currTime - prevTime)))
    except:
        pass
    if console:
        print(f'FPS: {fps}')
    prevTime = currTime
    imgFps = fpsFont.render(str(fps), True, DARK_GREEN)
    screen.blit(imgFps, (5, 5))


screen = pygame.display.set_mode(size)
running = True
drawing = True
colorInd = 3

while running:
    for event in pygame.event.get():
        # print(event)

        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
            colorInd = event.button

            mousePos = event.pos
            indF = floor(mousePos[1] * pHeight / height)
            indS = floor(mousePos[0] * pWidth / width)

            drawMatrix[indF][indS] = colorInd
        elif event.type == MOUSEBUTTONUP:
            drawing = False
        elif event.type == MOUSEMOTION and drawing:

            mousePos = event.pos
            indF = floor(mousePos[1] * pHeight / height)
            indS = floor(mousePos[0] * pWidth / width)

            drawMatrix[indF][indS] = colorInd

    screen.fill(WHITE)

    for w in range(0, pWidth):
        for h in range(0, pHeight):
            # rect_color = GRAY if (w + h) % 2 == 0 else DARK_GRAY
            rect_color = GRAY
            start = [round(i) for i in (w * width / pWidth, h * height / pHeight)]
            end = [round(i) for i in ((w + 1) * width / pWidth, (h + 1) * height / pHeight)]
            size = end[0] - start[0], end[1] - start[1]
            pygame.draw.rect(screen, DARK_GRAY if drawMatrix[h][w] == 1 else WHITE, (start, size))
            pygame.draw.rect(screen, rect_color, (start, size), 1)

    printFPS(False)
    pygame.display.update()

pygame.quit()
