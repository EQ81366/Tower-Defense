from enum import Enum
import pygame

class Images(Enum):
    BULLET = "assets/bullet/b_bullet.png"
    ENEMY1 = "assets/enemies/enemy1.png"
    SHOP_UI = "assets/shop/shopui.png"
    BASIC_TOWER = "assets/towers/basic_tower/basic_tower.png" #TODO edit this image (this is the image used in the shop)

class TowerImages(Enum):
    BASIC = [
        "assets/towers/basic_tower/basic_base.png",
        "assets/towers/basic_tower/basic_turret.png",
        "assets/towers/basic_tower/firing_basic_turret.png"
    ]
    
    @staticmethod
    def get_tower_from_name(name : str):
        for tower in TowerImages:
            if tower.name == name.upper():
                return tower
        print("Did not find a valid tower for name: " + name)
        return None

class Maps(Enum):
    MAP1 = "assets/maps/map1.png"

    @staticmethod
    def get_map_from_name(name : str):
        for map in Maps:
            if map.name == name.upper():
                return map
        return None

class ImageLoader:
    @staticmethod
    def load(image : Images):
        return pygame.image.load(image.value)
    
    @staticmethod
    def load_tower(name : str):
        tower = TowerImages.get_tower_from_name(name)
        return pygame.image.load(tower.value[0]), pygame.image.load(tower.value[1]), pygame.image.load(tower.value[2])
    
    @staticmethod
    def load_map(name : str):
        return pygame.image.load(Maps.get_map_from_name(name).value)