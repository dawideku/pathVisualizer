import pygame
from mazeSolvers.mazeSolverDFS import MazeSolverDFS
from mazeGenerators.binaryTree import BinaryTreeMazeGenerator
from mazeGenerators.kruskal import KruskalMazeGenerator

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

class MazeUI:
    def __init__(self, size=20, cell_size=10):
        self.generator_classes = [BinaryTreeMazeGenerator, KruskalMazeGenerator]
        self.current_generator_index = 0

        self.size = size
        self.cell_size = cell_size

        self.set_generator(self.generator_classes[self.current_generator_index])

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generator & Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        self.show_animation = True

        self.generating = True

        self.buttons = [
            Button(self.cols * cell_size + 30, 30, 120, 40, "Start DFS", self.font, (0, 200, 0), (255, 255, 255), self.start_dfs),
            Button(self.cols * cell_size + 30, 90, 120, 40, "Reset", self.font, (200, 100, 0), (255, 255, 255), self.reset),
            Button(self.cols * cell_size + 30, 150, 120, 40, "New Maze", self.font, (0, 100, 200), (255, 255, 255), self.new_maze)
        ]

        self.animation_button = Button(
            self.cols * cell_size + 30, 330, 120, 40,
            "Animation: ON",
            self.font,
            (100, 100, 100),
            (255, 255, 255),
            self.toggle_animation
        )

        self.buttons.append(self.animation_button)

        self.generator_buttons = []

        def make_action(index):
            return lambda: self.select_generator(index)

        for i, gen_cls in enumerate(self.generator_classes):
            btn = Button(
                self.cols * self.cell_size + 30,
                210 + i * 50,
                120, 40,
                f"Use {gen_cls.__name__}",
                self.font,
                (50, 50, 200),
                (255, 255, 255),
                action=make_action(i)
            )
            self.generator_buttons.append(btn)

    def toggle_animation(self):
        self.show_animation = not self.show_animation
        label = "Animation: ON" if self.show_animation else "Animation: OFF"
        self.animation_button.text = label
        print(f"Animation toggled: {self.show_animation}")

    def set_generator(self, generator_class):
        self.generator_class = generator_class
        self.generator = generator_class(self.size)
        self.generator_steps = self.generator._generate_maze_step_by_step()
        self.maze = [[1 for _ in range(self.size * 2 + 1)] for _ in range(self.size * 2 + 1)]
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.width = self.cols * self.cell_size + 180
        self.height = self.rows * self.cell_size
        self.generating = True
        self.solver_generator = None
        self.path = []

    def select_generator(self, index):
        if index != self.current_generator_index:
            self.current_generator_index = index
            self.set_generator(self.generator_classes[index])

    def start_dfs(self):
        if not self.generating:
            self.solver = MazeSolverDFS(self.maze)
            self.solver_generator = self.solver.step_by_step_solve()
            self.path = []

    def reset(self):
        self.solver_generator = None
        self.path = []

    def new_maze(self):
        self.set_generator(self.generator_class)

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(self.rows):
            for j in range(self.cols):
                color = (150, 10, 100) if self.maze[i][j] == 1 else (150, 250, 100)
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

        for r, c in self.path:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

        for button in self.buttons + self.generator_buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()

            if self.generating:
                if self.show_animation:
                    try:
                        self.maze = next(self.generator_steps)
                        pygame.time.wait(10)
                    except StopIteration:
                        self.generating = False
                        self.generator.maze = self.maze
                else:
                    for maze in self.generator_steps:
                        self.maze = maze
                    self.generating = False
                    self.generator.maze = self.maze
            elif self.solver_generator:
                if self.show_animation:
                    try:
                        row, col, current_path = next(self.solver_generator)
                        self.path = current_path
                        pygame.time.wait(15)

                    except StopIteration:
                        self.solver_generator = None

                else:
                    for row, col, current_path in self.solver_generator:
                        self.path = current_path
                    self.solver_generator = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons + self.generator_buttons:
                    button.handle_event(event)

            self.clock.tick(60)

        pygame.quit()
