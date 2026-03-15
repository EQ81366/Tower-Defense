import os

import pygame, sys
from enum import Enum
from pathlib import Path
from typing import Mapping


def get_resource_path(relative_path: Path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    return Path(*(Path(__file__).resolve().parent).parts[:-1]) / relative_path


# finds the image paths
def image_paths(type: str, sub_type: Enum | None):
    if sub_type is not None:
        image_folder = Path(f"assets/{type}_images/{sub_type.name.lower()}")
    else:
        image_folder = Path(f"assets/{type}_images")

    image_folder = get_resource_path(image_folder)

    images = os.listdir(image_folder)

    return image_folder, images


# enum of all enemies
class EnemyType(Enum):
    BASIC = 0


# enum of all towers
class TowerType(Enum):
    BASIC = 0
    DOUBLE = 1


# enum of all shop items
class ShopType(Enum):
    SHOPUI = 0
    TOWERUI = 1


# enum of all upgrades
class UpgradeType(Enum):
    UPGRADEUI = 0
    UPGRADES = 1


# loads all game images
def load_images(retrieve: list[str]):
    image_list: list[Mapping[Enum, list[pygame.Surface]]] = []

    if "enemy" in retrieve:
        paths = image_paths("enemy", None)
        enemy_image_paths = sorted(
            paths[1]
        )  # list of all enemy image paths
        enemy_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all enemy images

        # loads all the enemy images
        for enum in EnemyType:
            enemy_list[enum] = [pygame.image.load(paths[0] / enemy_image_paths[enum.value])]

        image_list.append(enemy_list)

    if "tower" in retrieve:
        tower_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all tower images

        # loads all the tower images
        for enum in TowerType:
            paths = image_paths("tower", enum)
            tower_image_paths = sorted(
                paths[1]
            )  # list of all tower image paths
            temp_tower_list: list[pygame.Surface] = []

            # loads all images for a certain tower
            temp_tower_list = [
                pygame.image.load(paths[0] / tower_image_paths[i])
                for i in range(len(tower_image_paths))
            ]

            tower_list[enum] = temp_tower_list  # adds all the 3 tower images in one dict

        image_list.append(tower_list)

    if "shop" in retrieve:
        paths = image_paths("shop", None)
        shop_image_paths = sorted(
            paths[1]
        )  # list of all shop image paths
        shop_list: dict[Enum, list[pygame.Surface]] = {}  # dict of all shop images

        # loads all the shop images
        for enum in ShopType:
            shop_list[enum] = [pygame.image.load(paths[0] / shop_image_paths[enum.value])]

        image_list.append(shop_list)

    if "upgrade" in retrieve:
        paths = image_paths("upgrade", None)
        upgrade_image_paths = sorted(paths[1])  # list of all upgrade image paths
        upgrade_list: dict[
            Enum, list[pygame.Surface]
        ] = {}  # dict of all upgrade images

        # loads all the upgrade images
        for enum in UpgradeType:
            upgrade_list[enum] = [pygame.image.load(paths[0] / upgrade_image_paths[enum.value])]

        image_list.append(upgrade_list)

    return image_list
