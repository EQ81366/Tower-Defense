import pygame
from enum import Enum
from pathlib import Path
from typing import Mapping

# finds the image paths
def image_paths(type : str):
    image_folder = Path(f"assets/{type}_images")
    images = list(image_folder.glob("*.png"))
    return images

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
    enemy_list : dict[Enum, pygame.Surface] = {} # dict of all enemy images

    # loads all the enemy images
    for enum in EnemyType:
        enemy_list[enum] = pygame.image.load(enemy_image_paths[enum.value])

    return enemy_list

# loads tower images
def load_tower_images():
    tower_image_paths = sorted(image_paths("tower")) # list of all tower image paths
    tower_list : dict[Enum, list[pygame.Surface]] = {} # dict of all tower images

    loop = 1
    # loads all the tower images
    for enum in TowerType:
        temp_tower_list : list[pygame.Surface] = []
        loop -= 1
        # loads all images for a certain tower
        for i in range(ImagesPerTower[enum.name].value): # type: ignore
            temp_tower_list += [pygame.image.load(tower_image_paths[enum.value+loop])]
            loop += 1
        
        tower_list[enum] = temp_tower_list # adds all the 3 tower images in one dict
    
    return tower_list

# loads shop images
def load_shop_images():
    shop_image_paths = sorted(image_paths("shop")) # list of all shop image paths
    shop_list : dict[Enum, pygame.Surface] = {} # dict of all shop images

    # loads all the shop images
    for enum in ShopType:
        shop_list[enum] = pygame.image.load(shop_image_paths[enum.value])

    return shop_list

# loads upgrade images
def load_upgrade_images():
    upgrade_image_paths = sorted(image_paths("upgrade")) # list of all upgrade image paths
    upgrade_list : dict[Enum, pygame.Surface] = {} # dict of all upgrade images

    # loads all the upgrade images
    for enum in UpgradeType:
        upgrade_list[enum] = pygame.image.load(upgrade_image_paths[enum.value])

    return upgrade_list

# loads all game images
def load_images():
    return load_enemy_images(), load_tower_images(), load_shop_images(), load_upgrade_images()