from flask import Flask, render_template_string, request
import random
from collections import deque

app = Flask(__name__)

# -------- Maze Generation (DFS Backtracking) --------
def generate_maze(rows, cols):
    maze = [['#'] * cols for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = ' '

    while stack:
        x, y = stack[-1]
        directions = [(-2,0), (2,0), (0,-2), (0,2)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < rows-1 and 1 <= ny < cols-1 and maze[nx][ny] == '#':
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[x + dx//2][y + dy//2] = ' '
            maze[nx][ny] = ' '
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze

# -------- Maze Solver (BFS for shortest path) --------
def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    start, end = (1, 1), (rows-2, cols-2)
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == ' ' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None

# -------- Convert Maze to HTML Table --------
def maze_to_html(maze, path=None):
    html = "<table style='border-collapse:collapse;'>"
    for i, row in enumerate(maze):
        html += "<tr>"
        for j, cell in enumerate(row):
            if path and (i, j) in path:
                color = "yellow"  # solved path
            elif cell == "#":
                color = "black"
            else:
                color = "white"
            html += f"<td style='width:15px;height:15px;background:{color};border:1px solid #ccc;'></td>"
        html += "</tr>"
    html += "</table>"
    return html

# -------- Flask Routes --------
maze = generate_maze(41, 41)  # bigger & more complex maze

@app.route('/', methods=['GET', 'POST'])
def index():
    global maze
    solved_path = None
    if request.method == 'POST':
        if 'generate' in request.form:
            maze = generate_maze(41, 41)
        elif 'solve' in request.form:
            solved_path = solve_maze(maze)
    maze_html = maze_to_html(maze, solved_path)
    return render_template_string(f"""
    <html>
    <head>
        <title>Maze Generator & Solver</title>
        <style>
            body {{ background:#f4f4f4; text-align:center; font-family:Arial; }}
            h1 {{ color:#333; }}
            button {{
                background-color:#4CAF50;
                color:white;
                border:none;
                padding:10px 20px;
                margin:10px;
                border-radius:5px;
                cursor:pointer;
            }}
            button:hover {{ background-color:#45a049; }}
        </style>
    </head>
    <body>
        <h1>Maze Generator & Solver - DAA Project</h1>
        <form method='POST'>
            <button name='generate'>Generate New Maze</button>
            <button name='solve'>Solve Maze</button>
        </form>
        <div style='display:inline-block;margin-top:10px;'>{maze_html}</div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(port=5000)
