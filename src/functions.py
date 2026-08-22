import pygame, os, psutil
from math import floor
from fonts import font_30
from image_loader import load_images


def stats(money: int, health_points: int, screen: pygame.Surface):
    text = font_30.render(f"Money: ${money}", True, "black")
    screen.blit(text, (5, 0))
    text = font_30.render(f"Health: {health_points}", True, "black")
    screen.blit(text, (5, 35))


def lerp(point1: pygame.Vector2, point2: pygame.Vector2, distance_b_points: float):
    distance = point1.distance_to(point2)

    total_points = floor((distance / distance_b_points))

    percentage = distance_b_points / distance

    percentage_complete = percentage

    points: list[pygame.Vector2] = []
    for i in range(total_points - 1):
        points.append(point1.lerp(point2, percentage_complete))
        percentage_complete += percentage

    return points


def get_mem_use():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"Current memory usage: {mem_info.rss / (1024 * 1024):.2f} MB")


def __init__():
    load_images()

    from map.map_sys import create_map

    create_map()
    from map.map_sys import map_system
    from constants import TowerConstants, MapInfo

    map_system.set_map(MapInfo.path1)

    from shop import shop, ShopType, Shop
    from tower import towers, Towers

    for i in range(1):
        towers.add(Towers(TowerConstants.BASIC, 640, 360))

    shop.add(Shop(ShopType.SHOPUI, 640, 900))

    for i, tower in enumerate(TowerConstants):
        shop.add(Shop(tower, 100 + 150 * i, 540))
    # shop.add(Shop(TowerConstants.BASIC, 100, 540))

    shop.add(Shop(ShopType.TOWERUI, 0, 0))  # KEEP THIS AT END OF SHOP ITEMS


class BRect:
    def __init__(
        self,
        rect: tuple[int, int, int, int] | pygame.Rect,
        color: str | tuple[int, int, int],
        border: tuple[bool, str | tuple[int, int, int], None | pygame.Rect] = (
            False,
            "black",
            None,
        ),
        border_width: int = 0,
        border_radius: int = 0,
    ):
        self.rect = pygame.Rect(rect)
        self.rect.center = rect[0], rect[1]
        self.color = color
        self.border = border
        if self.border[2] is not None:
            self.border[2].center = rect[0], rect[1]

        self.border_width = border_width
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.border[0]:
            pygame.draw.rect(
                screen,
                self.border[1],
                self.rect if self.border[2] is None else self.border[2],
                width=self.border_width,
                border_radius=self.border_radius,
            )
