# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Instance Generator

    Generates a problem instance for the robust coloring problem.

    Author: Abdul Rahman Dabbour
    Affiliation: CogRobo Lab, FENS, Sabanci University
    License: GNU General Public License v3.0
    Repository: https://github.com/ardabbour/grmmo/
"""

import argparse
import itertools
import random


def get_costs(max_vertex, edges, rand, seed, const_cost, max_vertices, max_cost):
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
    else:
        assert const_cost > 0
        if max_vertices > 0:
            non_adjacent_pairs = non_adjacent_pairs[:max_vertices]
            for pair in non_adjacent_pairs:
                costs_to_write.append('cost({},{},{}).\n'.format(
                    pair[0], pair[1], const_cost))

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


def write_result(output_path, max_vertex, edges, costs_to_write):
    """Dumps all the information (graph description + costs) to a file."""

    edges_to_write = ['edge({},{}).\n'.format(x, y) for (x, y) in edges]
    with open(output_path, 'w') as f:
        f.write('% Graph description\n')
        f.write('vertex(1..{}).\n'.format(max_vertex))
        f.writelines(edges_to_write)
        f.write('\n')
        f.write('% Define costs\n')
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
                        default=1,
                        help='Define random costs for non-adjacent vertices.',
                        type=int)
    PARSER.add_argument('--random_seed', '-rs',
                        default=-1,
                        help='Define a seed. Use -1 to not use a seed. Only pass integers.',
                        type=int)
    PARSER.add_argument('--const_cost', '-c',
                        default=0,
                        help='Define a const. cost for non-adjacent vertices.',
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
                               max_vertices=ARGS.max_vertices,
                               max_cost=ARGS.max_cost)
    write_result(ARGS.output, MAX_VERTEX, EDGES, COSTS_TO_WRITE)
