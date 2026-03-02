import pygame
from enum import Enum
from pathlib import Path
from typing import Mapping
import sys
import os


# Resolve paths correctly when running under PyInstaller
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore
    return relative_path


# finds the image paths
def image_paths(type: str, sub_type: Enum | None):
    if sub_type is not None:
        folder = f"assets/{type}_images/{sub_type.name.lower()}"
    else:
        folder = f"assets/{type}_images"

    image_folder = Path(resource_path(folder))
    return list(image_folder.glob("*.png"))


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
        enemy_image_paths = sorted(image_paths("enemy", None))
        enemy_list: dict[Enum, list[pygame.Surface]] = {}

        for enum in EnemyType:
            path = resource_path(str(enemy_image_paths[enum.value]))
            enemy_list[enum] = [pygame.image.load(path)]

        image_list.append(enemy_list)

    if "tower" in retrieve:
        tower_list: dict[Enum, list[pygame.Surface]] = {}

        for enum in TowerType:
            tower_image_paths = sorted(image_paths("tower", enum))
            tower_list[enum] = [
                pygame.image.load(resource_path(str(p)))
                for p in tower_image_paths
            ]

        image_list.append(tower_list)

    if "shop" in retrieve:
        shop_image_paths = sorted(image_paths("shop", None))
        shop_list: dict[Enum, list[pygame.Surface]] = {}

        for enum in ShopType:
            path = resource_path(str(shop_image_paths[enum.value]))
            shop_list[enum] = [pygame.image.load(path)]

        image_list.append(shop_list)

    if "upgrade" in retrieve:
        upgrade_image_paths = sorted(image_paths("upgrade", None))
        upgrade_list: dict[Enum, list[pygame.Surface]] = {}

        for enum in UpgradeType:
            path = resource_path(str(upgrade_image_paths[enum.value]))
            upgrade_list[enum] = [pygame.image.load(path)]

        image_list.append(upgrade_list)

    return image_list
