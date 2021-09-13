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

    def choose_centroids(self):
        if self.map_point is not None:
            random_index = np.random.choice(self.size, size=3, replace=False)
            return self.map_point[random_index,:]
