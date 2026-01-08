import pygame
import json

def select_map():
    global current_map
    #return input("Map: ")
    current_map = "path1"
    return current_map

select_map()

def show_map():
    return current_map

# the map system
def map(map : str):
    # loads the map based off of selected map
    path = pygame.image.load(f"assets/map_images/{map}.png")
    with open(f"assets/map_data/{map}.json") as f:
        map_data = json.load(f)
    
    # all destinations for the enemy on a given map
    movement_nodes = map_data.get("movement_nodes", [])
    map_offsets = map_data.get("map_offsets", [])
    
    return path, movement_nodes, map_offsets