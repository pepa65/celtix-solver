from collections import Counter

from ortools.sat.python import cp_model
import networkx as nx

from common import *


def get_matches(x, y, orientation):
    if orientation == Orientation.horizontal:
        return [((x, y), (x+1, y)), ((x, y+1), (x+1, y+1))]
    elif orientation == Orientation.vertical:
        return [((x, y), (x, y+1)), ((x+1, y), (x+1, y+1))]
    else:
        return [((x, y), (x+1, y+1)), ((x, y+1), (x+1, y))]

def build_model(puzzle):
    model = cp_model.CpModel()
    colors = {
        (x, y): model.new_int_var(0, puzzle.n_colors - 1, f"color_{x}_{y}")
        for x in range(puzzle.width)
        for y in range(puzzle.height)
    }
    for c, points in enumerate(puzzle.pips.values()):
        for point in points:
            model.add(colors[point] == c)
    for a, b in puzzle.edge_connections():
        model.add(colors[a] == colors[b])

    crossings = {}
    for x, y in puzzle.cross_positions():
        choices = {
            orientation: model.new_bool_var(f"cross_{x}_{y}_{orientation}")
            for orientation in (None, *Orientation)
        }
        model.add_exactly_one(choices.values())
        for orientation, chosen in choices.items():
            for a, b in get_matches(x, y, orientation):
                model.add(colors[a] == colors[b]).only_enforce_if(chosen)
        crossings[x, y] = choices

    model.minimize(sum(choices[o] for choices in crossings.values() for o in Orientation))
    return model, crossings


def find_loops(puzzle, walls):
    # Build the connectivity between ribbon segments
    G = nx.Graph()
    G.add_nodes_from((x, y) for x in range(puzzle.width) for y in range(puzzle.height))
    G.add_edges_from(puzzle.edge_connections())
    for x, y in puzzle.cross_positions():
        G.add_edges_from(get_matches(x, y, walls.get((x, y))))
    # Ribbon loops are connected components of that graph
    return [set(component) for component in nx.connected_components(G)]

def solve_puzzle(puzzle):
    if not puzzle.pips:
        raise ValueError("Puzzle has no pips")
    model, crossings = build_model(puzzle)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    pips = {point: color for color, points in puzzle.pips.items() for point in points}

    while True:
        status = solver.solve(model)
        if status == cp_model.INFEASIBLE:
            raise ValueError("Puzzle has no solution")
        if status != cp_model.OPTIMAL:
            raise RuntimeError(f"Could not prove a minimum solution: {solver.status_name(status)}")

        walls = {
            point: orientation
            for point, choices in crossings.items()
            for orientation in Orientation if solver.value(choices[orientation])
        }
        loops = find_loops(puzzle, walls)
        # The color constraints ensure each loop has at most one pip color.
        loop_colors = [next((pips[p] for p in loop if p in pips), None) for loop in loops]
        counts = Counter(loop_colors)
        invalid = [
            loop for loop, color in zip(loops, loop_colors)
            if color is None or counts[color] > 1
        ]
        if not invalid:
            return [Wall(x, y, orientation) for (x, y), orientation in walls.items()]
        print(f"Tentative solution with {len(walls)} walls, excluding {len(invalid)} invalid loops")
        for loop in invalid:
            # A valid solution must connect this set of points to the rest
            # of the board, even if its internal crossings are rearranged.
            model.add_bool_or(
                chosen
                for (x, y), choices in crossings.items()
                for orientation, chosen in choices.items()
                if any((a in loop) != (b in loop) for a, b in get_matches(x, y, orientation))
            )
