import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from sys import maxsize as maxint
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from networkx.algorithms.connectivity import minimum_st_edge_cut

def show_tree(G, filename):
    pos =graphviz_layout(G, prog='dot')
    nx.draw(G,pos,with_labels = True)
    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(filename)
    plt.show()
    plt.cla()


# Генерирует случайный взвешенный граф с n вершинами
def generate_random_weighted_graph(n,m):
    G = nx.gnm_random_graph(n,m)
    for (u, v) in G.edges():
        G.edges[u,v]['capacity'] = random.randint(1,17)
    return G


def find_min_st_cut(G,s,t):
    cut_value, partition = nx.minimum_cut(G, s, t)
    reachable, non_reachable = partition
    cutset = set()
    for u, nbrs in ((n, G[n]) for n in reachable):
        cutset.update((u, v) for v in nbrs if v in non_reachable)

    return cut_value, cutset


def find_connected_component(G, s,t):
    G1 = G.copy()
    G1.remove_edge(s,t)
    #print('edges-----------------', list(G1.edges()))
    queue = []
    queue.append(s)
    for k in queue:
        for el in list(G1.neighbors(queue[-1])):
            if not (el in queue):
                queue.append(el)
                if el == t:
                    #print("que---------", queue)

                    return queue

    #print("que---------", queue)
    return queue


def build_gomory_hu_tree(G0):
    T = nx.Graph() # Результирующее дерево
    T.add_node(tuple(G0.nodes())) # На первом шаге у Т только 1 вершина
    while True:
        # Шаг 2 - выбор группы вершин из V(t) в которой больше 1 вершины
        # Если все группы по одной вершине - дерево готово
        X = ()
        for n in T.nodes():
            if len(n) >= 2:
                X = tuple(n)
        if not X:
            break

        # Шаг 3 - конструируем вспомогательный граф G'
        G = nx.Graph()
        # Сначала добавляем Х целиком
        for i in X:
            G.add_node(tuple([X[i]]))
        T.add_node(tuple([99])); T.add_node(tuple([777]))
        T.add_edge(X,tuple([99]), capacity = 1); T.add_edge(tuple([777]),tuple([99]), capacity = 2);
        show_tree(G,'test.png')
        # Потом добвляем сгруппированные сеты вершин компонент связности T\X
        for i in T.neighbors(X):
            G.add_node(tuple(find_connected_component(T,i,X)))
        show_tree(G,'test.png')


        for u in X:
            for v in X:
                if G0.has_edge(u,v):
                    G.add_edge(tuple([u]),tuple([v]), capacity = G0.edges[u,v]['capacity'])
        show_tree(G,'test.png')
        # фиксануть веса ребер в G
        for n in G.nodes():
            if n != X:

                for u in X:
                    total_cap = 0
                    for v in n:
                        if G0.has_edge(u,v):
                            total_cap += G0.edges[u,v]['capacity']
                    if total_cap:
                        G.add_edge(X,n)
                        G.edges[X,n]['capacity'] = total_cap

        print(list(G.nodes))


        # Шаг 4

        #cut_value, cutset = find_min_st_cut(G, )

def main():

    G = generate_random_weighted_graph(6,10)
    #show_tree(G, "graph.png")
    less = minimum_st_edge_cut(G,0,4)
    node_cut = nx.minimum_node_cut(G,0,4)

    cut_value, cutset = find_min_st_cut(G, 0,4)

    build_gomory_hu_tree(G)
    T = nx.Graph()
    T.add_node(1)
    T.add_node(2)
    T.add_node(3)
    T.add_node(4)

    T.add_edge(1,2,weight = 0.3)
    T.add_edge(1,3,weight = 0.4)
    #show_tree(T, 'tree.png')

if __name__ == "__main__":
    main()
