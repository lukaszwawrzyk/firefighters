#!/usr/bin/env python

import argparse
import os
import random
from collections import Counter
from itertools import combinations

from graph import Graph


def generate_edges(vertices_num, density):
    """
    :param vertices_num: number of graph vertices to be generated
    :param density: float in [0..1] where 0 - no edges at all, 1 - clique
    """
    max_edges = (vertices_num * (vertices_num - 1)) / 2
    edges_num = int(max_edges * density)

    all_possible_edges = combinations(xrange(vertices_num), 2)

    edges = random.sample(list(all_possible_edges), edges_num)
    return edges_num, edges


def generate_tree_edges(child_probability=0.7, max_nodes=150):
    tree_size = 0
    root = 0
    current_node = 0
    edges = list()

    stack = [root]
    while stack:
        node = stack.pop(0)
        # try to generate two childs
        for _ in (0, 1):
            if random.random() < child_probability and current_node < max_nodes:
                tree_size += 1
                current_node += 1
                child = current_node
                stack.append(child)
                edges.append((node, child))

    return tree_size, current_node + 1, edges


def generate_file_data(out_file, vertices_num, density, starting_vertices_num, tree=False):
    if tree:
        # in case of tree vertices_num is maximum number of vertices
        edges_num, vertices_num, edges = generate_tree_edges(child_probability=density, max_nodes=vertices_num)
    else:

        if density < 2 * (float(vertices_num - 1) / (vertices_num * (vertices_num - 1))):
            raise ValueError("Density too low, cannot generate connected graph")

        edges_num, edges = generate_edges(vertices_num, density)

        # make graph connected by connecting unconnected nodes to graph
        # and removing edges that will not make graph unconnected again
        # each time we remove an edge we have to check the conditions again
        while True:
            nodes_degree = Counter()
            for v_start, v_end in edges:
                nodes_degree[v_start] += 1
                nodes_degree[v_end] += 1

            unconnected_nodes = set([node for node in xrange(vertices_num) if node not in nodes_degree])

            if not unconnected_nodes:
                break

            # add an edge from unconnected node to a random node
            edges.append((unconnected_nodes.pop(), random.randint(0, vertices_num - 1)))

            # find each edge which removal will not make graph unconnected
            redundant_edges = set()
            for v_start, v_end in edges:
                if nodes_degree[v_start] >= 2 and nodes_degree[v_end] >= 2:
                    redundant_edges.add((v_start, v_end))

            # remove one redundant edge
            edges.remove(redundant_edges.pop())

    starting_vertices = random.sample(xrange(vertices_num), starting_vertices_num)

    with open(out_file, 'w') as f:
        f.write("{} {}\n".format(vertices_num, edges_num))
        for sv in starting_vertices:
            f.write("{} ".format(sv))
        f.write('\n')
        for e in edges:
            f.write("{} {}\n".format(*e))


def _get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def _generate_graph_file_name(vertex_no, density, starting_vertices_no):
    return u"{}_{}_{}.rgraph".format(vertex_no, density, starting_vertices_no)


def load_graph(vertex_no, density, starting_vertices_no=1):
    graphs_dir = "graphs/"
    fname = _generate_graph_file_name(vertex_no, density, starting_vertices_no)
    graph_file_path = os.path.join(_get_script_dir(), graphs_dir, fname)

    if not os.path.isfile(graph_file_path):
        generate_file_data(graph_file_path, vertex_no, density, starting_vertices_no)

    graph = Graph.from_file(graph_file_path)

    return graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vertices', help='number of vertices in graph', type=int, default=10)
    parser.add_argument('-d', '--density', help='edges density; float in range [0..1]', type=float, default=0.2)
    parser.add_argument('-s', '--starting_vertices', help='number of starting vertices', type=int, default=1)
    parser.add_argument('--out', help='output file', default=os.path.join('graphs', 'random.txt'))
    args = parser.parse_args()

    generate_file_data(out_file=args.out,
                       vertices_num=args.vertices,
                       density=args.density,
                       starting_vertices_num=args.starting_vertices)
