#! /usr/bin/env python

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from automaton import *
import sys
import os

# Predefined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)


# Argparse arguments
parser = ArgumentParser(description='''A simulation of Conway's Game of Life in a finite space. This program shows how cellular automaton evolve
in a deterministic way depending on the starting grid and set of rules.''', formatter_class=RawTextHelpFormatter)
parser.add_argument('-s', '--size',
    help='specify size for randomly generated initial grid \n'
    '  takes 2 integer arguments : row_size column_size', nargs=2, metavar='int', type=int)
parser.add_argument('-p', '--proportion',
    help='specify proportion of cells on initial grid \n'
    '   takes 1 integer argument : proportion (between 0 and 1)', nargs=1, metavar='float', type=float)
parser.add_argument('-f', '--file',
    help='specify a text file as starting grid \n'
    '   takes 1 argument : path to .txt file', nargs=1, metavar='path', type=str)
parser.add_argument('-r', '--rules', help='specify rules of game\n'
    '   takes 3 integer arguments x y z : \n'
    '     - 1st argument x : cell dies if strictly less than x neighbours\n'
    '     - 2nd argument y : cell dies if strictly more than y neighbours\n'
    '     - 3rd argument z : cell is born if exactly z neighbours\n', nargs=3, metavar='int', type=int)
args = parser.parse_args()

# String that stores argparse values
str_arguments = ""

# Check arguments for initial grid
if args.file is not None : #need to test on windows
    if os.path.exists(args.file[0]):
        str_arguments = f"File opened : {args.file[0]} \n"
        with open(args.file[0], 'r') as f:
            grid = [line.replace('\n','').split(' ') for line in f if line !='\n']
    else:
        print("Error : path to file does not appear to exist")
        sys.exit(0)
elif args.size is not None :
    str_arguments = f"File opened : None \n"
    p = .33
    if args.proportion is not None and args.proportion[0] >= 0 and args.proportion[0] <= 1 :
        p = args.proportion[0]
    grid = [['1' if random.random() < p else '0' for i in range(args.size[1])] for j in range(args.size[0])]
    str_arguments += f"Proportion of cells : {p} \n"
    str_arguments += f"Grid size : {args.size[0]} rows x {args.size[1]} columns \n"
else :
    p = .33
    if args.proportion is not None and args.proportion[0] >= 0 and args.proportion[0] <= 1 :
        p = args.proportion[0]
    grid = [['1' if random.random() < p else '0' for i in range(16)] for j in range(16)] # Default grid
    str_arguments += f"Proportion of cells : {p} \n"
    str_arguments += "Grid size : 16 rows x 16 columns \n"

# Check arguments for special rules
if args.rules is not None :
    rules = [args.rules[0], args.rules[1], args.rules[2]]
else :
    rules = [2,3,3] # Default rules
str_arguments += f"Rules : {rules} \n"


# Number of columns/ rows
columns = len(grid[0])
rows = len(grid)

# Initialise pygame
pygame.init()

# Length of one cell depending on row to column ratio (to define an appropriate size on screen)
l = min(int((4./5)*pygame.display.Info().current_h/rows), int((4./5)*pygame.display.Info().current_w/columns))
# Margin (size of space between cells)
m = (int(0.04*l))
# Width, height of window
H, W = rows*(l+m)+m, columns*(l+m)+m

# Title of window
pygame.display.set_caption('Game of Life')
# Define screen of window
screen = pygame.display.set_mode((W, H), pygame.DOUBLEBUF)
# Fill screen with gray background
screen.fill(GRAY)

# Initialise font to adapt to screen size
font = pygame.font.Font('freesansbold.ttf', int(W/18))

# Initialise the text
text = font.render('Press [space bar] to start / pause', True, BLACK)
# Get the rectangle that contains the text
textRect = text.get_rect()
# Center text in middle of screen using rectangle
textRect.center = (W // 2, H // 2)
# Blit text and rectangle together
screen.blit(text, textRect)
# Update Screen
pygame.display.update()


# New cellular automaton
automaton = CellularAutomaton(grid, l, m, rules)

# Initialise pygame's clock
clock = pygame.time.Clock()

# Avoid errors related to event
pygame.event.clear()

# Animation hasn't started yet
start = False

# Creating folder to save screen captures and used arguments
if os.path.isdir('screen_captures') :
    os.system("rm -rf screen_captures")
os.mkdir(f'screen_captures')
with open('screen_captures/optional_arguments.txt','w') as f:
    f.write(str_arguments)


i = 0
# Arbitrary upper bound for number of screen captures
bound = columns*rows
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
        automaton.display(screen)
        pygame.display.update()
        automaton.update()

        if i <= bound :
            pygame.image.save(screen, f"screen_captures/{i}.jpeg")
            i += 1
