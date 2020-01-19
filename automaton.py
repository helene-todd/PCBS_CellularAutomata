#! /usr/bin/env python

import pygame, random
random.seed()

class Automata_list() :

    # Constructor for a display specified in text file
    def __init__(self, grid, l, m, rules):
        self.columns = len(grid[0])
        self.rows = len(grid)
        self.list = [[None]*self.columns for k in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.columns):
                if grid[row][col] == '1' :
                    self.list[row][col] = Automaton(row, col, l, m, "alive", rules)
                else :
                    self.list[row][col] = Automaton(row, col, l, m, "dead", rules)
        self.count_neighbours()


    def display(self, screen):
        for row in self.list:
            for element in row:
                element.display(screen)


    def reset_neighbours(self):
        for row in self.list:
            for element in row:
                element.neighbours = 0


    def count_neighbours(self):
        for i in range(self.rows):
            for j in range(self.columns):
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
        for row in self.list:
            for element in row:
                element.update()
        self.reset_neighbours()
        self.count_neighbours()

    def isAlive(self):
        alive = False
        for row in self.list:
            for element in row:
                if element.isAlive() :
                    alive = True
        return alive


class Automaton(pygame.sprite.Sprite):

    # Automaton constructor
    def __init__(self, row, column, length, margin, state, rules):
        # Call superclass constructor
        super().__init__()

        # Position of Automaton on screen
        self.x, self.y = margin + column*(length + margin), margin + row*(length + margin)
        # Size of Automaton square
        self.width, self.height = length, length
        self.state = state
        self.rules = rules

        self.happy = False

        self.newborn = True

        self.neighbours = 0

# TRY COLOURING NEWBORN IN WHITE/ CREME COLOUR

    def display(self, screen):
        if self.state == "alive" :
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

            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            self.rect =  self.image.get_rect(left = self.x, top = self.y)
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.image, self.rect)

    def update(self) :
        if self.state == "alive" and self.happy == False:
            self.state = "dead"
            self.newborn = False

        elif self.state == "dead" :
            if self.neighbours == self.rules[2] :
                self.state = "alive"
                self.newborn = True

    def isAlive(self):
        return self.state == "alive"
