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


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(FLOOR_POS)
    pipes = [ Pipe(PIPE_DISTANCE) ]
    win = pygame.display.set_mode(( WIN_WIDTH, WIN_HEIGHT ))
    clock = pygame.time.Clock()

    score = 0
    
    run = True

    while run:
        clock.tick( FPS )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append( Pipe(PIPE_DISTANCE) )
            print(score)

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= FLOOR_POS:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)
    
    pygame.quit()
    quit()

main()