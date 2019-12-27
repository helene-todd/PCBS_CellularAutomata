#! /usr/bin/env python

from automaton import *

# Predefined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

# Initialise pygame
pygame.init()

# Number of columns/ rows
n = 10
# Length of one cell
l = int((4./5)*pygame.display.Info().current_h/n)
# Margin (size of space between cells)
m = int(0.04*l)
# Width, height of screen
W, H = n*(l+m)+m, n*(l+m)+m

# Title of window
pygame.display.set_caption('Game of Life')
# Define screen of window
screen = pygame.display.set_mode((H, W), pygame.DOUBLEBUF)
# Fill screen with gray background
screen.fill(GRAY)
# Write message in middle of screen
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Press enter to start', True, BLACK)
textRect = text.get_rect()
textRect.center = (W // 2, H // 2)
screen.blit(text, textRect)
# Update Screen
pygame.display.update()

# List of automata
automata_list = Automata_list(n, l, m, 0.33)

while True :

    for event in pygame.event.get():
        screen.fill(BLACK)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            automata_list.display(screen)
            pygame.display.update()
            automata_list.update()

        if event.type == pygame.QUIT :
            quit()
