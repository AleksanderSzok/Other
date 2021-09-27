import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.datasets import make_blobs


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


class KClusters:
    def __init__(self, lenght: int = 100, size: int = 20, k_value: int = 3):
        self.lenght = lenght
        self.size = size
        self.k_value = k_value
        self.points_set, self.centroids = self.initialize_points_set()

    def initialize_points_set(self):
        points_map_instance = PointsMap(lenght=self.lenght, size=self.size)
        points_map_instance.bind_created_map()
        return points_map_instance.map_point, points_map_instance.choose_centroids(self.k_value)

    def assign_point_to_cluster(self):
        assignment_list = []
        for elem in self.points_set:
            tmp_list = []
            for centroid in self.centroids:
                tmp_list.append(np.linalg.norm([elem - centroid]))
            assignment_list.append(np.argmin(tmp_list))
        return assignment_list

    def new_centroids(self):
        assignment_list = np.array(self.assign_point_to_cluster()) # todo change to array in assign_point_to_zone method
        new_centroid_list = np.empty((1,2), dtype=int)
        for i in range(self.k_value):
            tmp = self.points_set[assignment_list == i].mean(axis=0)
            new_centroid_list = np.append(new_centroid_list, [tmp], axis=0)
        return np.around(new_centroid_list[1:], decimals=2)

    def choose_final_centroids(self):
        tmp_centroids = self.new_centroids()
        while not np.array_equal(self.centroids, tmp_centroids):
            self.centroids = tmp_centroids
            tmp_centroids = self.new_centroids()

    @staticmethod
    def points_set_flatten_to_plot(points):
        flatten_array = points.flatten('F').copy()
        return flatten_array[:int(len(flatten_array)/2)], flatten_array[int(len(flatten_array)/2):]

    def plot_points_set(self):
        assignment_array = np.array(self.assign_point_to_cluster())
        colors = cm.rainbow(np.linspace(0, 1, self.k_value))
        for i in range(self.k_value):
            tmp = self.points_set[assignment_array == i]
            x, y = self.points_set_flatten_to_plot(tmp)
            plt.scatter(x, y, color=colors[i])
        plt.show()
        plt.savefig("k_means_{}.png".format(self.k_value))


# create sample:
X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=0)
points_m = PointsMap(size=len(X), map_point=X)
points_m.choose_centroids(k_value=4)
k_cluster = KClusters(lenght=200, size=300, k_value=4)
k_cluster.points_set = points_m.map_point
k_cluster.centroids = points_m.choose_centroids(k_value=4)
k_cluster.choose_final_centroids()
k_cluster.plot_points_set()
