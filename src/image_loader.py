import pygame
from enum import Enum
from pathlib import Path

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

# enum of all shop items
class ShopType(Enum):
    SHOPUI = 0
    TOWERUI = 1

# enum of all upgrades
class UpgradeType(Enum):
    UPGRADEUI = 0
    BASICUPGRADES = 1

# loads all game images
def load_images():
    enemy_image_paths = sorted(image_paths("enemy")) # list of all enemy image paths
    enemy_list : dict[Enum, pygame.Surface] = {} # dict of all enemy images

    # loads all the enemy images
    for enum in EnemyType:
        enemy_list[enum] = pygame.image.load(enemy_image_paths[enum.value])

    tower_image_paths = sorted(image_paths("tower")) # list of all tower image paths
    tower_list : dict[Enum, list[pygame.Surface]] = {} # dict of all tower images

    loop = 1
    # loads all the tower images
    for enum in TowerType:
        temp_tower_list : list[pygame.Surface] = []
        loop -= 1
        # loads all 3 images for a certain tower
        for i in range(3): # type: ignore
            temp_tower_list += [pygame.image.load(tower_image_paths[enum.value+loop])]
            loop += 1
        
        tower_list[enum] = temp_tower_list # adds all the 3 tower images in one dict

    shop_image_paths = sorted(image_paths("shop")) # list of all shop image paths
    shop_list : dict[Enum, pygame.Surface] = {} # dict of all shop images

    # loads all the shop images
    for enum in ShopType:
        shop_list[enum] = pygame.image.load(shop_image_paths[enum.value])

    upgrade_image_paths = sorted(image_paths("upgrade")) # list of all upgrade image paths
    upgrade_list : dict[Enum, pygame.Surface] = {} # dict of all upgrade images

    # loads all the upgrade images
    for enum in UpgradeType:
        upgrade_list[enum] = pygame.image.load(upgrade_image_paths[enum.value])

    print(upgrade_list)

    return enemy_list, tower_list, shop_list, upgrade_list


#load_images()
