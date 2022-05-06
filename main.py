import pygame
import sprites
from settings import *

playing = True

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Final Game")
clock = pygame.time.Clock()
layout1 = sprites.Layout(screen)
layout_tiles = layout1.get_tiles()
player_group = pygame.sprite.GroupSingle()
player = sprites.Player(100, 500, TILE_SIZE, layout_tiles)
player_group.add(player)
xxmmm
while playing:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:  # allow for q key to quit the game
            if event.key == pygame.K_q:
                playing = False

    screen.fill(BLUE)
    layout1.update(screen)
    player.update(screen)

    pygame.display.flip()

pygame.quit()
