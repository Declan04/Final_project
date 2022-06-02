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
# coin_group = layout1.get_coin_group()
# coin_list = coin_group.sprites()
coin_list = layout1.get_coin_group()
HEALTH_TEXT = HEALTH_FONT.render(f'3', True, WHITE)
life_counter = 3

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

    # print(coin_group)
    # coin_collisions = pygame.sprite.spritecollide(player, coin_group, True)
    points = 0
    for tile in layout_tiles:
        if tile[-1] == 'COIN':
            if tile[1].colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                print('HIT')
                # coin_group.kill()
        # points += 10
        # print(points)

    # def lives(self):
    #     life_counter = 3
    #
    #     if player == enemy_collisions:
    #         life_counter -= 1
    #     if life_counter == 0:
    #         player.kill()
    #         print(lives(player))

    # exit_collisions = pygame.sprite.spritecollide(player, exit_grp, True)
    # if exit_collisions:
    #     print(layout2)

    screen.fill(BLUE)
    layout1.update(screen)
    screen.blit(HEALTH_TEXT, (25,25))
    player_group.update(screen)
    enemy_group.update(screen)
    # coin_group.update(screen)

    pygame.display.flip()

pygame.quit()
