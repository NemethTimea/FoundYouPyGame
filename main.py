import pygame
from UI.ScreenFade import ScreenFade

import World, Game
from consts import *
from helpers import *

pygame.init()
pygame.display.set_caption("Founder")

game = Game.Game()

clock = pygame.time.Clock()

start_game = False

run = True
while run:
    clock.tick(FPS)
    if start_game == False:
        #draw menu
        SCREEN.fill(BG)
        if start_button.draw(SCREEN):
            start_game = True
            game.start()
        if exit_button.draw(SCREEN):
            run = False
    else:
        game.update()
        game.handle_fades()
        game.handle_game()
        game.handle_collides()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                game.moving_left = True
            if event.key == pygame.K_d:
                game.moving_right = True
            if event.key == pygame.K_q:
                game.throw_rock = True
            if event.key == pygame.K_w:
                game.player.jump = True
                jump_sound.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                game.moving_left = False
            if event.key == pygame.K_d:
                game.moving_right = False
            if event.key == pygame.K_q:
                game.throw_rock = False
                game.rock_thrown = False

    pygame.display.update()

pygame.quit()

