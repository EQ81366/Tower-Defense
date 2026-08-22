import pygame, os, sys
from enum import Enum
from pathlib import Path
from constants import TowerConstants, EnemyConstants, ShopType, UpgradeType, MapInfo

pygame.display.init()
pygame.display.set_mode(flags=pygame.HIDDEN)


def get_resource_path(relative_path: Path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)  # type: ignore
    except Exception:
        base_path = Path(".").absolute()

    return base_path / relative_path


# finds the image paths
def image_paths(type: str, sub_type: Enum | None = None):
    if sub_type is not None:
        image_folder = Path(f"assets/{type}_images/{sub_type.name.lower()}")
    else:
        image_folder = Path(f"assets/{type}_images")

    image_folder = get_resource_path(image_folder)

    images = os.listdir(image_folder)

    return image_folder, images


image_cache: dict[str, dict[Enum, list[pygame.Surface]]] = {}


# loads all game images
def load_images():
    if not image_cache:
        paths = image_paths("enemy")
        enemy_image_paths = sorted(paths[1])  # list of all enemy image paths
        enemy_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all enemy images

        # loads all the enemy images
        for enum in EnemyConstants:
            enemy_list[enum] = [pygame.image.load(paths[0] / enemy_image_paths[enum.number]).convert_alpha()]

        image_cache["enemy"] = enemy_list

        # ---------------------------------------------------------------------------------------------------------- #

        tower_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all tower images

        # loads all the tower images
        for enum in TowerConstants:
            paths = image_paths("tower", enum)
            tower_image_paths = sorted(paths[1])  # list of all tower image paths
            temp_tower_list: list[pygame.Surface] = []

            # loads all images for a certain tower
            temp_tower_list = [pygame.image.load(paths[0] / tower_image_paths[i]).convert_alpha() for i in range(len(tower_image_paths))]

            tower_list[enum] = temp_tower_list  # adds all the 3 tower images in one dict

        image_cache["tower"] = tower_list

        # ---------------------------------------------------------------------------------------------------------- #

        paths = image_paths("shop")
        shop_image_paths = sorted(paths[1])  # list of all shop image paths
        shop_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all shop images

        # loads all the shop images
        for enum in ShopType:
            shop_list[enum] = [pygame.image.load(paths[0] / shop_image_paths[enum.value]).convert_alpha()]

        image_cache["shop"] = shop_list

        # ---------------------------------------------------------------------------------------------------------- #

        paths = image_paths("upgrade")
        upgrade_image_paths = sorted(paths[1])  # list of all upgrade image paths
        upgrade_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all upgrade images

        # loads all the upgrade images
        for enum in UpgradeType:
            upgrade_list[enum] = [pygame.image.load(paths[0] / upgrade_image_paths[enum.value]).convert_alpha()]

        image_cache["upgrade"] = upgrade_list

        # ---------------------------------------------------------------------------------------------------------- #

        paths = image_paths("map")
        map_image_paths = sorted(paths[1])
        map_list: dict[Enum, list[pygame.Surface]] = {}

        # loads all the map images
        for i, enum in enumerate(MapInfo):
            map_list[enum] = [pygame.image.load(paths[0] / map_image_paths[i]).convert_alpha()]

        image_cache["map"] = map_list


# ---------------------------------------------------------------------------------------------------------- #
