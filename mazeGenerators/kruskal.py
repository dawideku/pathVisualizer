import random

class KruskalMazeGenerator:
    class DisjointSet:
        def __init__(self, size):
            self.parent = list(range(size))

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            root_x = self.find(x)
            root_y = self.find(y)
            if root_x != root_y:
                self.parent[root_y] = root_x
                return True
            return False

    def __init__(self, size, add_entrance_exit=True):
        self.n = size
        self.add_entrance_exit = add_entrance_exit
        self.maze = None
        self.generator = self._generate_maze_step_by_step()

    def regenerate(self):
        self.generator = self._generate_maze_step_by_step()

    def _generate_maze_step_by_step(self):
        n = self.n
        total_cells = n * n
        ds = self.DisjointSet(total_cells)

        edges = []
        for row in range(n):
            for col in range(n):
                cell = row * n + col
                if col < n - 1:
                    edges.append((cell, cell + 1))
                if row < n - 1:
                    edges.append((cell, cell + n))
        random.shuffle(edges)

        size = 2 * n + 1
        maze = [[1 for _ in range(size)] for _ in range(size)]

        for row in range(n):
            for col in range(n):
                maze[2 * row + 1][2 * col + 1] = 0
                yield [r[:] for r in maze]

        for cell1, cell2 in edges:
            if ds.union(cell1, cell2):
                r1, c1 = divmod(cell1, n)
                r2, c2 = divmod(cell2, n)
                wall_r = r1 + r2 + 1
                wall_c = c1 + c2 + 1
                maze[wall_r][wall_c] = 0
                yield [r[:] for r in maze]

        if self.add_entrance_exit:
            maze[1][0] = 0
            yield [r[:] for r in maze]
            maze[2 * n - 1][2 * n] = 0
            yield [r[:] for r in maze]

        self.maze = maze

    def get_maze(self):
        return self.maze
