if __name__ == "__main__":
    import pygame, os, numpy

    os.environ["DISPLAY"] = ":1"

    # initiates pygame
    pygame.display.init()
    pygame.font.init()

    from functions import stats, __init__, get_mem_use, BRect

    __init__()  # runs all the necessary starting functions

    from constants import stat_constants, EnemyConstants, GameScreen, BulletStats, TowerConstants
    from enemy import Enemies, enemies, spawn_enemy, enemy_xy, enemy_alive, enemy_movement_vector
    from tower import Towers, towers
    from shop import Shop, shop
    from upgrade import upgrade_manager, upgrade_background
    from money import money_man
    from tower_projectiles import tower_projectiles
    from mouse import mouse_info, clicked_and_released
    from map.map_sys import map_system
    from fonts import font_50

    bullet_stats = {stat: TowerConstants.BASIC.bullet_info[i] for i, stat in enumerate(BulletStats)}

    # TODO LIST
    # bruh. clean up code bc I'm lazy and don't want to make art
    # 1. add more towers/enemies
    # 2. make bosses
    #
    # I'll add more as I go on

    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)

    clock = pygame.time.Clock()
    running = True

    game_screen = GameScreen.MAIN_MENU

    health_points = stat_constants()[1]

    # loads map info
    current_map = map_system.get_map()
    map_image = map_system.get_image()
    map_offsets = map_system.get_offsets()

    x = 0

    clicked = False

    play = font_50.render("Play", True, "black").convert_alpha()
    play_location = (int(screen.get_width() / 2), int(screen.get_height() / 2 - 56))
    play_rect = pygame.Rect(play_location, (play.get_width() + 200, play.get_height() + 20))
    border = play_rect.inflate(20, 20)
    settings_rect = BRect((35, 35, 50, 50), (180, 180, 180))
    play_rect = BRect(play_rect, "gray", (True, (100, 100, 100), border), 10, 25)

    get_mem_use()

    frame_check = 0

    # and so begins the main script
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_screen is not GameScreen.IN_GAME:
            screen.fill((255, 255, 255))
            if frame_check < 100:
                frame_check += 1

        if game_screen is GameScreen.MAIN_MENU:
            play_rect.draw(screen)
            settings_rect.draw(screen)
            screen.blit(
                play,
                (
                    play_location[0] - play.get_width() / 2,
                    play_location[1] - play.get_height() / 2,
                ),
            )
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)

            if play_rect.rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.IN_GAME
                get_mem_use()

            elif settings_rect.rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.SETTINGS

        elif game_screen is GameScreen.SETTINGS:
            settings_rect.draw(screen)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)
            if settings_rect.rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.MAIN_MENU
            # TODO: add settings

        elif game_screen is GameScreen.IN_GAME:
            screen.fill((50, 200, 20))  # background
            screen.blit(map_image, map_offsets)  # map

            # -------------------------------------------------------------- #
            # cycles through all the necessary commands for the enemies group
            # -------------------------------------------------------------- #
            Enemies.c_frame_dmg = 0
            Enemies.update_xy()
            enemies.update(screen)
            health_points -= Enemies.c_frame_dmg
            enemy_amount = len(enemies)
            # --------------------------------------------------------------------- #

            local_enemy_xy = enemy_xy[enemy_alive]

            # ------------------------------------------------------------------- #
            # cycles through all the necessary commands for the tower projectiles
            # ------------------------------------------------------------------- #
            tower_projectiles.update(
                local_enemy_xy,
                enemy_movement_vector[enemy_alive],
                screen,
            )
            # ------------------------------------------------------------ #

            # ------------------------------------------------------------- #
            # cycles through all the necessary commands for the towers group
            # ------------------------------------------------------------- #
            towers.update(screen, enemy_xy, upgrade_background.rect)
            # -----------------------------------------------------------------------#

            # ---------------------------------------------------------------- #
            # runs the methods for upgrades
            # ---------------------------------------------------------------- #
            if len(towers) > 0:  # if towers exist
                tower_selected = Towers.get_tower()
                upgrade_background.hovering(tower_selected.upgrades_open, tower_selected.right_side, screen)

                upgrade_index = upgrade_manager.upgrades(tower_selected, screen)
                if upgrade_index is not None:  # if upgrade or tierup clicked
                    upgrade_manager.buy_upgrade(tower_selected, upgrade_index)  # subtracts cost and applied upgrade effect to tower
            # ------------------------------------------------------------------------------------ #

            # ------------------------------------------------------------ #
            # cycles through all the necessary commands for the shop group
            # ------------------------------------------------------------ #
            Shop.reset()
            shop.update(screen)
            # -------------------------------------------------------- #

            money = money_man.get_money()  # finds the current amount of money
            stats(money, int(health_points), screen)  # displays statss

            x += 1
            if x > 10:
                for i in range(10000):
                    # enemies.add(Enemies(EnemyConstants.BASIC))
                    spawn_enemy(EnemyConstants.BASIC)
                x = -10000000

            # for point in map_system.all_nodes:
            #     pygame.draw.rect(screen, "red", (point[0], (10, 10)))

        pygame.display.flip()
        clock.tick(60)
        fps = clock.get_fps()
        # print(fps, len(enemies), len(towers))
        # print(fps)
        # print(Enemies.damage_dealt)
        if fps < 5 and frame_check == 100:
            print("GAME CRASHED")
            running = False
            pygame.quit()

    pygame.quit()
