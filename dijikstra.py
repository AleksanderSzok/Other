from collections import namedtuple
from dataclasses import dataclass
from math import sqrt, inf
import heapq
from typing import Optional, TypeVar, Dict, Set, List, Tuple

T = TypeVar("T")
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

graph_example = {
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


def remove_from_queue(queue: List[Point], distances: Dict[Point, float]) -> Point:
    queue.sort(key=lambda item: distances[item], reverse=True)
    nearest = queue.pop()
    return nearest


def dijkstra(
    graph: Dict[Point, Set[Point]], start: Point, destiny: Point
) -> Tuple[float, Dict[Point, Point]]:
    distances = {}
    for key, _ in graph.items():
        distances[key] = inf
    distances[start] = 0
    Q = list(graph.keys())
    previous = {}
    while Q:
        v = remove_from_queue(Q, distances)
        for neighbour in graph[v]:
            new_dist = distances[v] + dist(v, neighbour)
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                previous[v] = neighbour
            if neighbour == destiny:
                return distances[destiny], previous


@dataclass(order=True)
class PrioritizedPoint:
    distance: float = inf
    point: Optional[Point] = None

    def dist(self: T, other: T) -> float:
        delta_x = abs(self.point.x - other.point.x)
        delta_y = abs(self.point.y - other.point.y)
        return sqrt(delta_y**2 + delta_x**2)


def graph_to_prioritized(
    graph: Dict[Point, Set[Point]]
) -> Dict[Point, List[PrioritizedPoint]]:
    pts = {}
    for point in graph.keys():
        pts[point] = PrioritizedPoint(point=point)
    prioritized_graph = {}
    for key, items in graph.items():
        neighbours = []
        for item in items:
            neighbours.append(pts[item])
        prioritized_graph[key] = neighbours

    return prioritized_graph


def dijkstra_heap(
    graph: Dict[Point, List[PrioritizedPoint]], start: Point, destiny: Point
) -> Tuple[float, Dict[Point, Point]]:
    Q = []
    heapq.heapify(Q)
    points = list(graph.keys())
    points.remove(start)
    for point in points:
        heapq.heappush(Q, PrioritizedPoint(point=point))
    previous = {}
    v = PrioritizedPoint(point=start, distance=0)
    while Q:
        # if there's no access to destiny point, loop will not end
        for neighbour in graph[v.point]:
            new_dist = v.distance + v.dist(neighbour)
            if new_dist < neighbour.distance:
                neighbour.distance = new_dist
                updated_neighbour = PrioritizedPoint(
                    distance=new_dist, point=neighbour.point
                )
                previous[v.point] = neighbour.point
                heapq.heappush(Q, updated_neighbour)
            if neighbour.point == destiny:
                return neighbour.distance, previous
        v = heapq.heappop(Q)


# print(graph_to_prioritized(graph))

print(dijkstra(graph_example, start=a, destiny=e))
print(dijkstra_heap(graph_to_prioritized(graph_example), start=a, destiny=e))
