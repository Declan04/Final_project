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
player = sprites.Player(500, 500, TILE_SIZE, layout_tiles)
player_group.add(player)
enemy_group = layout1.get_enemy_group()
enemy_list = enemy_group.sprites()
coin_group = layout1.get_coin_group()
# coin_list = coin_group.sprites()
coin_list = layout1.get_coin_group()
HEALTH_TEXT = HEALTH_FONT.render(f'3', True, WHITE)
POINTS_TEXT = POINTS_FONT.render(f'0', True, WHITE)
life_counter = 3
points = 0
blank = pg.Surface((30, 30))
blank.fill(RED)
while playing:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:  # allow for q key to quit the game
            if event.key == pygame.K_q:
                playing = False
            if event.key == pygame.K_UP and not player.jumping:
                player.jump()

    enemy_collisions = pygame.sprite.spritecollide(player, enemy_group, True)
    if enemy_collisions:
        # if player == enemy_collisions:
        life_counter -= 1
        HEALTH_TEXT = HEALTH_FONT.render(f'{life_counter}', True, WHITE)
        player.kill()
        player = sprites.Player(500, 500, TILE_SIZE, layout_tiles)
        player_group.add(player)
    if life_counter == 0:
        player.kill()
        playing = False

    for tile in layout_tiles:
        if tile[-1] == 'COIN':
            if tile[1].colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                points += 10
                POINTS_TEXT = POINTS_FONT.render(f'{points}', True, WHITE)
                tile = (blank, (player.rect.x, player.rect.y), '')

    screen.fill(BLUE)
    layout1.update(screen)
    screen.blit(HEALTH_TEXT, (25, 25))
    player_group.update(screen)
    enemy_group.update(screen)
    # coin_group.update(screen)
    screen.blit(POINTS_TEXT, (100, 25))

    pygame.display.flip()

pygame.quit()
