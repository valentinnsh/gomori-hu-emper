import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def show_tree(G, filename):
    pos =graphviz_layout(G, prog='dot')
    nx.draw(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(filename)
    plt.cla()


# Генерирует случайный взвешенный граф с n вершинами
def generate_random_weighted_graph(n,m):
    G = nx.gnm_random_graph(n,m)
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = random.randint(0,10)
    return G


def main():

    G = generate_random_weighted_graph(7,5)


    T = nx.Graph()
    T.add_node(1)
    T.add_node(2)
    T.add_node(3)

    T.add_edge(1,2,weight = 0.3)
    T.add_edge(1,3,weight = 0.4)

    show_tree(T, 'tree.png')
    show_tree(G, "graph.png")

if __name__ == "__main__":
    main()
