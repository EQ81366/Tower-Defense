from pathlib import Path

def enemy_image_path(enemy_type_number : int):
    # path to the enemies image
    image_folder = Path("assets/enemy_images")
    image_path = str(list(image_folder.glob("*enemy.png"))[enemy_type_number])

    return image_path

def tower_image_path_list(tower_type_number : int):
    # path to the tower images
    image_folder = Path("assets/tower_images")
    turret_image_path = str(list(image_folder.glob("*turret.png"))[tower_type_number])
    f_turret_image_path = str(list(image_folder.glob("*f_turret.png"))[tower_type_number])
    base_image_path = str(list(image_folder.glob("*base.png"))[tower_type_number])

    return [
        turret_image_path,
        f_turret_image_path,
        base_image_path
    ]

def shop_image_path(shop_type_number : int):
    # path to the shops image
    image_folder = Path("assets/shop_images")
    image_path = str(list(image_folder.glob("*ui.png"))[shop_type_number])

    return image_path

def upgrade_image_path(upgrade_type_number : int):
    image_folder = Path("assets/upgrade_images")
    image_path = str(list(image_folder.glob("*ui.png"))[upgrade_type_number])

    return image_path
