import random
import heapq
import time
GRID_SIZE = 10
WALL_PROB = 0.25
SCENARIOS = 50
MAX_STEPS = 200

START = (0, 0)
GOAL = (9, 9)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_cost = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == 1:
                    continue

                new_cost = g_cost[current] + 1
                if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

    return None
def random_grid():
    grid = [[0 if random.random() > WALL_PROB else 1 for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)]
    grid[START[0]][START[1]] = 0
    grid[GOAL[0]][GOAL[1]] = 0
    return grid
total_path = 0
total_replan_time = 0
success = 0

for _ in range(SCENARIOS):
    grid = random_grid()
    current = START
    steps = 0

    while steps < MAX_STEPS:
        t0 = time.time()
        path = astar(grid, current, GOAL)
        total_replan_time += time.time() - t0

        if not path:
            break

        next_pos = path[0]

        grid = random_grid()

        if grid[next_pos[0]][next_pos[1]] == 1:
            continue  

        current = next_pos
        steps += 1

        if current == GOAL:
            success += 1
            total_path += steps
            break
print("Scenarios:", SCENARIOS)
print("Success rate:", success / SCENARIOS)
print("Average path length:", total_path / max(success, 1))
print("Average replanning time:", total_replan_time / SCENARIOS)
