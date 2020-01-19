#! /usr/bin/env python

import pygame, random
random.seed()

class CellularAutomaton() :
    """
    The CellularAutomaton object structures how cells behave

    Attributes:
        columns (int): number of cells in column
        rows (int) : number of cells in row
        list (list) : list of how cells are displayed
    """

    def __init__(self, grid, l, m, rules):
        """
        Constructor for CellularAutomaton object

        Args:
        grid: 2 dimensional list of 0s and 1s
        l: side length of an cell
        m: margin between cells
        rules: list of rules
        """
        self.columns = len(grid[0])
        self.rows = len(grid)
        self.list = [[None]*self.columns for k in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.columns):
                if grid[row][col] == '1' :
                    self.list[row][col] = Cell(row, col, l, m, "alive", rules)
                else :
                    self.list[row][col] = Cell(row, col, l, m, "dead", rules)
        self.count_neighbours()


    def display(self, screen):
        """
        Display all the cells in CellularAutomaton on screen

        Args:
        screen: the screen on which to display
        """
        for row in self.list:
            for element in row:
                element.display(screen)


    def reset_neighbours(self):
        """
        Reset the number of neighbours for each cell to zero
        """
        for row in self.list:
            for element in row:
                element.neighbours = 0


    def count_neighbours(self):
        """
        Count the number of neighbours for each cell
        """
        nb_rows = len(self.list)
        nb_columns = len(self.list[0])

        for i in range(self.rows):
            for j in range(self.columns):
                # Right
                if self.list[i][(j+1)%nb_columns].isAlive() :
                    self.list[i][j].neighbours += 1
                # Left
                if self.list[i][j-1].isAlive() :
                    self.list[i][j].neighbours += 1
                # Down
                if self.list[(i+1)%nb_rows][j].isAlive() :
                    self.list[i][j].neighbours += 1
                # Up
                if self.list[i-1][j].isAlive() :
                    self.list[i][j].neighbours += 1
                # Down Left
                if self.list[(i+1)%nb_rows][(j+1)%nb_columns].isAlive() :
                    self.list[i][j].neighbours += 1
                # Down Right
                if self.list[(i+1)%nb_rows][j-1].isAlive() :
                    self.list[i][j].neighbours += 1
                # Upper Right
                if self.list[i-1][(j+1)%nb_columns].isAlive() :
                    self.list[i][j].neighbours += 1
                # Upper Left
                if self.list[i-1][j-1].isAlive() :
                    self.list[i][j].neighbours += 1


    def update(self):
        """
        Update each cell in CellularAutomaton to new state
        """
        for row in self.list:
            for element in row:
                element.update()
        self.reset_neighbours()
        self.count_neighbours()


class Cell(pygame.sprite.Sprite):
    """
    The Cellular object contains all the information about one cell

    Attributes:
        width (int): width lenghth of cell
        height (int): height length of cell
        x (float): x coordiante of cell
        y (float): y coordiante of cell
        state (str): cell is "alive" or "dead"
        rules (list): set of rules the cell obeys
        happy (bool): cell is happy of sad
        newborn (bool): cell has just been born or not
        neighbours (int): number of immediate surrounding neighbours
        image (pygame.image): image associated to cell (happy/ sad face)
        color (pygame.Color): color of cell (pink/ blue)
    """

    def __init__(self, row, column, length, margin, state, rules):
        """
        Constructor for Cell object

        Args:
        row: row position in CellularAutomaton list
        column: column position in CellularAutomaton list
        length: side length of cell
        margin: space between two cells
        state: "alive" or "dead"
        rules: list of rules
        """

        # Call superclass constructor
        super().__init__()

        # Position of Cell on screen
        self.x, self.y = margin + column*(length + margin), margin + row*(length + margin)
        # Size of Cell (it's a square)
        self.width, self.height = length, length
        # State of Cell
        self.state = state
        # Rules cell will obey
        self.rules = rules
        # By default cell initialised at sad
        self.happy = False
        # By default cell begins as newborn
        self.newborn = True
        # By default cell initialised as having no neighbours
        self.neighbours = 0


    def display(self, screen):
        """
        Display cell on screen depending on current attributes

        Args:
        screen: the screen on which to display
        """
        if self.state == "alive" :
            # Cell is sad if it is isolated or overcrowded
            if self.neighbours < self.rules[0] or self.neighbours > self.rules[1]:
                self.happy = False
                if self.newborn != True :
                    self.color = pygame.Color('#70eeff')
                elif self.newborn == True :
                    self.color = pygame.Color('#bcf7ff')
                    self.newborn = False
                self.image = pygame.image.load('sad_square.png').convert_alpha()
            else :
                self.happy = True
                if self.newborn != True :
                    self.color = pygame.Color('#fd8eff')
                elif self.newborn == True :
                    self.color = pygame.Color('#fed1ff')
                    self.newborn = False
                self.image = pygame.image.load('happy_square.png').convert_alpha()

            # Redimension image while keeping a good quality
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            # Get image rectangle and position it on screen
            self.rect =  self.image.get_rect(left = self.x, top = self.y)
            # Draw coloured rectangle on screen
            pygame.draw.rect(screen, self.color, self.rect)
            # Blit coloured rectangle with image together
            screen.blit(self.image, self.rect)


    def update(self) :
        """
        Update cell
        """
        # If cell is alive but sad, it will die. No changes for happy cells.
        if self.state == "alive" and self.happy == False:
            self.state = "dead"
            self.newborn = False

        # If empty cell has exactly rule[2] neighbours it will be born
        elif self.state == "dead" :
            if self.neighbours == self.rules[2] :
                self.state = "alive"
                self.newborn = True


    def isAlive(self):
        """
        Accessor to cell state

        Returns:
            True if cell is "alive", False otherwise
        """
        return self.state == "alive"
