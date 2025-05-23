from mazeGenerators.kruskal import KruskalMazeGenerator
from mazeRenderer import MazeRenderer
from mazeSolvers.mazeSolverDFS import MazeSolverDFS

n = 20
mazeGenerator = KruskalMazeGenerator(n)
squares = mazeGenerator.get_maze()
solver = MazeSolverDFS(squares)
solver_generator = solver.step_by_step_solve()
renderer = MazeRenderer(squares, solver_generator)
renderer.run()
