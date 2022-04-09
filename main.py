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
LIGHT_BLUE = (135, 206, 250)

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
screen.fill(WHITE)

running = True
drawing = True
colorInd = 3

simple_fill = False
line_fill = False
stack = []
lastMouseMotion = None
filled = 0
poped = 0

drawColours = {1: DARK_GRAY, 2: LIGHT_BLUE, 3: WHITE}

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
            mousePos = event.pos
            indF = floor(mousePos[1] * pHeight / height)
            indS = floor(mousePos[0] * pWidth / width)
            drawMatrix[indF][indS] = colorInd
            colorInd = event.button
        elif event.type == MOUSEBUTTONUP:
            drawing = False
        elif event.type == MOUSEMOTION and drawing:
            mousePos = event.pos
            indF = floor(mousePos[1] * pHeight / height)
            indS = floor(mousePos[0] * pWidth / width)
            drawMatrix[indF][indS] = colorInd
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                simple_fill = False
                line_fill = False
                filled = 0
                poped = 0
                drawMatrix = []
                for i in range(0, pHeight):
                    row = [3] * pWidth
                    drawMatrix.append(row)
                print('Сброс всего')
            if event.key == pygame.K_1 or event.key == pygame.K_2:
                if not line_fill and not simple_fill:
                    if event.key == pygame.K_1:
                        simple_fill = True
                    if event.key == pygame.K_2:
                        line_fill = True
                    mousePos = pygame.mouse.get_pos()
                    indF = floor(mousePos[1] * pHeight / height)
                    indS = floor(mousePos[0] * pWidth / width)
                    stack.append((indF, indS))

    if simple_fill:
        if len(stack) == 0:
            simple_fill = False
            print('Все закрашено!')
            print(f'Закрашено пикселей: {filled}')
            print(f'Всего было в стеке пикселей: {poped}')
            print(f'Зря побывало в стеке пикселей: {(((poped - filled) * 100) / poped):.2f} %')
            filled = 0
            poped = 0
        else:
            pixel = stack.pop(-1)
            y, x = pixel
            print(f'Вытащил пиксель: {(x, y)}')
            poped += 1
            if drawMatrix[y][x] != 2:
                drawMatrix[y][x] = 2
                print('Закрасил его')
                filled += 1
            if y + 1 < pHeight and drawMatrix[y + 1][x] != 2 and drawMatrix[y + 1][x] != 1:
                stack.append((y + 1, x))
                print('Добавил пиксель снизу')
            if x + 1 < pWidth and drawMatrix[y][x + 1] != 2 and drawMatrix[y][x + 1] != 1:
                stack.append((y, x + 1))
                print('Добавил пиксель справа')
            if y - 1 >= 0 and drawMatrix[y - 1][x] != 2 and drawMatrix[y - 1][x] != 1:
                stack.append((y - 1, x))
                print('Добавил пиксель сверху')
            if x - 1 >= 0 and drawMatrix[y][x - 1] != 2 and drawMatrix[y][x - 1] != 1:
                stack.append((y, x - 1))
                print('Добавил пиксель слева')


    if line_fill:
        pass


    for w in range(0, pWidth):
        for h in range(0, pHeight):
            start = [round(i) for i in (w * width / pWidth, h * height / pHeight)]
            end = [round(i) for i in ((w + 1) * width / pWidth, (h + 1) * height / pHeight)]
            size = end[0] - start[0], end[1] - start[1]
            pygame.draw.rect(screen, drawColours.get(drawMatrix[h][w]), (start, size))
            pygame.draw.rect(screen, GRAY, (start, size), 1)

    printFPS(False)
    pygame.display.update()

pygame.quit()
