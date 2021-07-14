import pygame
import os
import numpy as np
import random
import math
import copy

##os.environ['SDL_VIDEODRIVER'] = 'directx'

pygame.mixer.pre_init(44100, 16, 8, 4096)
pygame.init()
dwidth = 1280
dheight = 720
gameDisplay = pygame.display.set_mode((dwidth, dheight))
pygame.display.set_caption('Path')
clock = pygame.time.Clock()
level = 1
nodeNumber = 0
nodes = -1
nodeList = []

lvl1 = pygame.transform.smoothscale(pygame.image.load('files/glvl1.jpg'), (1280,720))
lvl2 = pygame.image.load('files/glvl2.jpg')
lvl3 = pygame.image.load('files/glvl3.jpg')
lvl4 = pygame.image.load('files/glvl4.jpg')
lvl5 = pygame.image.load('files/glvl5.jpg')
node = pygame.transform.smoothscale(pygame.image.load('files/node.png'), (160, 90))
startend = pygame.transform.smoothscale(pygame.image.load('files/startend.png'), (320, 180))
successimg = pygame.image.load('files/successimage2.png')
failureimg = pygame.image.load('files/failureimage2.png')
path = pygame.image.load('files/path.png')
howto = pygame.image.load('files/howto3.png')
completionScreen = pygame.image.load('files/completion.jpg')

successSound = pygame.mixer.Sound('files/successSound.wav')
failureSound = pygame.mixer.Sound('files/failureSound.wav')
failureSound.set_volume(5000)
placementSound = pygame.mixer.Sound('files/placementSound.wav')
bard = pygame.mixer.Sound('files/bard.wav')
bard.set_volume(0.5)
nature = pygame.mixer.Sound('files/nature.wav')
nature.set_volume(0.5)
limitless = pygame.mixer.Sound('files/limitless.wav')
limitless.set_volume(0.5)
calm = pygame.mixer.Sound('files/calm.wav')
calm.set_volume(0.5)

musicArray = [bard, nature, limitless, calm]

class Node:
    def __init__(self, number, x, y, active):
        self.number = number
        self.x = x
        self.y = y
        self.active = active

startNode = Node(0, 10000, 10000, False)
endNode = Node(0, 10000, 10000, False)

def place(a,x,y):
    gameDisplay.blit(a, (x,y))

def centralPlace(a,cx,cy):
    gameDisplay.blit(a, (cx-(a.get_width()/2), cy-(a.get_height()/2)))

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, n, m, size, font, color):
    font = pygame.font.SysFont(font, size)
    ##largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, font, color)
    TextRect.center = (int(n)),(int(m))
    gameDisplay.blit(TextSurf, TextRect)

def collision(a,b,c,d):
    global level
    rects = []
    collision = False
    if level == 1:
        rect1 = pygame.Rect(222,116.667,757.333,84.667)
        rect2 = pygame.Rect(361.333,172,68,200.667)
        rect3 = pygame.Rect(782,334,74,340)
        rect4 = pygame.Rect(996,262,222,62)
        rects.append(rect1)
        rects.append(rect2)
        rects.append(rect3)
        rects.append(rect4)
    elif level == 2:
        rect1 = pygame.Rect(958,150,117,579)
        rect2 = pygame.Rect(217,12,682,85)
        rect3 = pygame.Rect(270,16,88,554)
        rects.append(rect1)
        rects.append(rect2)
        rects.append(rect3)
    elif level == 3:
        rect1 = pygame.Rect(265,91,77,640)
        rect2 = pygame.Rect(607,31,65,262)
        rect3 = pygame.Rect(763,44,52,205)
        rect4 = pygame.Rect(1014,97,46,150)
        rect5 = pygame.Rect(561,231,685,65)
        rects.append(rect1)
        rects.append(rect2)
        rects.append(rect3)
        rects.append(rect4)
        rects.append(rect5)
    elif level == 4:
        rect1 = pygame.Rect(296,33,95,194)
        rect2 = pygame.Rect(607,-6,63,147)
        rect3 = pygame.Rect(966,94,108,95)
        rect4 = pygame.Rect(1140,130,146,57)
        rect5 = pygame.Rect(416,244,736,53)
        rect6 = pygame.Rect(1117,336,169,46)
        rect7 = pygame.Rect(692,433,462,95)
        rect8 = pygame.Rect(586,556,84,179)
        rects.append(rect1)
        rects.append(rect2)
        rects.append(rect3)
        rects.append(rect4)
        rects.append(rect5)
        rects.append(rect6)
        rects.append(rect7)
        rects.append(rect8)
    elif level == 5:
        rect1 = pygame.Rect(420,534,865,48)
        rect2 = pygame.Rect(-16,416,442,54)
        rect3 = pygame.Rect(284,190,59,238)
        rect4 = pygame.Rect(330,300,175,31)
        rect5 = pygame.Rect(181,207,120,17)
        rect6 = pygame.Rect(118,65,19,162)
        rect7 = pygame.Rect(432,73,45,177)
        rect8 = pygame.Rect(118,60,1128,22)
        rects.append(rect1)
        rects.append(rect2)
        rects.append(rect3)
        rects.append(rect4)
        rects.append(rect5)
        rects.append(rect6)
        rects.append(rect7)
        rects.append(rect8)

    m = (d-b)/(c-a)
    ##print(rects)
    j = 0
    if c - a >= 1:
        j = 1
    else:
        j = -1
    for xx in range(round(a),round(c),j):
        yy = m*(xx-a) + b
        for rectangulo in rects:
            if rectangulo.collidepoint((xx,yy)):
                collision = True
    ##print(collision)
    return collision


def titleLoop():
    n = 0.01
    end = False
    startTime = pygame.time.get_ticks()
    t1 = False
    x1 = dwidth/2
    y1 = dheight/2
    x2 = dwidth/2
    y2 = dheight*3/2
    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                end = True
        fps = 1000/n
        gameDisplay.fill((113,113,113))
        centralPlace(path, x1, y1)
        centralPlace(howto, x2, y2)
        if pygame.time.get_ticks() - startTime >= 5000 and pygame.time.get_ticks() - startTime <= 10000:
            t1 = True
        else:
            t1 = False
        if t1:
            y1 = y1 - 45/(fps+0.01)
            y2 = y2 - 150/(fps+0.01)
        pygame.display.update()
        n = clock.tick()



def gameLoop():
    global level
    global nodes
    global nodeNumber
    global nodeList
    global startNode
    global endNode
    end = False
    failure = False
    success = False
    if level == 1:
        nodes = 2
        nodeNumber = 0
        node1 = Node(1, 10000, 10000, False)
        node2 = Node(2, 10000, 10000, False)
        nodeList.clear()
        nodeList.append(node1)
        nodeList.append(node2)
        startNode.x = 1200
        startNode.y = 650
        startNode.active = True
        endNode.x = 80
        endNode.y = 340
        endNode.active = True
    elif level == 2:
        nodes = 2
        nodeNumber = 0
        node1 = Node(1, 10000, 10000, False)
        node2 = Node(2, 10000, 10000, False)
        nodeList.clear()
        nodeList.append(node1)
        nodeList.append(node2)
        startNode.x = 1200
        startNode.y = 650
        startNode.active = True
        endNode.x = 110
        endNode.y = 160
        endNode.active = True
    elif level == 3:
        nodes = 2
        nodeNumber = 0
        node1 = Node(1, 10000, 10000, False)
        node2 = Node(2, 10000, 10000, False)
        nodeList.clear()
        nodeList.append(node1)
        nodeList.append(node2)
        startNode.x = 1200
        startNode.y = 650
        startNode.active = True
        endNode.x = 917
        endNode.y = 170
        endNode.active = True
    elif level == 4:
        nodes = 2
        nodeNumber = 0
        node1 = Node(1, 10000, 10000, False)
        node2 = Node(2, 10000, 10000, False)
        nodeList.clear()
        nodeList.append(node1)
        nodeList.append(node2)
        startNode.x = 1200
        startNode.y = 650
        startNode.active = True
        endNode.x = 762
        endNode.y = 46
        endNode.active = True

    elif level == 5:
        nodes = 4
        nodeNumber = 0
        node1 = Node(1, 10000, 10000, False)
        node2 = Node(2, 10000, 10000, False)
        node3 = Node(3, 10000, 10000, False)
        node4 = Node(4, 10000, 10000, False)
        nodeList.clear()
        nodeList.append(node1)
        nodeList.append(node2)
        nodeList.append(node3)
        nodeList.append(node4)
        startNode.x = 1200
        startNode.y = 650
        startNode.active = True
        endNode.x = 134
        endNode.y = 377
        endNode.active = True

    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if nodeNumber < len(nodeList):
                        clickX = pygame.mouse.get_pos()[0]
                        clickY = pygame.mouse.get_pos()[1]
                        nodeList[nodeNumber].active = True
                        nodeList[nodeNumber].x = clickX
                        nodeList[nodeNumber].y = clickY
                        nodeNumber = nodeNumber + 1
                        pygame.mixer.Channel(4).play(placementSound)



        if level == 1:
            centralPlace(lvl1, 640, 360)
        elif level == 2:
            centralPlace(lvl2, 640, 360)
        elif level == 3:
            centralPlace(lvl3, 640, 360)
        elif level == 4:
            centralPlace(lvl4, 640, 360)
        elif level == 5:
            centralPlace(lvl5, 640, 360)

        if level == 5:
            pygame.draw.rect(gameDisplay,(150,150,150),(0,640,130,80))
            centralPlace(node, 50, 680)
            message_display("x" + str(nodes - nodeNumber), 85, 680, 20, 'verdana', (0,0,0))
            message_display("Press Q to quit game", 190,705, 10, 'verdana', (0,0,0))
        else:
            pygame.draw.rect(gameDisplay,(150,150,150),(0,0,130,80))
            centralPlace(node, 50, 40)
            message_display("x" + str(nodes - nodeNumber), 85, 40, 20, 'verdana', (0,0,0))
            message_display("Press Q to quit game", 65,705, 10, 'verdana', (0,0,0))

        centralPlace(startend, startNode.x, startNode.y)
        centralPlace(startend, endNode.x, endNode.y)

        # rect1 = pygame.Rect(222,116.667,757.333,84.667)
        # rect2 = pygame.Rect(361.333,172,68,200.667)
        # rect3 = pygame.Rect(782,334,74,340)
        # rect4 = pygame.Rect(996,262,222,62)
        # pygame.draw.rect(gameDisplay, (100,0,0), rect1)
        # pygame.draw.rect(gameDisplay, (100,0,0), rect2)
        # pygame.draw.rect(gameDisplay, (100,0,0), rect3)
        # pygame.draw.rect(gameDisplay, (100,0,0), rect4)
        for nodeus in nodeList:
            if nodeus.active == True:
                centralPlace(node, nodeus.x, nodeus.y)
            if nodeus.number == 1 and nodeus.active == True:
                pygame.draw.aaline(gameDisplay, (0,0,100), (startNode.x, startNode.y), (nodeus.x, nodeus.y), 9)
                col = collision(startNode.x, startNode.y, nodeus.x, nodeus.y)
                if col:
                    failure = True
                    end = True
            elif nodeus.number == nodes and nodeus.active == True:
                pygame.draw.aaline(gameDisplay, (0,0,100), (nodeList[nodeus.number -2].x, nodeList[nodeus.number -2].y), (nodeus.x, nodeus.y), 9)
                pygame.draw.aaline(gameDisplay, (0,0,100), (nodeus.x, nodeus.y), (endNode.x, endNode.y), 9)
                col = collision(nodeList[nodeus.number -2].x, nodeList[nodeus.number -2].y, nodeus.x, nodeus.y)
                col2 = collision(nodeus.x, nodeus.y, endNode.x, endNode.y)
                if col or col2:
                    failure = True
                    end = True
                else:
                    success = True
                    end = True
            else:
                if nodeus.active == True:
                    pygame.draw.aaline(gameDisplay, (0,0,100), (nodeList[nodeus.number -2].x, nodeList[nodeus.number -2].y), (nodeus.x, nodeus.y), 9)
                    col = collision(nodeList[nodeus.number -2].x, nodeList[nodeus.number -2].y, nodeus.x, nodeus.y)
                    if col:
                        failure = True
                        end = True
        pygame.display.update()
        clock.tick()

    if failure:
        failLoop()
    if success:
        successLoop()


def failLoop():
    pygame.mixer.Channel(3).play(failureSound)
    centralPlace(failureimg, dwidth/2, dheight/2)
    pygame.display.update()
    end = False
    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameLoop()

def successLoop():
    global level
    pygame.mixer.Channel(2).play(successSound)
    centralPlace(successimg, dwidth/2, dheight/2)
    pygame.display.update()
    end = False
    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                level = level + 1
                if level == 6:
                    completionLoop()
                else:
                    gameLoop()

def completionLoop():
    quit = False
    centralPlace(completionScreen, dwidth/2, dheight/2)
    pygame.display.update()
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()




titleLoop()
gameLoop()
