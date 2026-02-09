import pygame
from enum import Enum
from pathlib import Path
from typing import Mapping

# finds the image paths
def image_paths(type : str, sub_type : str|None):
    if sub_type != None:
        image_folder = Path(f"assets/{type}_images/{sub_type}")
    else:
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

# loads all game images
def load_images(retrieve : list[str]):
    image_list : list[Mapping[Enum, list[pygame.Surface]]] = []

    if retrieve.count("enemy") > 0:
        enemy_image_paths = sorted(image_paths("enemy", None)) # list of all enemy image paths
        enemy_list : dict[Enum, list[pygame.Surface]] = {} # dict of all enemy images

        # loads all the enemy images
        for enum in EnemyType:
            enemy_list[enum] = [pygame.image.load(enemy_image_paths[enum.value])]

        image_list.append(enemy_list)

    if retrieve.count("tower") > 0:
        tower_list : dict[Enum, list[pygame.Surface]] = {} # dict of all tower images

        # loads all the tower images
        for enum in TowerType:
            tower_image_paths = sorted(image_paths("tower", str(enum.name).lower())) # list of all tower image paths
            temp_tower_list : list[pygame.Surface] = []
            
            # loads all images for a certain tower
            temp_tower_list = [pygame.image.load(tower_image_paths[i]) for i in range(len(tower_image_paths))]
            
            tower_list[enum] = temp_tower_list # adds all the 3 tower images in one dict
        
        image_list.append(tower_list)
        
    if retrieve.count("shop") > 0:
        shop_image_paths = sorted(image_paths("shop", None)) # list of all shop image paths
        shop_list : dict[Enum, list[pygame.Surface]] = {} # dict of all shop images

        # loads all the shop images
        for enum in ShopType:
            shop_list[enum] = [pygame.image.load(shop_image_paths[enum.value])]

        image_list.append(shop_list)

    if retrieve.count("upgrade") > 0:
        upgrade_image_paths = sorted(image_paths("upgrade", None)) # list of all upgrade image paths
        upgrade_list : dict[Enum, list[pygame.Surface]] = {} # dict of all upgrade images

        # loads all the upgrade images
        for enum in UpgradeType:
            upgrade_list[enum] = [pygame.image.load(upgrade_image_paths[enum.value])]
        
        image_list.append(upgrade_list)

    return image_list