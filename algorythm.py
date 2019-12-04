import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def show_tree(G, filename):
    pos =graphviz_layout(G, prog='dot')
    nx.draw(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(filename)
    plt.show()
    plt.cla()

def main():

    G=nx.Graph()
    i=1

    T = nx.Graph()
    T.add_node(1)
    T.add_node(2)
    T.add_node(3)

    T.add_edge(1,2,weight = 0.3)
    T.add_edge(1,3,weight = 0.4)

    show_tree(T, 'tree.png')

if __name__ == "__main__":
    main()
