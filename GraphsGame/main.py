from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
]

grid = Grid(matrix = matrix)

begin = grid.node(0,0)

end = grid.node(5,2)


search = AStarFinder()

path,runs = search.find_path(begin, end, grid)

print(path)
