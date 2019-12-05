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
        G.edges[u,v]['weight'] = random.uniform(0.,100.)
    return G


def find_path(G, s, t):
    queue = []
    queue.append(s)

    for k in queue:
        for el in list(G.neighbors(queue[-1])):
            if not (el in queue):
                queue.append(el)
                if el == t:
                    return queue

    return queue


def find_min_st_cut(G):
    while true:
        #path = find_path(G,)
        break

    return 0


def build_gomory_hu_tree(G):
    T = nx.Graph() # Результирующее дерево
    T.add_node(tuple(G.nodes())) # На первом шаге у Т только 1 вершина
    while True:
        # Шаг 2 - выбор группы вершин из V(t) в которой больше 1 вершины
        # Если все группы по одной вершине - дерево готово
        X = ()
        for n in tuple(T.nodes()):
            if len(n) >= 2:
                X = tuple(n)
        if not X:
            break





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
