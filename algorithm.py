import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from sys import maxsize as maxint
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from networkx.algorithms.connectivity import minimum_st_edge_cut

def check_examples():
    #G = generate_random_weighted_graph(5,13)
    G = nx.Graph()
    gn = [0,1,2,3,4,5]
    G.add_nodes_from(gn)
    G.add_edge(0,1, capacity = 1)
    G.add_edge(0,2, capacity = 7)
    G.add_edge(1,2, capacity = 1)
    G.add_edge(3,1, capacity = 3)
    G.add_edge(4,1, capacity = 2)
    G.add_edge(2,4, capacity = 4)
    G.add_edge(4,3, capacity = 1)
    G.add_edge(4,5, capacity = 2)
    G.add_edge(3,5, capacity = 6)


    # show_tree(G, "graph.png")

    T = build_gomory_hu_tree(G)
    show_tree(T, 'Wiki_example.png', "Example from wikipedia:")



def show_tree(G, filename, title = 'none'):
    pos =graphviz_layout(G, prog='dot')
    nx.draw(G,pos,with_labels = True)
    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(filename)
    plt.title(title)
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
    if G1.has_edge(s,t):
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

    # print("que---------", queue)
    return tuple(queue)


def build_gomory_hu_tree(G0):
    T = nx.Graph() # Результирующее дерево
    new_nodes = []
    for i in G0.nodes():
        new_nodes.append(i)

    T.add_node(tuple(new_nodes)) # На первом шаге у Т только 1 вершина
    while True:
        # Шаг 2 - выбор группы вершин из V(t) в которой больше 1 вершины
        # Если все группы по одной вершине - дерево готово
        X = ()
        for n in T.nodes():
            if len(n) >= 2:
                X = n
        if not X:
            break
        # Шаг 3 - конструируем вспомогательный граф G'
        G = nx.Graph()
        # Сначала добавляем Х целиком
        for i in range(len(X)):
            G.add_node(X[i])

        # Потом добвляем сгруппированные сеты вершин компонент связности T\X
        for i in T.neighbors(X):
            G.add_node(find_connected_component(T,i,X))

        for u in X:
            for v in X:
                if G0.has_edge(u,v):
                    G.add_edge(u,v, capacity = G0.edges[u,v]['capacity'])

        # фиксануть веса ребер в G
        for n in G.nodes():
            if n not in X:
                for u in X:
                    total_cap = 0
                    for v in n:
                        if G0.has_edge(u,v):
                            total_cap += G0.edges[u,v]['capacity']
                        if type(v) == tuple:
                            for k in v:
                                if G0.has_edge(u,k):
                                    total_cap += G0.edges[u,k]['capacity']
                    if total_cap:
                        G.add_edge(u,n)
                        G.edges[u,n]['capacity'] = total_cap



        # Шаг 4 Ищем минимальный st-разрез в G
        # А также строим множества А и В
        s = X[0]; t = X[1]

        cut_value, cutset = find_min_st_cut(G, s, t)
        G1 = G.copy()
        G1.remove_edges_from(list(cutset))
        A = list(find_connected_component(G1,t,s))
        B = list(find_connected_component(G1,s,t))
        for el in A:
            if type(el) == tuple:
                A.remove(el)
                for i in el:
                    A.append(i)

        for el in B:
            if type(el) == tuple:
                B.remove(el)
                for i in el:
                    B.append(i)

        # Шаг 5 перестраиваем дерево T
        ax = tuple(set(A)&set(X))
        bx = tuple(set(B)&set(X))
        T.add_node(ax)
        T.add_node(bx)
        T.add_edge(ax, bx, capacity = cut_value)

        for y in T.neighbors(X) :
            if y in A:
                e1 =(ax, y)
            else:
                e1 =(bx, y)
            w = T.edges[X,y]['capacity']
            T.add_edge(e1[0], e1[1], capacity = w)

        T.remove_node(X)

    # Шаг 6 - наводим красоту
    result = nx.Graph()
    for i in T.nodes():
        result.add_node(i[0])
    for (u,v) in T.edges():
        result.add_edge(u[0], v[0], capacity = T.edges[u,v]['capacity'])

    return result




def main():
    check_examples()
    # G = generate_random_weighted_graph(5,13)


    # show_tree(G, "graph.png")

    # T = build_gomory_hu_tree(G)
    # show_tree(T, 'tree.png')

if __name__ == "__main__":
    main()
