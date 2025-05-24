import random

class BinaryTreeMazeGenerator:
    def __init__(self, size, add_entrance_exit=True):
        self.n = size
        self.add_entrance_exit = add_entrance_exit
        self.maze = []
        self.regenerate()

    def regenerate(self):
        generator = self._generate_maze_step_by_step()
        for state in generator:
            self.maze = state

    def _generate_maze_step_by_step(self):
        n = self.n
        size = 2 * n + 1
        maze = [[1 for _ in range(size)] for _ in range(size)]

        for row in range(n):
            for col in range(n):
                maze[2 * row + 1][2 * col + 1] = 0
                yield [row[:] for row in maze]

        for row in range(n):
            for col in range(n):
                directions = []
                if row > 0:
                    directions.append('N')
                if col < n - 1:
                    directions.append('E')

                if directions:
                    direction = random.choice(directions)
                    r, c = 2 * row + 1, 2 * col + 1

                    if direction == 'N':
                        maze[r - 1][c] = 0
                    elif direction == 'E':
                        maze[r][c + 1] = 0

                    yield [row[:] for row in maze]

        if self.add_entrance_exit:
            maze[1][0] = 0
            yield [row[:] for row in maze]
            maze[2 * n - 1][2 * n] = 0
            yield [row[:] for row in maze]

    def get_maze(self):
        return self.maze

