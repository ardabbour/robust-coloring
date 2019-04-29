# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Experiments

    Runs experiments and stores data to a csv file.

    Author: Abdul Rahman Dabbour
    Affiliation: CogRobo Lab, FENS, Sabanci University
    License: GNU General Public License v3.0
    Repository: https://github.com/ardabbour/grmmo/
"""
import argparse
import os
import re
import time
import subprocess
import warnings

import pandas as pd

import instance_generator as ig


def measure_saved_instances():
    """Tests the ASP program on all instances saved under the 'instances'
    folder. Saves results in a csv file titled results_<timestamp>.csv."""

    data = pd.DataFrame(
        columns=['Graph Name', '#Vertices', '#Edges', '#Non-Adjacent Pairs',
                 '#Colors', 'Penalty', 'CPU Time'])
    asp_instances = [os.path.join('instances', f)
                     for f in os.listdir('instances') if f.endswith('.lp')]

    for _, asp_instance in enumerate(asp_instances):

        with open(asp_instance) as f:
            graph_name = re.search('instances/(.+?).lp', asp_instance).group(1)
            edges_count = 0
            non_adjacent_pairs_count = 0
            for line in f.readlines():
                if 'vertex' in line:
                    vertex_count = int(re.findall(r'\d+', line)[-1])
                elif 'edge' in line:
                    edges_count += 1
                elif 'cost' in line:
                    non_adjacent_pairs_count += 1

        start_time = time.time()

        ans = subprocess.run(['clingo',
                              asp_instance,
                              'robustColoring.lp',
                              '--quiet=2,1,2',
                              '--time-limit=2000',
                              '--parallel-mode=20',
                              '--verbose=0'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        time_elapsed = time.time() - start_time
        ans = ans.stdout.decode("utf-8")

        if 'UNSATISFIABLE' not in ans:
            optimization_info = ans.splitlines()[-2]
            optimization_info = optimization_info.split(' ')
            colors_count = int(optimization_info[-2])
            penalty = int(optimization_info[-1])
            results = [str(graph_name), int(vertex_count), int(edges_count),
                       int(non_adjacent_pairs_count), int(colors_count),
                       int(penalty), float(time_elapsed)]
            data = data.append(pd.DataFrame(
                columns=data.columns, data=[results]))
        else:
            warnings.warn('{} could not be solved!'.format(asp_instance))

    data.to_csv('data_{}.csv'.format(time.time()/1000), index=False)


def generate_instances():
    """Generates instances from each graph saved under the 'graphs' folder.
    Saves each instance in the 'instances' folder in an lp file titled
    '<original filename>'.lp."""

    instances = [os.path.join('selection', f)
                 for f in os.listdir('selection') if f.endswith('.col')]

    data = []
    for _, instance in enumerate(instances):
        graph_name = re.search('selection/(.+?).col', instance).group(1)
        color_no_pair = ig.K_VALUES[graph_name]
        max_vertex, edges = ig.extract_info(instance)
        costs_to_write = ig.get_costs(max_vertex, edges, rand=False, seed=None,
                                      max_cost=10, const_cost=False,
                                      prod_cost=True, max_vertices=0)
        data.append([graph_name, max_vertex, len(edges), len(costs_to_write),
                     color_no_pair[0], None, None,
                     color_no_pair[1], None, None])
        for no_of_colors in color_no_pair:
            ig.write_result('instances/{}-k_{}.lp'.format(graph_name, no_of_colors),
                            no_of_colors, max_vertex, edges, costs_to_write)

    columns = ['name', '#vertices', '#edges','#nonedges',
               'k1', 'penalty1', 'time1',
               'k2', 'penalty2', 'time2']
    empty_table = pd.DataFrame(columns=columns,data=data)
    empty_table = empty_table.sort_values('name')
    empty_table.to_csv('empty_table.csv', index=False)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Runs a set of experiments.')
    PARSER.add_argument('mode',
                        help='0: generate and test instances. 1: only generate instances. 2: only test instances',
                        type=int)
    ARGS = PARSER.parse_args()
    if ARGS.mode == 0:
        generate_instances()
        measure_saved_instances()
    elif ARGS.mode == 1:
        generate_instances()
    elif ARGS.mode == 2:
        measure_saved_instances()
