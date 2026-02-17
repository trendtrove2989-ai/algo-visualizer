import collections
import heapq

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (1, 1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]

def get_neighbors(node, grid, rows, cols):
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != -1:
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(parent_map, target):
    if target not in parent_map: return None
    path, curr = [], target
    while curr is not None:
        path.append(curr)
        curr = parent_map[curr]
    return path[::-1]

def bfs(start, target, grid, rows, cols):
    queue = collections.deque([start])
    visited = {start: None}
    explored = []
    while queue:
        curr = queue.popleft()
        if curr == target: break
        for n in get_neighbors(curr, grid, rows, cols):
            if n not in visited:
                visited[n] = curr
                queue.append(n)
                explored.append(n)
    return reconstruct_path(visited, target), explored

def dfs(start, target, grid, rows, cols):
    stack = [start]
    visited = {start: None}
    explored = []
    while stack:
        curr = stack.pop()
        if curr == target: break
        for n in get_neighbors(curr, grid, rows, cols):
            if n not in visited:
                visited[n] = curr
                stack.append(n)
                explored.append(n)
    return reconstruct_path(visited, target), explored

def ucs(start, target, grid, rows, cols):
    pq = [(0, start)]
    visited = {start: (None, 0)}
    explored = []
    while pq:
        cost, curr = heapq.heappop(pq)
        if curr == target: break
        for n in get_neighbors(curr, grid, rows, cols):
            new_cost = cost + 1
            if n not in visited or new_cost < visited[n][1]:
                visited[n] = (curr, new_cost)
                heapq.heappush(pq, (new_cost, n))
                explored.append(n)
    return reconstruct_path({k: v[0] for k, v in visited.items()}, target), explored

def dls(start, target, grid, rows, cols, limit=20):
    stack = [(start, 0)]
    visited = {start: None}
    explored = []
    while stack:
        curr, depth = stack.pop()
        if curr == target: return reconstruct_path(visited, target), explored
        if depth < limit:
            for n in get_neighbors(curr, grid, rows, cols):
                if n not in visited:
                    visited[n] = curr
                    stack.append((n, depth + 1))
                    explored.append(n)
    return None, explored

def iddfs(start, target, grid, rows, cols):
    all_explored = []
    for limit in range(rows * cols):
        path, explored = dls(start, target, grid, rows, cols, limit)
        all_explored.extend(explored)
        if path: return path, all_explored
    return None, all_explored

def bidirectional(start, goal, grid, rows, cols):
    f_q, b_q = collections.deque([start]), collections.deque([goal])
    f_vis, b_vis = {start: None}, {goal: None}
    explored = []
    explored.append(start)
    explored.append(goal)

    while f_q and b_q:
        if f_q:
            c_f = f_q.popleft()
            for n in get_neighbors(c_f, grid, rows, cols):
                if n in b_vis:
                    f_vis[n] = c_f
                    path = list(reconstruct_path(f_vis, n)) + list(reconstruct_path(b_vis, n))[::-1][1:]
                    return path, explored
                if n not in f_vis:
                    f_vis[n] = c_f
                    f_q.append(n)
                    explored.append(n)
        if b_q:
            c_b = b_q.popleft()
            for n in get_neighbors(c_b, grid, rows, cols):
                if n in f_vis:
                    b_vis[n] = c_b
                    path = list(reconstruct_path(f_vis, n)) + list(reconstruct_path(b_vis, n))[::-1][1:]
                    return path, explored
                if n not in b_vis:
                    b_vis[n] = c_b
                    b_q.append(n)
                    explored.append(n)
    return None, explored