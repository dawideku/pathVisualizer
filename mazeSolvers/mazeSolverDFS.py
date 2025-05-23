class MazeSolverDFS:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.path = []
        self.steps = []
        self.start = self._find_start()
        self.end = self._find_end()
        self.found = False

    def _find_start(self):
        for row in range(self.rows):
            if self.maze[row][0] == 0:
                return row, 0
        return None

    def _find_end(self):
        for row in range(self.rows):
            if self.maze[row][self.cols - 1] == 0:
                return row, self.cols - 1
        return None

    def step_by_step_solve(self):
        if not self.start or not self.end:
            return

        yield from self._dfs(self.start[0], self.start[1])

    def _dfs(self, row, col):
        if self.found:
            return
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if self.maze[row][col] == 1 or self.visited[row][col]:
            return

        self.visited[row][col] = True
        self.path.append((row, col))
        self.steps.append((row, col))
        yield row, col, list(self.path)

        if (row, col) == self.end:
            self.found = True
            return

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            yield from self._dfs(row + dr, col + dc)

        if not self.found:
            self.path.pop()
            yield row, col, list(self.path)
