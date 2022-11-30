# problem 39
import copy
from typing import List


output_list = []


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    l = []
    combination_sum(candidates, target, l, target)
    return output_list


def combination_sum(
    candidates: List[int], temp_target: int, l: List[int], target: int
) -> None:
    if temp_target < min(candidates):
        if sum(l) == target:
            output_list.append(copy.copy(l))
        return

    for idx, elem in enumerate(candidates):
        l.append(elem)
        combination_sum(candidates[idx:], temp_target - elem, l + [elem], target)
        l.remove(elem)


print(combinationSum([2, 3, 6, 7], 7))


# HackerRank kruskalmstrsub problem:
def kruskals(g_nodes, g_from, g_to, g_weight):
    components = {i: {i} for i in range(1, g_nodes + 1)}
    edges = list(zip(g_from, g_to, g_weight))
    edges.sort(key=lambda i: i[2])
    weights_of_edges = 0
    lenght_of_component = 0
    for edge in edges:
        if lenght_of_component == g_nodes:
            break
        tmp = 0
        for k in components.keys():
            if edge[0] in components[k]:
                tmp = k
                break
        for p in components.keys():
            if edge[1] in components[p]:
                if p != tmp:
                    weights_of_edges += edge[2]
                    components[tmp].update(components[p])
                    lenght_of_component = len(components[tmp])
                    del components[p]
                    break

    return weights_of_edges
