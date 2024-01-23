import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import pickle as pkl


G = pkl.load(open('network.pkl', 'rb'))
movie_nodes = pkl.load(open('map.pkl', 'rb'))
text_out = open('summary.txt', 'w')

H = G.copy()
circle_refs = nx.selfloop_edges(G)
H.remove_edges_from(circle_refs)

H2 = nx.Graph(H)
for n in H2.nodes():
    edges_H2 = nx.edges(H2,n)
    if len(edges_H2) == 0:
        H.remove_edges_from(edges_H2)
        H.remove_node(n)
    elif len(edges_H2) < 2:
        connected_edges=list(list(edges_H2)[0])
        connected_edges.remove(n)
        if len(nx.edges(H2,connected_edges[0])) < 2:
            H.remove_edges_from(edges_H2)
            H.remove_node(n)
nt = Network('1000px', '1000px', directed=True)
nt.from_nx(H)
nt.show('movies_in_movies_nolabel.html')


final_net = nx.Graph()
nodes = {y: x for x, y in movie_nodes.items()}
long = nx.dag_longest_path(H)

labels = {}
while len(long) > 2:
    final_net.add_nodes_from(long)
    edges = []
    for n in long:
        out_string = nodes[n]
        if n != long[-1]:
            out_string += '->'
        text_out.write(out_string)
        labels[n] = nodes[n]
        edges += nx.edges(H, n)
    text_out.write('\n')

    for p1, p2 in edges:
        if p1 not in labels.keys():
            final_net.add_node(p1, label=nodes[p1])
            labels[p1] = nodes[p1]
        # else:
            # final_net.nodes[p1]['label'] = nodes[p1]
        if p2 not in labels.keys():
            final_net.add_node(p2, label=nodes[p2])
            labels[p2] = nodes[p2]
        # else:
            # final_net.nodes[p2]['label'] = nodes[p2]
    final_net.add_edges_from(edges)
    # H.remove_nodes_from(long)
    H.remove_edges_from(zip(long[:-1], long[1:]))
    long = nx.dag_longest_path(H)

# nx.draw_networkx(final_net, labels=labels, arrows=True,
#                  node_shape= 's', node_color = 'white', font_size=4, arrowsize=2)
nt = Network('500px', '500px')
nt.from_nx(final_net)
nt.show('nx.html')
# plt.title('Movies in Movies')
# plt.savefig('movies_in_movies.jpeg', dpi = 300)