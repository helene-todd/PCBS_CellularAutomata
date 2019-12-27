#! /usr/bin/env python

import pygame, random
random.seed()

class Automata_list() :
    def __init__(self, n, l, m, proportion):
        self.n = n
        self.list = [[None]*n for k in range(n)]
        for row in range(n):
            for col in range(n):
                if random.random() < proportion :
                    self.list[row][col] = Automaton(row, col, l, m, "alive")
                else :
                    self.list[row][col] = Automaton(row, col, l, m, "dead")
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
        for i in range(self.n):
            for j in range(self.n):
                # Right
                if j < self.n-1 and self.list[i][j+1] != None and self.list[i][j+1].isAlive():
                    self.list[i][j].neighbours += 1
                # Left
                if j > 0 and self.list[i][j-1] != None and self.list[i][j-1].isAlive():
                    self.list[i][j].neighbours += 1
                # Up
                if i < self.n-1 and self.list[i+1][j] != None and self.list[i+1][j].isAlive():
                    self.list[i][j].neighbours += 1
                # Down
                if i > 0 and  self.list[i-1][j] != None and self.list[i-1][j].isAlive():
                    self.list[i][j].neighbours += 1
                # Bottom Right
                if j < self.n-1 and i < self.n-1  and self.list[i+1][j+1] != None and self.list[i+1][j+1].isAlive():
                    self.list[i][j].neighbours += 1
                # Bottom Left
                if j > 0 and i < self.n-1  and self.list[i+1][j-1] != None and self.list[i+1][j-1].isAlive():
                    self.list[i][j].neighbours += 1
                # Top Left
                if j > 0 and i > 0 and self.list[i-1][j-1] != None and self.list[i-1][j-1].isAlive():
                    self.list[i][j].neighbours += 1
                # Top Right
                if j < self.n-1 and i > 0  and self.list[i-1][j+1] != None and self.list[i-1][j+1].isAlive():
                    self.list[i][j].neighbours += 1


    def update(self):
        for row in self.list:
            for element in row:
                element.update()
        self.reset_neighbours()
        self.count_neighbours()


class Automaton(pygame.sprite.Sprite):

    # Automaton constructor
    def __init__(self, row, column, length, margin, state):
        # Call superclass constructor
        super().__init__()

        # Position of Automaton on screen
        self.x, self.y = margin + column*(length + margin), margin + row*(length + margin)
        # Size of Automaton square
        self.width, self.height = length, length
        self.state = state

        self.happy = False
        self.sad = False

        self.neighbours = 0


    def display(self, screen):
        if self.state == "alive":
            if self.neighbours < 2 or self.neighbours > 3:
                self.sad = True
                self.color = pygame.Color('#67D0DD')
                self.image = pygame.image.load('sad_square.png').convert_alpha()
            else :
                self.happy = True
                self.color = pygame.Color('#DC95DD')
                self.image = pygame.image.load('happy_square.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            self.rect =  self.image.get_rect(left = self.x, top = self.y)
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.image, self.rect)


    def update(self) :
        if self.state == "alive" and self.sad == True:
            self.state = "dead"
            self.happy, self.sad = False, False

        elif self.state == "dead" :
            if self.neighbours == 3 :
                self.state = "alive"


    def isAlive(self):
        return self.state == "alive"
