#! /usr/bin/env python

from automaton import *

# Predefined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

# Initialise pygame
pygame.init()

# Number of columns/ rows
n = 16
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

# Initialise font to adapt to screen size
font = pygame.font.Font('freesansbold.ttf', int(H/20))

# Initialise the text
text = font.render('Press [spacebar] to start / pause', True, BLACK)

# Get the rectangle that contains the text
textRect = text.get_rect()

# Center text in middle of screen using rectangle
textRect.center = (W // 2, H // 2)

# Blit the text and rectangle together
screen.blit(text, textRect)

# Update Screen
pygame.display.update()

# List of automata
automata_list = Automata_list(n, l, m, 0.33)

# Initialise pygame's clock
clock = pygame.time.Clock()

# Avoid errors
pygame.event.clear()

# Animation hasn't started yet
start = False

while True:

    # Clock delay
    clock.tick(2)

    for event in pygame.event.get():

        # Quit program
        if event.type == pygame.QUIT :
            quit()

        # When space key is pressed start/ pause the animation
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = not start

    # Start/ pause when space bar has been pressed
    if start == True:

        screen.fill(BLACK)
        automata_list.display(screen)
        pygame.display.update()
        automata_list.update()
