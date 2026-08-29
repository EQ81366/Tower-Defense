import pygame, json
from numpy import ndarray, zeros
from image_loader import image_cache
from pathlib import Path
from constants import MapInfo
from functions import lerp


class MapSystem:
    map_images = image_cache["map"]
    with open(Path("src/map/map_nodes.json"), "r") as file:
        nodes_file = json.load(file)

    def __init__(self):
        self.current_map: MapInfo
        self.map_image: pygame.Surface
        self.distance_b_points = 10

    def get_map(self):
        return self.current_map

    def set_map(self, map: MapInfo):
        self.current_map = map
        self.nodes: list[tuple[int, int]] = MapSystem.nodes_file.get(self.current_map.name)
        self.map_image = MapSystem.map_images[self.current_map][0]

        self.all_nodes: list[tuple[tuple[float, float], set[int]]] = []
        for idx, i in enumerate(self.nodes):
            self.all_nodes.append(((i[0], i[1]), set()))
            if idx + 1 < len(self.nodes):
                points = lerp(pygame.Vector2(self.nodes[idx]), pygame.Vector2(self.nodes[idx + 1]), self.distance_b_points)
                for point in points:
                    self.all_nodes.append(((point.x, point.y), set()))

    def get_offsets(self):
        return self.current_map.offset

    def get_image(self):
        return self.map_image

    def get_nodes(self):
        return self.nodes

    def get_all_nodes(self, filter: ndarray = zeros(0)) -> list[tuple[tuple[float, float], set[int]]]:
        if filter.__len__() == 0:
            return self.all_nodes
        else:
            return [self.all_nodes[int(i)] for i in filter]

    def get_d_b_points(self):
        return self.distance_b_points

    def set_enemy_pos(self, index: int, enemy_idx: int):
        if index + 1 < len(self.all_nodes):
            self.all_nodes[index][1].add(enemy_idx)

    def remove_enemy_pos(self, index: int, enemy_idx: int):
        if index + 1 < len(self.all_nodes):
            self.all_nodes[index][1].remove(enemy_idx)


def create_map():
    global map_system
    map_system = MapSystem()
