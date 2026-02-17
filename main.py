import pygame
import pygame_gui
import time
import tkinter as tk
from tkinter import filedialog
import cv2
import collections
import heapq
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1100, 750
GRID_SIZE = 25
ROWS, COLS = 22, 32
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (1, 1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]

pygame.init()
FONT = pygame.font.SysFont('Arial', 11)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Multi-Algo Visualizer")
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# --- ALGORITHMS ---
def get_neighbors(node, grid):
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] != -1:
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(parent_map, target):
    if target not in parent_map: return None
    path, curr = [], target
    while curr is not None:
        path.append(curr); curr = parent_map[curr]
    return path[::-1]

def bfs(start, target, grid):
    q = collections.deque([start]); visited = {start: None}; explored = []
    while q:
        curr = q.popleft()
        if curr == target: break
        for n in get_neighbors(curr, grid):
            if n not in visited:
                visited[n] = curr; q.append(n); explored.append(n)
    return reconstruct_path(visited, target), explored

def dfs(start, target, grid):
    stack = [start]; visited = {start: None}; explored = []
    # Custom directions for DFS.
    # Priority Order Wanted: Down, Right, Up, Left.
    # Stack is LIFO, so we push in REVERSE priority: Left, Up, Right, Down.
    custom_dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while stack:
        curr = stack.pop()
        if curr == target: break
        
        # Manually check neighbors with custom order and NO DIAGONALS
        for dx, dy in custom_dirs:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] != -1:
                n = (nx, ny)
                if n not in visited:
                    visited[n] = curr; stack.append(n); explored.append(n)
    return reconstruct_path(visited, target), explored

def ucs(start, target, grid, weights):
    pq = [(0, start)]; visited = {start: (None, 0)}; explored = []
    while pq:
        cost, curr = heapq.heappop(pq)
        if curr == target: break
        for n in get_neighbors(curr, grid):
            weight = weights[n[1]][n[0]]
            new_cost = cost + weight
            if n not in visited or new_cost < visited[n][1]:
                visited[n] = (curr, new_cost); heapq.heappush(pq, (new_cost, n)); explored.append(n)
    return reconstruct_path({k: v[0] for k, v in visited.items()}, target), explored

def dls(start, target, grid, limit=20):
    stack = [(start, 0)]; visited = {start: None}; explored = []
    while stack:
        curr, depth = stack.pop()
        if curr == target: return reconstruct_path(visited, target), explored
        if depth < limit:
            for n in get_neighbors(curr, grid):
                if n not in visited:
                    visited[n] = curr; stack.append((n, depth + 1)); explored.append(n)
    return None, explored

def iddfs(start, target, grid):
    all_explored = []
    for limit in range(ROWS * COLS):
        path, explored = dls(start, target, grid, limit)
        all_explored.extend(explored)
        if path: return path, all_explored
    return None, all_explored

def bidirectional(start, goal, grid):
    f_q, b_q = collections.deque([start]), collections.deque([goal])
    f_vis, b_vis = {start: None}, {goal: None}; explored = []
    while f_q and b_q:
        if f_q:
            curr = f_q.popleft()
            for n in get_neighbors(curr, grid):
                if n in b_vis:
                    f_vis[n] = curr
                    return list(reconstruct_path(f_vis, n)) + list(reconstruct_path(b_vis, n))[::-1][1:], explored
                if n not in f_vis:
                    f_vis[n] = curr; f_q.append(n); explored.append(n)
        if b_q:
            curr = b_q.popleft()
            for n in get_neighbors(curr, grid):
                if n in f_vis:
                    b_vis[n] = curr
                    return list(reconstruct_path(f_vis, n)) + list(reconstruct_path(b_vis, n))[::-1][1:], explored
                if n not in b_vis:
                    b_vis[n] = curr; b_q.append(n); explored.append(n)
    return None, explored

# --- IMAGE PROCESSING ---
def scan_maze_secure(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None: return None, False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (COLS, ROWS), interpolation=cv2.INTER_AREA)
        thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        new_grid = [[0 if thresh[r, c] > 127 else -1 for c in range(COLS)] for r in range(ROWS)]
        return new_grid, True
    except:
        return None, False

# --- UI ELEMENTS ---
start_btn = pygame_gui.elements.UIButton(pygame.Rect((830, 20), (230, 45)), 'Start Searching', manager)
reset_btn = pygame_gui.elements.UIButton(pygame.Rect((830, 75), (230, 45)), 'Reset All', manager)
upload_btn = pygame_gui.elements.UIButton(pygame.Rect((830, 130), (230, 45)), 'Upload Maze', manager)
s_btn = pygame_gui.elements.UIButton(pygame.Rect((830, 190), (70, 40)), 'Start', manager)
t_btn = pygame_gui.elements.UIButton(pygame.Rect((910, 190), (70, 40)), 'Target', manager)
e_btn = pygame_gui.elements.UIButton(pygame.Rect((990, 190), (70, 40)), 'End', manager)
algo_options = ['BFS', 'DFS', 'UCS', 'DLS', 'IDDFS', 'Bidirectional']
algo_drop = pygame_gui.elements.UIDropDownMenu(algo_options, 'BFS', pygame.Rect((830, 275), (230, 30)), manager)

def main():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    start = target = end = None
    mode, path, explored = "WALL", [], []
    animating = is_done = show_weights = False; step = 0
    
    while True:
        dt = pygame.time.Clock().tick(60)/1000.0
        screen.fill((235, 238, 242))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            manager.process_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                c, r = (mx - 20) // GRID_SIZE, (my - 50) // GRID_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if mode == 'START': start = (c, r)
                    elif mode == 'TARGET': target = (c, r)
                    elif mode == 'END': end = (c, r)
                    else: grid[r][c] = -1 if grid[r][c] == 0 else 0
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == s_btn: mode = 'START'
                elif event.ui_element == t_btn: mode = 'TARGET'
                elif event.ui_element == e_btn: mode = 'END'
                elif event.ui_element == reset_btn:
                    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                    weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                    start = target = end = None; path = []; explored = []; animating = is_done = show_weights = False
                elif event.ui_element == upload_btn:
                    root = tk.Tk(); root.withdraw()
                    f_path = filedialog.askopenfilename(); root.destroy()
                    if f_path:
                        new_grid, success = scan_maze_secure(f_path)
                        if success:
                            grid = new_grid
                            path = []; explored = []; animating = is_done = False
                elif event.ui_element == start_btn:
                    if start and target:
                        sel = algo_drop.selected_option
                        algo_name = sel[0] if isinstance(sel, tuple) else sel
                        show_weights = (algo_name == 'UCS')
                        
                        if show_weights:
                            weights = [[random.randint(1, 20) if grid[r][c] != -1 else 0 for c in range(COLS)] for r in range(ROWS)]
                            path, explored = ucs(start, target, grid, weights)
                        elif algo_name == 'BFS': path, explored = bfs(start, target, grid)
                        elif algo_name == 'DFS': path, explored = dfs(start, target, grid)
                        elif algo_name == 'DLS': path, explored = dls(start, target, grid)
                        elif algo_name == 'IDDFS': path, explored = iddfs(start, target, grid)
                        elif algo_name == 'Bidirectional': path, explored = bidirectional(start, target, grid)
                        
                        animating, is_done, step = True, False, 0

        if animating:
            if step < len(explored): step += 5
            else: animating, is_done = False, True

        for r in range(ROWS):
            for c in range(COLS):
                rect = (c*GRID_SIZE+20, r*GRID_SIZE+50, GRID_SIZE-2, GRID_SIZE-2)
                color = (255,255,255)
                if grid[r][c] == -1: color = (40,40,40)
                if (c,r) in explored[:step]: color = (180,220,255)
                if is_done and (c,r) in path: color = (0,100,255)
                if (c,r) == start: color = (0,255,100)
                elif (c,r) == target: color = (255,50,50)
                elif (c,r) == end: color = (255,255,0)
                pygame.draw.rect(screen, color, rect, border_radius=4)
                
                if show_weights and grid[r][c] != -1 and (c,r) not in [start, target, end]:
                    val = weights[r][c]
                    txt = FONT.render(str(val), True, (100,100,100))
                    screen.blit(txt, (c*GRID_SIZE+24, r*GRID_SIZE+55))
                    
        manager.update(dt); manager.draw_ui(screen); pygame.display.flip()

if __name__ == "__main__": main()