import pygame
import neat
import time
import os
import random
pygame.font.init()

from base import Base
from bird import Bird
from pipe import Pipe
from constants import BG_IMG, FLOOR_POS, FPS, PIPE_DISTANCE, STAT_FONT, WIN_WIDTH, WIN_HEIGHT


class GameLoop:
    def __init__(self):
        self.bird = Bird(230, 350)
        self.base = Base(FLOOR_POS)
        self.pipes = [ Pipe(PIPE_DISTANCE) ]
        self.win = pygame.display.set_mode(( WIN_WIDTH, WIN_HEIGHT ))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.run = True

    def draw_window(self):
        self.win.blit(BG_IMG, (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.win)

        text = STAT_FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

        self.base.draw(self.win)
        self.bird.draw(self.win)

        pygame.display.update()

    def main(self):
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            # self.bird.move()  # Uncomment when bird movement logic is ready

            add_pipe = False
            rem = []
            for pipe in self.pipes:
                if pipe.collide(self.bird):
                    pass  # Handle collision logic here

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()
            
            if add_pipe:
                self.score += 1
                self.pipes.append( Pipe(PIPE_DISTANCE) )
                print(self.score)

            for r in rem:
                self.pipes.remove(r)

            if self.bird.y + self.bird.img.get_height() >= FLOOR_POS:
                pass  # Handle hitting the ground logic here

            self.base.move()
            self.draw_window()

        pygame.quit()
