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


# print(combinationSum([2,3,6,7],7))