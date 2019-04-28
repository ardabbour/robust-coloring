# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Instance Generator

    Generates a problem instance for the robust coloring problem.

    Author: Abdul Rahman Dabbour
    Affiliation: CogRobo Lab, FENS, Sabanci University
    License: GNU General Public License v3.0
    Repository: https://github.com/ardabbour/robust-coloring/
"""

import argparse
import itertools
import random


K_VALUES = {
    'myciel3': [6, 8],
    'myciel4': [8, 10],
    'queen5_5': [8, 10],
    '1-FullIns_3': [6, 8],
    'queen6_6': [11, 14],
    '2-Insertions_3': [6, 8],
    'myciel5': [9, 12],
    'queen7_7': [11, 14],
    '2-FullIns_3': [8, 10],
    '3-Insertions_3': [6, 8],
    'queen8_8': [14, 18],
    '1-Insertions_4': [8, 10],
    'huck': [17, 22],
    '4-Insertions_3': [6, 8],
    '3-FullIns_3': [9, 12],
    'jean': [15, 20],
    'queen9_9': [15, 20],
    'david': [17, 22],
    'mug88_1': [6, 8],
    'mug88_25': [6, 8],
    '1-FullIns_4': [8, 10],
    'myciel6': [11, 14],
    'queen8_12': [18, 24],
    'mug100_1': [6, 8],
    'mug100_25': [6, 8],
    'queen10_10': [17, 22],
    '4-FullIns_3': [11, 14],
    'games120': [14, 18],
    'queen11_11': [17, 22],
    'DSJC125_1': [8, 10],
    'DSJC125_5': [26, 34],
    'DSJC125_9': [66, 88],
    'miles1000': [63, 84],
    'miles1500': [110, 156],
    'miles250': [12, 16],
    'miles500': [30, 40],
    'miles750': [47, 62],
    'anna': [17, 22],
    'queen12_12': [18, 24],
    '2-Insertions_4': [6, 8],
}


def get_costs(max_vertex, edges, rand, seed, const_cost, prod_cost, max_vertices, max_cost):
    """Generates costs for the non-adjacent vertices."""

    if seed == -1:
        seed = None
    random.seed(seed)

    all_pairs = set(itertools.combinations(range(1, max_vertex+1), 2))
    non_adjacent_pairs = all_pairs.difference(edges)
    costs_to_write = []
    if rand:
        if max_vertices > 0:
            non_adjacent_pairs = random.choices(
                non_adjacent_pairs, max_vertices)
        for pair in non_adjacent_pairs:
            costs_to_write.append('cost({},{},{}).\n'.format(
                pair[0], pair[1], random.randint(1, max_cost)))
    elif const_cost > 0:
        if max_vertices > 0:
            non_adjacent_pairs = non_adjacent_pairs[:max_vertices]
        for pair in non_adjacent_pairs:
            costs_to_write.append('cost({},{},{}).\n'.format(
                pair[0], pair[1], const_cost))
    elif prod_cost:
        if max_vertices > 0:
            non_adjacent_pairs = non_adjacent_pairs[:max_vertices]
        for pair in non_adjacent_pairs:
            costs_to_write.append('cost({},{},{}).\n'.format(
                pair[0], pair[1], pair[0]*pair[1]))

    return costs_to_write


def extract_info(input_path):
    """Extracts graph information."""

    edges = set()
    with open(input_path) as f:
        for line in f.readlines():
            if line[0] == 'e':
                edge = line.split(' ')
                edges.add((int(edge[1]), int(edge[2].replace('\n', ''))))
            elif line[0] == 'p':
                max_vertex = int(line.split(' ')[-2])

    return max_vertex, edges


def write_result(output_path, no_of_colors, max_vertex, edges, costs_to_write):
    """Dumps all the information (graph description + costs) to a file."""

    edges_to_write = ['edge({},{}).\n'.format(x, y) for (x, y) in edges]
    with open(output_path, 'w') as f:
        f.write('% Number of colors\n')
        f.write('#const k = {}.\n'.format(no_of_colors))
        f.write('\n')
        f.write('% Vertices\n')
        f.write('vertex(1..{}).\n'.format(max_vertex))
        f.write('\n')
        f.write('% Edges\n')
        f.writelines(edges_to_write)
        f.write('\n')
        f.write('% Costs\n')
        f.writelines(costs_to_write)

    return output_path


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Generates a problem instance for the robust coloring problem.')
    PARSER.add_argument('input',
                        help='Input file path.',
                        type=str)
    PARSER.add_argument('--output', '-o',
                        default='graph.lp',
                        help='Output file path.',
                        type=str)
    PARSER.add_argument('--random_costs', '-rc',
                        default=0,
                        help='Define random costs for non-adjacent vertices.',
                        type=int)
    PARSER.add_argument('--random_seed', '-rs',
                        default=-1,
                        help='Define a seed. Use -1 to not use a seed. Only pass integers.',
                        type=int)
    PARSER.add_argument('--const_cost', '-cc',
                        default=0,
                        help='Define a const. cost for non-adjacent vertices.',
                        type=int)
    PARSER.add_argument('--prod_cost', '-pc',
                        default=0,
                        help='Define the cost for non-adjacent vertices as the product of their indices.',
                        type=int)
    PARSER.add_argument('--max_vertices', '-mv',
                        default=-1,
                        help='Max. no. of non-adjacent vertices with costs.',
                        type=int)
    PARSER.add_argument('--max_cost', '-mc',
                        default=10,
                        help='Max. cost for non-adjacent vertices.',
                        type=int)

    ARGS = PARSER.parse_args()

    MAX_VERTEX, EDGES = extract_info(ARGS.input)
    COSTS_TO_WRITE = get_costs(MAX_VERTEX, EDGES,
                               rand=ARGS.random_costs,
                               seed=ARGS.random_seed,
                               const_cost=ARGS.const_cost,
                               prod_cost=ARGS.prod_cost,
                               max_vertices=ARGS.max_vertices,
                               max_cost=ARGS.max_cost)
    write_result(ARGS.output, MAX_VERTEX, EDGES, COSTS_TO_WRITE)
