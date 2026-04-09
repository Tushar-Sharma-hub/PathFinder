import streamlit as st
import time
import random
import math
import heapq
from collections import deque

# --- Page Config ---
st.set_page_config(page_title="DAA Algorithm Visualizer", layout="wide")

# --- Premium Nord Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #2e3440; color: #eceff4; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #4c566a; color: white; border: none; transition: 0.3s; font-weight: bold; }
    .stButton>button:hover { background-color: #5e81ac; border: 1px solid #88c0d0; }
    .sidebar .sidebar-content { background-color: #3b4252; }
    
    /* Pathfinding Grid */
    .grid-container { display: grid; gap: 2px; padding: 5px; background-color: #4c566a; border-radius: 10px; }
    .grid-item { aspect-ratio: 1; border-radius: 3px; }
    .empty { background-color: #2e3440; }
    .start { background-color: #a3be8c; }
    .end { background-color: #bf616a; }
    .wall { background-color: #4c566a; }
    .open { background-color: #88c0d0; }
    .closed { background-color: #81a1c1; }
    .path { background-color: #ebcb8b; }
    
    /* Chess Grid */
    .chess-board { display: grid; gap: 0px; border: 4px solid #4c566a; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .chess-square { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; font-size: 3em; }
    .chess-light { background-color: #eceff4; color: #2e3440; }
    .chess-dark  { background-color: #81a1c1; color: #2e3440; }
    </style>
""", unsafe_allow_html=True)

# --- Pathfinding State Management ---
if 'grid' not in st.session_state:
    st.session_state.rows = 21
    st.session_state.cols = 31
    st.session_state.start_pos = (5, 5)
    st.session_state.end_pos = (15, 25)
    st.session_state.grid = [['empty' for _ in range(st.session_state.cols)] for _ in range(st.session_state.rows)]
    st.session_state.grid[5][5] = 'start'
    st.session_state.grid[15][25] = 'end'

def reset_grid():
    st.session_state.grid = [['empty' for _ in range(st.session_state.cols)] for _ in range(st.session_state.rows)]
    r1, c1 = st.session_state.start_pos
    r2, c2 = st.session_state.end_pos
    st.session_state.grid[r1][c1] = 'start'
    st.session_state.grid[r2][c2] = 'end'

def clear_path():
    for r in range(st.session_state.rows):
        for c in range(st.session_state.cols):
            if st.session_state.grid[r][c] in ['open', 'closed', 'path']:
                st.session_state.grid[r][c] = 'empty'

def get_neighbors(r, c):
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < st.session_state.rows and 0 <= nc < st.session_state.cols:
            if st.session_state.grid[nr][nc] != 'wall':
                neighbors.append((nr, nc))
    return neighbors

def render_grid(placeholder):
    html = f'<div class="grid-container" style="grid-template-columns: repeat({st.session_state.cols}, 1fr);">'
    for r in range(st.session_state.rows):
        for c in range(st.session_state.cols):
            html += f'<div class="grid-item {st.session_state.grid[r][c]}"></div>'
    html += '</div>'
    placeholder.markdown(html, unsafe_allow_html=True)

# --- SLOWED DOWN Pathfinding Algorithms ---
def run_bfs(placeholder):
    start_time = time.time()
    queue = deque([st.session_state.start_pos])
    came_from = {}
    visited = {st.session_state.start_pos}
    nodes_visited_count = 0
    path_length = 0
    
    while queue:
        curr = queue.popleft()
        if curr == st.session_state.end_pos:
            path_node = curr
            while path_node in came_from:
                path_length += 1
                path_node = came_from[path_node]
                if path_node != st.session_state.start_pos:
                    st.session_state.grid[path_node[0]][path_node[1]] = 'path'
                render_grid(placeholder)
                time.sleep(0.06) 
            return nodes_visited_count, path_length, time.time() - start_time
        
        for n in get_neighbors(*curr):
            if n not in visited:
                visited.add(n)
                came_from[n] = curr
                if st.session_state.grid[n[0]][n[1]] == 'empty':
                    st.session_state.grid[n[0]][n[1]] = 'open'
                queue.append(n)
        
        if curr != st.session_state.start_pos:
            st.session_state.grid[curr[0]][curr[1]] = 'closed'
            nodes_visited_count += 1
        render_grid(placeholder)
        time.sleep(0.04) 
    
    return nodes_visited_count, 0, time.time() - start_time

def run_dfs(placeholder):
    start_time = time.time()
    stack = [st.session_state.start_pos]
    came_from = {}
    visited = {st.session_state.start_pos}
    nodes_visited_count = 0
    path_length = 0
    
    while stack:
        curr = stack.pop()
        if curr == st.session_state.end_pos:
            path_node = curr
            while path_node in came_from:
                path_length += 1
                path_node = came_from[path_node]
                if path_node != st.session_state.start_pos:
                    st.session_state.grid[path_node[0]][path_node[1]] = 'path'
                render_grid(placeholder)
                time.sleep(0.06) 
            return nodes_visited_count, path_length, time.time() - start_time
        
        if curr != st.session_state.start_pos:
            st.session_state.grid[curr[0]][curr[1]] = 'closed'
            nodes_visited_count += 1
            
        for n in reversed(get_neighbors(*curr)):
            if n not in visited:
                visited.add(n)
                came_from[n] = curr
                if st.session_state.grid[n[0]][n[1]] == 'empty':
                    st.session_state.grid[n[0]][n[1]] = 'open'
                stack.append(n)
        
        render_grid(placeholder)
        time.sleep(0.04) 
        
    return nodes_visited_count, 0, time.time() - start_time

def run_astar(placeholder):
    start_time = time.time()
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, 0, count, st.session_state.start_pos))
    came_from = {}
    
    g_score = { (r,c): float('inf') for r in range(st.session_state.rows) for c in range(st.session_state.cols) }
    g_score[st.session_state.start_pos] = 0
    
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
    f_score = { (r,c): float('inf') for r in range(st.session_state.rows) for c in range(st.session_state.cols) }
    f_score[st.session_state.start_pos] = manhattan(st.session_state.start_pos, st.session_state.end_pos)
    
    open_set_hash = {st.session_state.start_pos}
    nodes_visited_count = 0
    path_length = 0
    
    while open_set:
        curr = heapq.heappop(open_set)[3]
        open_set_hash.remove(curr)
        
        if curr == st.session_state.end_pos:
            path_node = curr
            while path_node in came_from:
                path_length += 1
                path_node = came_from[path_node]
                if path_node != st.session_state.start_pos:
                    st.session_state.grid[path_node[0]][path_node[1]] = 'path'
                render_grid(placeholder)
                time.sleep(0.06) 
            return nodes_visited_count, path_length, time.time() - start_time
            
        for n in get_neighbors(*curr):
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[n]:
                came_from[n] = curr
                g_score[n] = temp_g_score
                f_score[n] = temp_g_score + manhattan(n, st.session_state.end_pos)
                if n not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[n], g_score[n], count, n))
                    open_set_hash.add(n)
                    if st.session_state.grid[n[0]][n[1]] == 'empty':
                        st.session_state.grid[n[0]][n[1]] = 'open'
                        
        if curr != st.session_state.start_pos:
            st.session_state.grid[curr[0]][curr[1]] = 'closed'
            nodes_visited_count += 1
            
        render_grid(placeholder)
        time.sleep(0.04) 
        
    return nodes_visited_count, 0, time.time() - start_time

def run_prims_maze(placeholder):
    for r in range(st.session_state.rows):
        for c in range(st.session_state.cols):
            st.session_state.grid[r][c] = 'wall'
    
    nodes = [(r, c) for r in range(1, st.session_state.rows, 2) for c in range(1, st.session_state.cols, 2)]
    if not nodes: return
    
    start_r, start_c = random.choice(nodes)
    st.session_state.grid[start_r][start_c] = 'empty'
    visited = {(start_r, start_c)}
    frontier = []
    
    def add_f(r, c):
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < st.session_state.rows and 0 <= nc < st.session_state.cols:
                if (nr, nc) not in visited: frontier.append((nr, nc, r, c))
    
    add_f(start_r, start_c)
    while frontier:
        idx = random.randint(0, len(frontier) - 1)
        nr, nc, fr, fc = frontier.pop(idx)
        if (nr, nc) not in visited:
            visited.add((nr, nc))
            st.session_state.grid[nr][nc] = 'empty'
            st.session_state.grid[(nr+fr)//2][(nc+fc)//2] = 'empty'
            add_f(nr, nc)
            render_grid(placeholder)
            time.sleep(0.03) 
    
    empty_cells = [(r, c) for r in range(st.session_state.rows) for c in range(st.session_state.cols) if st.session_state.grid[r][c] == 'empty']
    if len(empty_cells) >= 2:
        st.session_state.start_pos = empty_cells[0]
        st.session_state.end_pos = empty_cells[-1]
        st.session_state.grid[st.session_state.start_pos[0]][st.session_state.start_pos[1]] = 'start'
        st.session_state.grid[st.session_state.end_pos[0]][st.session_state.end_pos[1]] = 'end'
    
    render_grid(placeholder)

# --- SLOWED DOWN N-Queens Algorithm ---
def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1: return False
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == 1: return False
    for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
        if board[i][j] == 1: return False
    return True

def render_n_queens(placeholder, board, n):
    html = f'<div class="chess-board" style="grid-template-columns: repeat({n}, 1fr); max-width: 600px; margin: auto;">'
    for r in range(n):
        for c in range(n):
            bg_class = "chess-light" if (r + c) % 2 == 0 else "chess-dark"
            content = "♛" if board[r][c] == 1 else ""
            if content:
                html += f'<div class="chess-square {bg_class}" style="color: #2e3440; text-shadow: 2px 2px #a3be8c;">{content}</div>'
            else:
                html += f'<div class="chess-square {bg_class}"></div>'
    html += '</div>'
    placeholder.markdown(html, unsafe_allow_html=True)

def run_n_queens(placeholder, n):
    start_time = time.time()
    board = [[0]*n for _ in range(n)]
    backtracks = [0]
    states_explored = [0]
    
    def solve(row):
        if row >= n: return True
        for col in range(n):
            states_explored[0] += 1
            board[row][col] = 1
            render_n_queens(placeholder, board, n)
            time.sleep(0.5) 
            
            if is_safe(board, row, col, n):
                if solve(row + 1): return True
            
            backtracks[0] += 1
            board[row][col] = 0
            render_n_queens(placeholder, board, n)
            time.sleep(0.3) 
        return False
        
    render_n_queens(placeholder, board, n)
    solve(0)
    return states_explored[0], backtracks[0], time.time() - start_time


# --- Sorting and Arrays Algorithm ---
def render_array(placeholder, arr, color_indices=None):
    if color_indices is None: color_indices = {}
    html = '<div style="display:flex; align-items:flex-end; justify-content:center; height:300px; gap:4px;">'
    max_val = max(arr) if arr else 1
    for i, val in enumerate(arr):
        color = color_indices.get(i, "#81a1c1") 
        height = max(15, int((val / max_val) * 280)) if max_val > 0 else 15
        html += f'<div style="width:30px; height:{height}px; background-color:{color}; text-align:center; color:#2e3440; font-size:12px; font-weight:bold; border-radius:4px 4px 0 0;">{val}</div>'
    html += '</div>'
    placeholder.markdown(html, unsafe_allow_html=True)

def merge_sort_visual(placeholder, arr, l, r):
    if l < r:
        m = (l + r) // 2
        merge_sort_visual(placeholder, arr, l, m)
        merge_sort_visual(placeholder, arr, m + 1, r)
        
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:m+1]
        R = arr[m+1:r+1]
        i = j = 0
        k = l
        
        while i < n1 and j < n2:
            colors = {x: "#ebcb8b" for x in range(l, r+1)}
            colors[k] = "#bf616a" 
            render_array(placeholder, arr, colors)
            time.sleep(0.1) 
            
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            render_array(placeholder, arr, {k-1: "#a3be8c"})
            time.sleep(0.1)
            
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            render_array(placeholder, arr, {k-1: "#a3be8c"})
            time.sleep(0.1)
            
        render_array(placeholder, arr, {x: "#a3be8c" for x in range(l, r+1)})
        time.sleep(0.1)

def quick_sort_visual(placeholder, arr, low, high):
    if low < high:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            colors = {high: "#bf616a", j: "#ebcb8b", i: "#d08770"}
            render_array(placeholder, arr, colors)
            time.sleep(0.1) 
            
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                render_array(placeholder, arr, {i: "#a3be8c", j: "#a3be8c", high: "#bf616a"})
                time.sleep(0.1)
                
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        render_array(placeholder, arr, {i+1: "#a3be8c"})
        time.sleep(0.1)
        pi = i + 1
        
        quick_sort_visual(placeholder, arr, low, pi - 1)
        quick_sort_visual(placeholder, arr, pi + 1, high)


# --- Main Layout ---
st.title("DAA Algorithm Visualizer")

# --- UI Domain Selector ---
st.sidebar.title("DAA Project Settings")
domain = st.sidebar.selectbox("Select Domain", ["Pathfinding Grid", "N-Queens (Backtracking)", "Arrays & Sorting"])
st.sidebar.markdown("---")

if domain == "Pathfinding Grid":
    metrics_placeholder = st.empty()
    grid_placeholder = st.empty()
    
    def show_metrics(nodes, path, duration):
        with metrics_placeholder.container():
            st.markdown("### 📊 Pathfinder Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Visualization Time", f"{duration:.3f} sec")
            col2.metric("Space (Nodes Explored)", f"{nodes}")
            col3.metric("Path Length Found", f"{path}")

    st.sidebar.subheader("Pathfinder Config")
    algo = st.sidebar.radio("Algorithm", ["Graph Colouring (BFS)", "Hamiltonian (Backtracking DFS)", "A* (Heuristic)"])
    
    if st.sidebar.button("Start Visualization"):
        clear_path()
        metrics_placeholder.empty()
        if algo == "Graph Colouring (BFS)": metrics = run_bfs(grid_placeholder)
        elif algo == "Hamiltonian (Backtracking DFS)": metrics = run_dfs(grid_placeholder)
        else: metrics = run_astar(grid_placeholder)
            
        if metrics: show_metrics(metrics[0], metrics[1], metrics[2])
            
    if st.sidebar.button("Generate Prim's Maze"):
        run_prims_maze(grid_placeholder)
        metrics_placeholder.empty()
        
    if st.sidebar.button("Reset Grid"):
        reset_grid()
        metrics_placeholder.empty()
        
    render_grid(grid_placeholder)

elif domain == "N-Queens (Backtracking)":
    metrics_placeholder = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    board_placeholder = st.empty()
    
    st.sidebar.subheader("N-Queens Config")
    n_size = st.sidebar.slider("Select N (Board Size)", min_value=4, max_value=8, value=4)
    
    def show_nq_metrics(states, backtracks, duration):
        with metrics_placeholder.container():
            st.markdown("### 📊 N-Queens Analysis")
            col1, col2, col3 = st.columns(3)
            col1.metric("Visualization Time", f"{duration:.3f} sec")
            col2.metric("States Explored", f"{states}")
            col3.metric("Backtracks Performed", f"{backtracks}")
            
    if st.sidebar.button("Solve N-Queens"):
        metrics_placeholder.empty()
        metrics = run_n_queens(board_placeholder, n_size)
        if metrics:
            show_nq_metrics(metrics[0], metrics[1], metrics[2])
    else:
        empty_board = [[0]*n_size for _ in range(n_size)]
        render_n_queens(board_placeholder, empty_board, n_size)

elif domain == "Arrays & Sorting":
    metrics_placeholder = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    array_placeholder = st.empty()
    
    st.sidebar.subheader("Array Config")
    algo = st.sidebar.radio("Algorithm", ["Quick Sort (Divide & Conquer)", "Merge Sort (Divide & Conquer)"])
    arr_size = st.sidebar.slider("Array Size", min_value=10, max_value=25, value=15)
    
    if 'unsorted_arr' not in st.session_state or st.session_state.get('arr_last_size') != arr_size:
        st.session_state.unsorted_arr = [random.randint(10, 100) for _ in range(arr_size)]
        st.session_state.arr_last_size = arr_size
        
    def show_array_metrics(duration):
        with metrics_placeholder.container():
            st.markdown("### 📊 Array Analysis")
            col1, col2 = st.columns(2)
            col1.metric("Visualization Time", f"{duration:.3f} sec")
            col2.metric("Array Size Analyzed", f"N = {arr_size}")

    if st.sidebar.button(f"Run {algo}"):
        metrics_placeholder.empty()
        arr_copy = st.session_state.unsorted_arr.copy()
        start = time.time()
        
        if "Quick" in algo:
            quick_sort_visual(array_placeholder, arr_copy, 0, len(arr_copy)-1)
            render_array(array_placeholder, arr_copy, {x: "#a3be8c" for x in range(len(arr_copy))})
            show_array_metrics(time.time() - start)
        elif "Merge" in algo:
            merge_sort_visual(array_placeholder, arr_copy, 0, len(arr_copy)-1)
            render_array(array_placeholder, arr_copy, {x: "#a3be8c" for x in range(len(arr_copy))})
            show_array_metrics(time.time() - start)
            
    if st.sidebar.button("Generate New Array"):
        st.session_state.unsorted_arr = [random.randint(10, 100) for _ in range(arr_size)]
        metrics_placeholder.empty()
        
    render_array(array_placeholder, st.session_state.unsorted_arr)
