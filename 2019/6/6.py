import os
import requests
import requests_cache
import networkx as nx
import matplotlib.pyplot as plt

def part1(lines):
    return nx.transitive_closure(create_graph(lines)).size()

def part2(lines):
    return nx.shortest_path_length(create_graph(lines).to_undirected(), "YOU", "SAN") - 2

def create_graph(lines):
    return nx.read_edgelist(lines, delimiter=")", create_using=nx.DiGraph)

def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))

    # Visualisation of graph - not part of AoC question
    graph = create_graph(lines)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, cmap=plt.get_cmap('jet'), node_size=30)
    nx.draw_networkx_labels(graph, pos, font_size=6)
    nx.draw_networkx_edges(graph, pos, edge_color='r', arrows=True)
    nx.draw_networkx_edges(graph, pos,  arrows=False)
    plt.show()

if __name__ == "__main__":
    main()
