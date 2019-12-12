#! /usr/bin/env python

'''This code does not do anything really interesting, it's just to test out some of the basics in pygame and figure out how to implement
the evolution of an automaton graphically. The next step is to code an automaton class, maybe using the sprites from pygame'''

import pygame  # see www.pygame.org
import sys
import os
import math
import random
import math
import psutil

# So it works on windows too
#pathfile=os.path.join()
#os.path.join("folder", file) #folder name then file name
#print(pathfile)
#rootTree.write(os.path.join(pathfile,"output","log.txt"))

warm_colors = ['#FFA8A8','#FFACEC','#FFA8D3','#FEA9F3','#EFA9FE','#E7A9FE','#C4ABFE']
cold_colors = ['#BBBBFF','#BBDAFF','#CEF0FF','#ACF3FD','#B5FFFC','#A5FEE3','#B5FFC8']

happy = [pygame.Color(x) for x in warm_colors]
sad = [pygame.Color(x) for x in cold_colors]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

#l = 50  # square side length
  # space between squares
n = 10  # number of columns and rows
l = int((4./5)*pygame.display.Info().current_h/n)
e = int(650/(n*20))
print("L="+str(l))

W, H = n*(l+e)+e, n*(l+e)+e  # graphic window size

# set the pygame window name
pygame.display.set_caption('Game of Life')
screen = pygame.display.set_mode((H, W), pygame.DOUBLEBUF)
screen.fill(GRAY)

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Press enter to start', True, BLACK)
textRect = text.get_rect()
textRect.center = (W // 2, H // 2)

#print(type(textRect))

screen.blit(text, textRect)


pygame.display.update()


# wait till the window is closed
while True :

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        screen.fill(BLACK)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:


            for row in range(n):
                for col in range(n):
                    img = pygame.image.load('happy_square.png').convert_alpha()

                    left, top = e+col*(l+e), e+row*(l+e)
                    myrect = pygame.Rect(left, top, l, l)
                    pygame.draw.rect(screen, random.choice(happy+sad), myrect)

                    img = pygame.transform.smoothscale(img, (l, l))

                    #rect = img.get_rect()
                    #rect = rect.move((left, top))
                    screen.blit(img, myrect)


            pygame.display.update()

        process = psutil.Process(os.getpid())
        print(process.memory_info().rss)  # in bytes, to see how much memory is used

        if event.type == pygame.QUIT :

            # deactivate the pygame library
            pygame.quit()

            # quit the program.
            quit()
