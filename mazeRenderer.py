import pygame

class MazeRenderer:
    def __init__(self, maze, solver_generator, cell_size=10, color_wall=(150,10,100), color_path=(150,250,100)):
        self.cell_size = cell_size
        self.color_wall = color_wall
        self.color_path = color_path
        self.maze = maze
        self.solver_generator = solver_generator
        self.size = len(maze)

        pygame.init()
        self.screen = pygame.display.set_mode((self.size * cell_size, self.size * cell_size))
        self.clock = pygame.time.Clock()
        self.running = True

    def set_maze(self, maze):
        self.maze = maze


    def run_step_by_step(self):
        for step in self.solver_generator:
            row, col, current_path = step
            self.screen.fill((0, 0, 0))
            for i in range(self.size):
                for j in range(self.size):
                    color = self.color_wall if self.maze[i][j] == 1 else self.color_path
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size,
                                                 self.cell_size))

            pygame.draw.rect(self.screen, (0, 100, 255),
                             pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

            for r, c in current_path:
                pygame.draw.rect(self.screen, (255, 0, 0),
                                 pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

            pygame.display.flip()
            pygame.time.wait(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def run(self):
        while self.running:
            self.run_step_by_step()
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()
