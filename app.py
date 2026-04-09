import streamlit as st
import time
import random
from collections import deque

# --- Page Config ---
st.set_page_config(page_title="DAA Pathfinding Visualizer", layout="wide")

# --- Premium Nord Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #2e3440;
        color: #eceff4;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #4c566a;
        color: white;
        border: none;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #5e81ac;
        border: 1px solid #88c0d0;
    }
    .sidebar .sidebar-content {
        background-color: #3b4252;
    }
    .grid-container {
        display: grid;
        gap: 2px;
        padding: 5px;
        background-color: #4c566a;
        border-radius: 10px;
    }
    .grid-item {
        aspect-ratio: 1;
        border-radius: 3px;
    }
    .empty { background-color: #2e3440; }
    .start { background-color: #a3be8c; }
    .end { background-color: #bf616a; }
    .wall { background-color: #4c566a; }
    .open { background-color: #88c0d0; }
    .closed { background-color: #81a1c1; }
    .path { background-color: #ebcb8b; }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if 'grid' not in st.session_state:
    st.session_state.rows = 21  # MUST BE ODD for maze generation
    st.session_state.cols = 31  # MUST BE ODD for maze generation
    st.session_state.grid = [['empty' for _ in range(st.session_state.cols)] for _ in range(st.session_state.rows)]
    st.session_state.start_pos = (5, 5)
    st.session_state.end_pos = (15, 25)
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

# --- Algorithm Helper ---
def get_neighbors(r, c):
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < st.session_state.rows and 0 <= nc < st.session_state.cols:
            if st.session_state.grid[nr][nc] != 'wall':
                neighbors.append((nr, nc))
    return neighbors

# --- Rendering ---
def render_grid(placeholder):
    html = f'<div class="grid-container" style="grid-template-columns: repeat({st.session_state.cols}, 1fr);">'
    for r in range(st.session_state.rows):
        for c in range(st.session_state.cols):
            html += f'<div class="grid-item {st.session_state.grid[r][c]}"></div>'
    html += '</div>'
    placeholder.markdown(html, unsafe_allow_html=True)

# --- BFS (Graph Colouring) ---
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
                time.sleep(0.02)
            end_time = time.time()
            return nodes_visited_count, path_length, end_time - start_time
        
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
        time.sleep(0.01)
    
    return nodes_visited_count, 0, time.time() - start_time

# --- DFS (Hamiltonian Backtracking) ---
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
                time.sleep(0.02)
            end_time = time.time()
            return nodes_visited_count, path_length, end_time - start_time
        
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
        time.sleep(0.01)
        
    return nodes_visited_count, 0, time.time() - start_time

# --- Prim's Maze ---
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
            time.sleep(0.01)
    
    empty_cells = [(r, c) for r in range(st.session_state.rows) for c in range(st.session_state.cols) if st.session_state.grid[r][c] == 'empty']
    if len(empty_cells) >= 2:
        st.session_state.start_pos = empty_cells[0]
        st.session_state.end_pos = empty_cells[-1]
        st.session_state.grid[st.session_state.start_pos[0]][st.session_state.start_pos[1]] = 'start'
        st.session_state.grid[st.session_state.end_pos[0]][st.session_state.end_pos[1]] = 'end'
    
    render_grid(placeholder)

# --- Layout ---
st.title("Interactive Pathfinder")

metrics_placeholder = st.empty()
grid_placeholder = st.empty()

def show_metrics(nodes, path, duration):
    with metrics_placeholder.container():
        st.markdown("### 📊 Algorithm Analysis Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Visualization Time", f"{duration:.3f} sec")
        col2.metric("Space (Nodes Explored)", f"{nodes}")
        col3.metric("Path Length Found", f"{path}")

# --- Sidebar ---
st.sidebar.title("DAA Pathfinder")
st.sidebar.subheader("Configuration")
algo = st.sidebar.radio("Algorithm", ["Graph Colouring (BFS)", "Hamiltonian (Backtracking DFS)"])

if st.sidebar.button("Start Visualization"):
    clear_path()
    metrics_placeholder.empty()
    if algo == "Graph Colouring (BFS)": 
        metrics = run_bfs(grid_placeholder)
    else: 
        metrics = run_dfs(grid_placeholder)
        
    if metrics:
        show_metrics(metrics[0], metrics[1], metrics[2])

if st.sidebar.button("Generate Prim's Maze"):
    run_prims_maze(grid_placeholder)
    metrics_placeholder.empty()

if st.sidebar.button("Reset Grid"):
    reset_grid()
    metrics_placeholder.empty()

# Render standard layout at script completion
render_grid(grid_placeholder)

st.sidebar.info("Click 'Start Visualization' to see the algorithms in action. Use 'Generate Maze' to create obstacles.")
