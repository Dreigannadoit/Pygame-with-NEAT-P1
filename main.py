import neat.config
import pygame
import neat
import time
import os
import random
pygame.font.init()

from base import Base
from bird import Bird
from pipe import Pipe
from constants import BG_IMG, FLOOR_POS, FPS, PIPE_DISTANCE, STAT_FONT, WIN_WIDTH, WIN_HEIGHT, GEN


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win)
        
    pygame.display.update()

def main( genomes, config ):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append( Bird(230, 350) )
        g.fitness = 0
        ge.append(g)



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
                pygame.quit()
                quit()

        pipe_ind = 0

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.05

            output = nets[x].activate(  
                (
                    bird.y, 
                    abs( bird.y - pipes[pipe_ind].height ), 
                    abs( bird.y - pipes[pipe_ind].bottom ) 
                ) 
            )

            if output[0] > 0.5:
                bird.jump()


        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds): 
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)


                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()
        
        if add_pipe:
            score += 1

            for g in ge:
                g.fitness += 1

            pipes.append( Pipe(PIPE_DISTANCE) )
            print(score)

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds): 
            if bird.y + bird.img.get_height() >= FLOOR_POS or bird.y < 0:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)
    
    


def run(config_path):
    config = neat.config.Config( 
        neat.DefaultGenome, 
        neat.DefaultReproduction, 
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)

    p.add_reporter( neat.StdOutReporter(True) )
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # TODO: USE PICKLE TO SAVE THE BEST GENERATION OBJECT

    winner = p.run( main ,50 )


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)