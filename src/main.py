import numpy

if __name__ == "__main__":
    import pygame, os, psutil

    os.environ["SDL_VIDEODRIVER"] = "x11"
    os.environ["DISPLAY"] = ":1"

    # initiates pygame
    pygame.display.init()
    pygame.font.init()

    from enum import Enum
    from typing import Any
    from enemy import Enemies, enemies
    from tower import Towers, towers
    from shop import Shop, shop
    from upgrade import Upgrades, upgrades
    from money import money_script
    from tower_projectiles import tower_projectiles
    from mouse import mouse_info, clicked_and_released
    from fonts import font_30, font_50
    from map_sys import select_map, map
    from constants import stat_constants, TowerConstants, ShopType, UpgradeType, EnemyConstants, TowerStats, BulletStats

    # TODO LIST
    # bruh. clean up code bc I'm lazy and don't want to make art
    # 1. add more towers/enemies
    # 2. make bosses
    #
    # I'll add more as I go on

    initialized = False

    # sets screen width and height
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)  # in pixels

    clock = pygame.time.Clock()
    running = True

    class GameScreen(Enum):
        MAIN_MENU = 0
        IN_GAME = 1
        SETTINGS = 2

    game_screen = GameScreen.MAIN_MENU

    health_points = stat_constants()[1]

    # loads map info
    current_map = select_map()
    path, movement_nodes, map_offsets = map(current_map)

    for i in range(0):
        towers.add(Towers(TowerConstants.BASIC, 640, 360))

    shop.add(Shop(ShopType.SHOPUI, 640, 900))

    # for i, tower in enumerate(TowerConstants):
    #     shop.add(Shop(tower, 100 + 150 * i, 540))
    shop.add(Shop(TowerConstants.BASIC, 100, 540))

    shop.add(Shop(ShopType.TOWERUI, 0, 0))  # KEEP THIS AT END OF SHOP ITEMS

    upgrades.add(Upgrades(UpgradeType.UPGRADEUI, 1180, 360))
    upgrades.add(Upgrades(UpgradeType.UPGRADES, 1160, 360))

    x = 0

    death_info = None

    upgrade_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    clicked = False

    enemy_cap = 10000
    enemy_x = numpy.zeros(enemy_cap, dtype=numpy.float16)
    enemy_y = numpy.zeros(enemy_cap, dtype=numpy.float16)
    enemy_movement_vector = numpy.zeros([enemy_cap, 2], dtype=numpy.float16)
    enemy_alive = numpy.zeros(enemy_cap, dtype=numpy.bool)

    play = font_50.render("Play", True, "black").convert_alpha()
    play_location = [
        int(screen.get_width() / 2 - play.get_width() / 2),
        int(screen.get_height() / 2 - play.get_height()),
    ]
    play_rect = pygame.Rect(
        play_location[0] - 100,
        play_location[1] - 10,
        play.get_width() + 200,
        play.get_height() + 20,
    )
    border = play_rect.inflate(20, 20)
    settings_rect = pygame.Rect(10, 10, 50, 50)

    initialized = True

    def stats(money: int, health_points: int):
        text = font_30.render(f"Money: ${money}", True, "black")
        screen.blit(text, (5, 0))
        text = font_30.render(f"Health: {health_points}", True, "black")
        screen.blit(text, (5, 35))

    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"Current memory usage: {mem_info.rss / (1024 * 1024):.2f} MB")

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
            pygame.draw.rect(screen, "gray", play_rect, border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), border, 10, 25)
            pygame.draw.rect(screen, (180, 180, 180), settings_rect)
            screen.blit(play, play_location)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)

            if play_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.IN_GAME
            elif settings_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.SETTINGS

        elif game_screen is GameScreen.SETTINGS:
            pygame.draw.rect(screen, (180, 180, 180), settings_rect)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)
            if settings_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.MAIN_MENU
            # TODO: add settings

        elif game_screen is GameScreen.IN_GAME:
            screen.fill((50, 200, 20))  # background
            screen.blit(path, (-4, 200))  # map

            # -------------------------------------------------------------- #
            # cycles through all the necessary commands for the enemies group
            # -------------------------------------------------------------- #
            if len(enemies) > enemy_cap:
                enemy_group = enemies.sprites()
                for i in range(len(enemies) - enemy_cap):
                    enemy_group[i].kill()

            enemies.update()
            for i, sprite in enumerate(enemies):
                info = sprite.pathfind(screen)
                if isinstance(info, int):
                    health_points -= info
                else:
                    enemy_movement_vector[i], enemy_x[i], enemy_y[i] = info
                enemy_alive[i] = sprite.alive()
                sprite.id = i

            # --------------------------------------------------------------------- #

            enemy_xy = numpy.column_stack((enemy_x[: len(enemies)], enemy_y[: len(enemies)]))
            tower_list = towers.sprites()

            # ------------------------------------------------------------------- #
            # cycles through all the necessary commands for the tower projectiles
            # ------------------------------------------------------------------- #
            for sprite in tower_projectiles:
                death_info = sprite.move(enemy_xy[: len(enemies)], enemy_movement_vector[: len(enemies)], enemy_alive[: len(enemies)], screen)
                if death_info is not None:
                    for key in death_info[1]:
                        tower_list[death_info[0]].enemies_killed[key] += death_info[1][key]

            # ---------------------------------------------------------------------------------------- #

            # ------------------------------------------------------------- #
            # cycles through all the necessary commands for the towers group
            # ------------------------------------------------------------- #
            open = False, 0, False
            for i, sprite in enumerate(towers):
                sprite.wait += 1
                sprite.rotate(screen)
                sprite.find_closest_enemy(enemy_xy)
                if not open[0]:
                    open = sprite.open_upgrades(upgrade_rect), i, sprite.right_side
                sprite.show_range(screen)

            # ---------------------------------------------------------------- #
            # cycles through all the necessary commands for the upgrades group
            # ---------------------------------------------------------------- #
            upgrade_list = upgrades.sprites()

            upgrade_list[0].hovering(open[0], open[2], screen)
            upgrade_rect = upgrade_list[0].rect

            if open[0]:
                open_index = open[1]
                tower_selected = tower_list[open_index]
                upgrade_info = upgrade_list[1].upgrades(tower_selected.id, screen)
                if upgrade_info is not None:  # makes sure the returned info is not None
                    upgrades_bought = tower_selected.upgrades_bought[tower_selected.stats[TowerStats.TIER]]
                    upgrade_values: list[tuple[TowerStats | BulletStats, float, Any]] | None = None

                    fully_upgraded = upgrades_bought[0] and upgrades_bought[1]  # variable for checking if tower's current tier is fully upgraded
                    if not fully_upgraded and type(upgrade_info[0]) is tuple:  # if not fully upgraded runs upgrades for basic upgrades
                        upgrade_cost: int = upgrade_info[0][0]
                        money_script(False, upgrade_cost)
                        upgrade_values = upgrade_info[0][1]

                        tower_selected.upgrades_bought[tower_selected.stats[TowerStats.TIER]][upgrade_info[1]] = True  # updates upgrades_bought

                    elif type(upgrade_info[0]) is list:  # if it's fully upgraded, it'll return the type for tier-up choices
                        upgrade_values = upgrade_info[0]
                        tower_selected.stats[TowerStats.TIER] += 1
                        tower_selected.upgrade_path += [upgrade_info[1]]

                    if upgrade_values:
                        for upgrade in upgrade_values:
                            upgrading = upgrade[0]  # the stat being upgraded
                            upgrade_function = upgrade[2]  # the function used for upgrading the stat
                            stat_value_mod = upgrade[1]  # the stat modifier value

                            if type(upgrading) is TowerStats:
                                tower_selected.stats[upgrading] = upgrade_function(tower_selected.stats[upgrading], stat_value_mod)

                            elif type(upgrading) is BulletStats:
                                tower_selected.bullet_stats[upgrading] = upgrade_function(tower_selected.bullet_stats[upgrading], stat_value_mod)
            # ------------------------------------------------------------------------------------ #

            # ------------------------------------------------------------ #
            # cycles through all the necessary commands for the shop group
            # ------------------------------------------------------------ #
            Shop.tower_stats = []
            for sprite in shop:
                sprite.hovering(screen)
                sprite.showing(screen)
                sprite.place_tower(screen)
                sprite.show_stats(screen)
            # ------------------------------------------------------------------------------- #

            money = money_script()  # finds the current amount of money
            stats(money, health_points)

            x += 1
            if x > 10:
                for i in range(1):
                    enemies.add(Enemies(EnemyConstants.BASIC, 8, 280))
                x = -10

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
