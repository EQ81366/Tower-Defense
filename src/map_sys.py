import pygame

from image_loader import ImageLoader

# the map system
def map(map : str):
    # loads the map based off of selected map
    path = ImageLoader.load_map(map)
    # defines movement_nodes so it doesn't break if given an invalid map name
    movement_nodes = []
    map_offsets = ()
    if map == "path1":
        # all destinations for the enemy on a given map
        movement_nodes = [[178, 260], [225, 560], [505, 560], [566, 254], [758, 259], [833, 586], [1130, 590], [1200, 260], [1279, 259]]
        map_offsets = (-4, 200)
    
    return path, movement_nodes, map_offsets