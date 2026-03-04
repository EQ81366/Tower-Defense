from pathlib import Path

ENEMY_IMAGE_PATH : Path = Path("assets/enemy_images")
TOWER_IMAGE_PATH : Path = Path("assets/tower_images")
SHOP_IMAGE_PATH = Path("assets/shop_images")
UPGRADE_IMAGE_PATH = Path("assets/upgrade_images")

def enemy_image_path(enemy_type_number : int):
    # path to the enemies image
    image_path = str(list(ENEMY_IMAGE_PATH.glob("*enemy.png"))[enemy_type_number])

    return image_path

def tower_image_path_list(tower_type_number : int):
    # path to the tower images
    turret_image_path = str(list(TOWER_IMAGE_PATH.glob("*turret.png"))[tower_type_number])
    f_turret_image_path = str(list(TOWER_IMAGE_PATH.glob("*f_turret.png"))[tower_type_number])
    base_image_path = str(list(TOWER_IMAGE_PATH.glob("*base.png"))[tower_type_number])

    return [
        turret_image_path,
        f_turret_image_path,
        base_image_path
    ]

def shop_image_path(shop_type_number : int):
    # path to the shops image
    image_path = str(list(SHOP_IMAGE_PATH.glob("*ui.png"))[shop_type_number])

    return image_path

def upgrade_image_path(upgrade_type_number : int):
    image_path = str(list(UPGRADE_IMAGE_PATH.glob("*ui.png"))[upgrade_type_number])

    return image_path
