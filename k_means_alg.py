import numpy as np


class PointsMap:
    def __init__(self, lenght=100, width=100, size=20, map_point=None):
        self.lenght = lenght
        self.width = width
        self.size = size
        self.map_point = map_point

    def create_map(self):
        return np.array([np.random.randint(self.lenght, size=2) for _ in range(self.size)])

    def bind_created_map(self):
        self.map_point = self.create_map()

    def choose_centroids(self, k_value=3):
        if self.map_point is not None:
            random_index = np.random.choice(self.size, size=k_value, replace=False)
            return self.map_point[random_index,:]


class KZones:
    def __init__(self, lenght=100, size=20, k_value=3):
        self.lenght = lenght
        self.size = size
        self.k_value = k_value
        self.points_set, self.centroids = self.initialize_points_set()

    def initialize_points_set(self):
        points_map_instance = PointsMap(lenght=self.lenght, size=self.size)
        points_map_instance.bind_created_map()
        return points_map_instance.map_point, points_map_instance.choose_centroids(self.k_value)
