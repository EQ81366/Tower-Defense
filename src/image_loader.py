import pygame
from enum import Enum
from pathlib import Path
import os

# finds the image paths
def image_paths(type : str):
    return list(Path(f"assets/{type}_images").glob("*.png"))

# enum of all enemies
class EnemyType(Enum):
    BASIC = 0

# enum of all towers
class TowerType(Enum):
    BASIC = 0
    DOUBLE = 1

# how many images to load for each tower
class ImagesPerTower(Enum):
    BASIC = 3
    DOUBLE = 4

# enum of all shop items
class ShopType(Enum):
    SHOPUI = 0
    TOWERUI = 1

# enum of all upgrades
class UpgradeType(Enum):
    UPGRADEUI = 0
    BASICUPGRADES = 1

# loads enemy images
def load_enemy_images():
    enemy_image_paths = sorted(image_paths("enemy")) # list of all enemy image paths
    return {enum: pygame.image.load(enemy_image_paths[enum.value]) for enum in EnemyType} # dict of all enemy images

# loads tower images
def load_tower_images():
    return {types: [pygame.image.load(paths) for paths in list(Path(f"assets/tower_images/{types.name.lower()}/").glob("*.png"))] for types in TowerType}

# loads shop images
def load_shop_images():
    shop_image_paths = sorted(image_paths("shop")) # list of all shop image paths
    return {enum: pygame.image.load(shop_image_paths[enum.value]) for enum in ShopType} # dict of all shop images

# loads upgrade images
def load_upgrade_images():
    upgrade_image_paths = sorted(image_paths("upgrade")) # list of all upgrade image paths
    return {enum: pygame.image.load(upgrade_image_paths[enum.value]) for enum in UpgradeType} # dict of all upgrade images

# loads all game images
def load_images():
    return load_enemy_images(), load_tower_images(), load_shop_images(), load_upgrade_images()