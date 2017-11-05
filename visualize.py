import pickle

from features import VISUALIZATION_PLOTTING
from graph import NodeState
from logging import getLogger

if VISUALIZATION_PLOTTING:
    import matplotlib.pyplot as plt
    import networkx as nx

logger = getLogger("visualization")


def on_key(event, args):
    if event.key == 'right':
        draw_next_step(args)

    elif event.key == 'left':
        draw_previous_step(args)

    elif event.key == 'q':
        exit(0)


def draw_graph(graph, untouched_nodes, burning_nodes, defended_nodes, edges, positions, labels, solution):
    node_size = 300
    labels_font_size = 12

    untouched_nodes_color = 'gray'
    defended_nodes_color = 'blue'
    burning_nodes_color = 'red'

    plt.clf()
    plt.axis('off')
    plt.title('Solution: ' + str(solution))

    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=burning_nodes,
                           node_size=node_size,
                           node_color=burning_nodes_color)
    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=defended_nodes,
                           node_size=node_size,
                           node_color=defended_nodes_color)
    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=untouched_nodes,
                           node_size=node_size,
                           node_color=untouched_nodes_color)

    nx.draw_networkx_edges(graph, pos=positions, edgelist=edges)
    nx.draw_networkx_labels(graph, pos=positions, labels=labels, font_size=labels_font_size)

    plt.show()


def draw_next_step(args):
    logger.info("Drawing next step...")

    future_transitions = args['future_transitions']
    shown_transitions = args['shown_transitions']

    if future_transitions:

        step = future_transitions.keys()[0]
        transition = future_transitions.pop(step)
        shown_transitions[step] = transition

        for node_id, state in transition:
            if state == NodeState.BURNING:
                args['burning_nodes'].append(node_id)
                args['untouched_nodes'].remove(node_id)
            elif state == NodeState.DEFENDED:
                args['defended_nodes'].append(node_id)
                args['untouched_nodes'].remove(node_id)

        draw_graph(args['graph'], args['untouched_nodes'], args['burning_nodes'], args['defended_nodes'], args['edges'],
                   args['positions'], args['labels'], args['solution'])


def draw_previous_step(args):
    logger.info("Falling back to previous step...")

    future_transitions = args['future_transitions']
    shown_transitions = args['shown_transitions']

    if shown_transitions:

        step = shown_transitions.keys()[-1]
        transition = shown_transitions.pop(step)
        future_transitions[step] = transition

        for node_id, state in transition:
            if state == NodeState.BURNING:
                args['burning_nodes'].remove(node_id)
                args['untouched_nodes'].append(node_id)
            elif state == NodeState.DEFENDED:
                args['defended_nodes'].remove(node_id)
                args['untouched_nodes'].append(node_id)

        draw_graph(args['graph'], args['untouched_nodes'], args['burning_nodes'], args['defended_nodes'], args['edges'],
                   args['positions'], args['labels'], args['solution'])


def visualize_simulation(graph, transitions, solution):
    nx_graph = nx.Graph()

    nodes = graph.get_nodes()
    edges = graph.get_edges()

    nx_graph.add_nodes_from(nodes)
    nx_graph.add_edges_from(edges)

    positions = nx.spring_layout(nx_graph)

    labels = dict()
    for node_id in nodes:
        labels[node_id] = node_id

    shown_transitions = dict()

    untouched_nodes = list(nodes)
    burning_nodes = list()
    defended_nodes = list()

    args = {
        'graph': nx_graph,
        'edges': edges,
        'positions': positions,
        'future_transitions': transitions,
        'shown_transitions': shown_transitions,
        'untouched_nodes': untouched_nodes,
        'burning_nodes': burning_nodes,
        'defended_nodes': defended_nodes,
        'labels': labels,
        'solution': solution,
    }

    plt.gcf().canvas.mpl_connect('key_press_event', lambda event: on_key(event, args))
    draw_graph(nx_graph, nodes, None, None, edges, positions, labels, solution)


def save_solution(solution, iteration_no, path):
    obj = (solution, iteration_no)
    pickle.dump(obj, open(path, "wb"), pickle.HIGHEST_PROTOCOL)


def load_solution(path):
    return pickle.load(open(path))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-sf', '--solution_file',
                        required=True,
                        help='file containing solution')
    parser.add_argument('-in', '--input_file',
                        required=True,
                        help='file containing graph')
    parser.add_argument('-f', '--ffs',
                        required=True,
                        help='number of firefighters per step',
                        type=int)
    args = parser.parse_args()

    # sf = "/home/piotr/Projects/SAO/results/150_tree_10000/sl/100_roulette_multi_injection_single_swap_best_then_random_tree_10000_4.csv.sl"
    # solution, iteration_no = load_solution(sf)
    solution, iteration_no = load_solution(args.solution_file)

    import simulation
    from graph import Graph

    g = Graph.from_file(args.input_file)
    transitions, score = simulation.simulation(g, solution, args.ffs)
    print "Score: {}, found in {} iteration".format(str(score), iteration_no)
    visualize_simulation(g, transitions, solution)
