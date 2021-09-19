import numpy as np


class PointsMap:
    def __init__(self, lenght: int = 100, width: int = 100, size: int = 20, map_point=None):
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

# PointsMap(map_point= ...)
# PointsMap.choose_centroids()
class KZones:
    def __init__(self, lenght: int = 100, size: int = 20, k_value: int = 3):
        self.lenght = lenght
        self.size = size
        self.k_value = k_value
        self.points_set, self.centroids = self.initialize_points_set()

    def initialize_points_set(self):
        points_map_instance = PointsMap(lenght=self.lenght, size=self.size)
        points_map_instance.bind_created_map()
        return points_map_instance.map_point, points_map_instance.choose_centroids(self.k_value)

    def assign_point_to_zone(self):
        assignment_list = []
        for elem in self.points_set:
            tmp_list = []
            for centroid in self.centroids:
                tmp_list.append(np.linalg.norm([elem - centroid]))
            assignment_list.append(np.argmin(tmp_list))
        return assignment_list

    def new_centroids(self):
        assignment_list = np.array(self.assign_point_to_zone()) # todo change to array in assign_point_to_zone method
        new_centroid_list = np.empty((1,2), dtype=int)
        for i in range(self.k_value):
            tmp = self.points_set[assignment_list == i].mean(axis=0)
            new_centroid_list = np.append(new_centroid_list, [tmp], axis=0)
        return new_centroid_list[1:]
