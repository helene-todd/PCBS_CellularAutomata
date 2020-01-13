#! /usr/bin/env python

from automaton import *
import argparse
import sys
import os

# Predefined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

# Initialise pygame
pygame.init()

# Argparse for a file
parser = argparse.ArgumentParser(description='Either a file or manually')
parser.add_argument("LIST", help="Arguments stored in list, or just nothing", nargs="*")
args = parser.parse_args()

if not any(vars(args).values()):
    grid = [['1' if random.random() < 0.33 else "0" for j in range(12)] for j in range(12)]
elif os.path.exists(args.LIST[0]):
    with open(args.LIST[0], 'r') as f:
        grid = [line.replace('\n','').split(' ') for line in f]
else :
    print('Wrong arguments : please specify text file path (grids/file.txt) or nothing.')
    sys.exit()


# Number of columns/ rows
columns = len(grid[0])
rows = len(grid)

# Length of one cell
l = (int((4./5)*pygame.display.Info().current_h/max(columns, rows)))
# Margin (size of space between cells)
m = (int(0.04*l))
# Width, height of screen
H, W = rows*(l+m)+m, columns*(l+m)+m

# Title of window
pygame.display.set_caption('Game of Life')
# Define screen of window
screen = pygame.display.set_mode((W, H), pygame.DOUBLEBUF)
# Fill screen with gray background
screen.fill(GRAY)

# Initialise font to adapt to screen size
font = pygame.font.Font('freesansbold.ttf', int(min(H,W)/20))

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
automata_list = Automata_list(grid, l, m)

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
