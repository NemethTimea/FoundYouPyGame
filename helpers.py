import World

from consts import *


def draw_text(screen, text, font, text_col, x, y):
    screen.blit(font.render(text, True, text_col), (x, y))

def draw_bg(background_scroll):
    SCREEN.fill(BG)
    width = SKY.get_width()
    for x in range(5):
        SCREEN.blit(SKY, ((x * width) - background_scroll * 0.5 , 0))
        SCREEN.blit(MOUNTAIN, ((x * width) - background_scroll * 0.6, (SCREEN_HEIGHT - MOUNTAIN.get_height()) - 200))
        SCREEN.blit(BACKGROUND1, ((x * width) - background_scroll * 0.7, (SCREEN_HEIGHT - MOUNTAIN.get_height()) - 70))
        SCREEN.blit(BACKGROUND2, ((x * width) - background_scroll * 0.8, (SCREEN_HEIGHT - MOUNTAIN.get_height()) - 50))

#func to reset level
def reset_level():
    player_group.empty()
    enemy_group.empty()
    bullet_group.empty()
    rock_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    World.World.obstacle_list = []

    #create empty tile list
    data = []
    for _ in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data
