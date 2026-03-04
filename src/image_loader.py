import pygame, sys
from enum import Enum
from pathlib import Path
from typing import Mapping

def get_resource_path(relative_path : Path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS) # type: ignore
    except Exception:
        base_path = Path(".").absolute()

    return base_path / relative_path

# finds the image paths
def image_paths(type : str, sub_type : Enum|None):
    image_folder = (
        Path(f"assets/{type}_images/{sub_type.name.lower()}")
        if sub_type is not None
        else Path(f"assets/{type}_images")
    )

    image_folder = get_resource_path(image_folder)

    images = list(image_folder.glob("*.png"))
    return images

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
def load_images(retrieve : list[str]):
    image_list : list[Mapping[Enum, list[pygame.Surface]]] = []

    if "enemy" in retrieve:
        image_list.append(
            {
                enum: [pygame.image.load(sorted(image_paths("enemy", None))[enum.value])]
                for enum in EnemyType
            }
        )

    if "tower" in retrieve:
        image_list.append(
            {
                enum: [pygame.image.load(path) for path in sorted(image_paths("tower", enum))]
                for enum in TowerType
            }
        )
        
    if "shop" in retrieve:
        image_list.append(
            {
                enum: [pygame.image.load(sorted(image_paths("shop", None))[enum.value])]
                for enum in ShopType
            }
        )

    if "upgrade" in retrieve:
        image_list.append(
            {
                enum: [pygame.image.load(sorted(image_paths("upgrade", None))[enum.value])]
                for enum in UpgradeType
            }
        )

    return image_list