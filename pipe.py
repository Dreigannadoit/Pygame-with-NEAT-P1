import pygame
import neat
import time
import os
import random

from constants import PIPE_IMG

class Pipe:
    GAP = 200
    BASE_VEL = 10

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.VEL = self.BASE_VEL 

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange( 50, 450 )

        # find the position of the pipe ( draw on - local )
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
    
    @classmethod
    def increase_velocity(cls, increment):
        cls.BASE_VEL += increment

    def draw(self, win):
        win.blit( self.PIPE_TOP, ( self.x, self.top ) )
        win.blit( self.PIPE_BOTTOM, ( self.x, self.bottom ) )

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = ( self.x - bird.x, self.top - round( bird.y ) )
        bottom_offset = ( self.x - bird.x, self.bottom - round( bird.y ) )

        b_point = bird_mask.overlap( bottom_mask, bottom_offset )
        t_point = bird_mask.overlap( top_mask, top_offset )

        if t_point or b_point:
            return True
        
        return False
    