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


# print(combinationSum([2, 3, 6, 7], 7))


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


def read_input():
    values = []
    with open("input.txt", "r") as f:
        for line in f.readlines():
            tmp = line.strip()
            a, b = tmp.split(" ")
            values.append([int(a), int(b)])

    return values


# components-in-graph problem
def componentsInGraph(gb):
    gb.sort(key=lambda i: i[0])
    n = gb[-1][0]
    components = {i: {i} for i in range(1, n + 1)}
    visited = {i: i for i in range(1, n + 1)}
    for edge in gb:
        node1, node2 = edge[0], edge[1]
        if node2 in visited:
            if visited[node2] != visited[node1]:
                components[visited[node2]].update(components[visited[node1]])
                tmp = visited[node1]
                for v in components[visited[node1]]:
                    visited[v] = visited[node2]
                del components[tmp]
        else:
            if not components.get(node1):
                components[visited[node1]].add(node2)
                visited[node2] = visited[node1]
            else:
                components[node1].add(node2)
                visited[node2] = node1

    val = components.values()
    comp_sizes = list(map(lambda x: len(x), filter(lambda i: len(i) > 1, val)))
    return min(comp_sizes), max(comp_sizes)


print(componentsInGraph(read_input()))


# 437. Path Sum III
from collections import defaultdict


class Solution:
    def __init__(self):
        self.output = 0

    def pathSum(self, root, targetsum):
        visited_values = defaultdict(lambda: 0)

        def path_sum(root, targetsum, parent_value):
            if not root:
                return
            root.val += parent_value
            if root.val == targetsum:
                self.output += 1
            if (root.val - targetsum) in visited_values:
                self.output += visited_values[root.val - targetsum]
            visited_values[root.val] += 1

            path_sum(root.left, targetsum, root.val)
            path_sum(root.right, targetsum, root.val)

            visited_values[root.val] -= 1

        path_sum(root=root, targetsum=targetsum, parent_value=0)

        return self.output


# 6. Zigzag Conversion
def convert(s: str, numRows: int) -> str:
    if numRows == 1:
        return s
    length = len(s)
    i, j, n = 0, 0, 0
    out = []
    while n < length:
        out.append((i, j, s[n]))
        i += 1
        n += 1
        if i == numRows - 1:
            while i > 0 and n < length:
                out.append((i, j, s[n]))
                i -= 1
                j += 1
                n += 1

    out = sorted(out)

    return "".join(list(zip(*out))[2])


# 24. Swap nodes in pairs
def swapPairs(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return None
    if head.next:
        h = head.next
    else:
        return head

    start = ListNode(next=head)

    while head and head.next:
        tmp = head.next
        if head.next and head.next.next:
            head.next = head.next.next
        else:
            head.next = None
        start.next = tmp
        tmp.next = head
        start = head
        head = head.next

    return h


# 32 Longest valid parentheses
def longestValidParentheses(s: str) -> int:
    if s == "":
        return 0
    stack = []
    longest = 0
    start = 0

    for indx, element in enumerate(s):
        if element == "(":
            stack.append(("(", indx))
        else:
            if not stack:
                start = indx + 1
            else:
                stack.pop()
                if not stack:
                    l = indx - start + 1
                else:
                    l = indx - stack[-1][1]

                if l > longest:
                    longest = l

    return longest
