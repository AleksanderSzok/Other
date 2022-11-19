from collections import namedtuple
from math import sqrt, inf

Point = namedtuple("Point", ["x", "y"])


def dist(point_one: Point, point_two: Point) -> float:
    delta_x = abs(point_one.x - point_two.x)
    delta_y = abs(point_one.y - point_two.y)
    return sqrt(delta_y**2 + delta_x**2)


a = Point(x=2, y=1)
b = Point(x=4, y=2)
c = Point(x=2, y=3)
d = Point(x=2, y=6)
e = Point(x=4, y=7)
f = Point(x=3, y=5)
g = Point(x=5, y=4)
h = Point(x=8, y=3)
i = Point(x=9, y=5)

graph = {
    a: {b},
    b: {a, c, g},
    c: {b, d, f},
    d: {c, e},
    e: {d, f},
    f: {c, e, g},
    g: {b, f, h},
    h: {g, i},
    i: {h},
}


def remove_from_queue(queue, distances):
    queue.sort(key=lambda item: distances[item], reverse=True)
    nearest = queue.pop()
    return nearest


def dijkstra(graph, start, destiny):
    distances = {}
    for key, _ in graph.items():
        distances[key] = inf
    distances[start] = 0
    Q = list(graph.keys())
    previous = {}
    stop = False
    while Q:
        if stop:
            break
        v = remove_from_queue(Q, distances)
        for neighbour in graph[v]:
            new_dist = distances[v] + dist(v, neighbour)
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                previous[v] = neighbour
            if neighbour == destiny:
                stop = True
                break

    return distances[destiny], previous


dijkstra(graph, a, e)
