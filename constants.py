import pygame
import os
pygame.font.init()


WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0
BIRD_IMGS = [ 
    pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "bird1.png" ))),
    pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "bird2.png" ))),
    pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "bird3.png" ))),
]
PIPE_IMG =  pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "pipe.png" )))
BASE_IMG =  pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "base.png" )))
BG_IMG =  pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs", "bg.png" )))

STAT_FONT = pygame.font.SysFont("8-BIT_WONDER.TTF", 50)

PIPE_DISTANCE = 600
FLOOR_POS = 730
FPS = 30