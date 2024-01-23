import networkx as nx
import numpy as np
import csv
import matplotlib.pyplot as plt
import pickle as pkl
import PIL

class MovieNode:
    connections = []
    def __init__(self, name):
        self.name = name

    def connect(self, node2):
        self.connections.append(node2)


def build_graph(reader):
    movie_nodes = {} # {movie name: ind value}
    movie_map = []  # list of tuples that map movie indices to one another
    indcount = 0
    for row in reader:
        base = row[0]
        nested = row[1]
        if base in movie_nodes.keys():
            ind1 = movie_nodes[base]
        else:
            ind1 = indcount
            movie_nodes[base] = ind1
            indcount += 1

        if nested in movie_nodes.keys():
            ind2 = movie_nodes[nested]
        else:
            ind2 = indcount
            movie_nodes[nested] = ind2
            indcount += 1

        movie_map.append((ind1, ind2))

    return movie_nodes, movie_map






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fn = 'movies_in_movies.csv'
    f = open(fn)
    pklfile = 'network.pkl'
    node_name_pkl = 'map.pkl'
    redo_graph = True

    if redo_graph:
        reader = csv.reader(f)
        movie_nodes, movie_map = build_graph(reader)
        pkl.dump(movie_nodes, open(node_name_pkl, 'wb'))
        labels = {y: x for x, y in movie_nodes.items()}

        G = nx.DiGraph()
        G.add_nodes_from(list(movie_nodes.values()))
        G.add_edges_from(movie_map)
        for node in G.nodes():
            G.nodes[node]['title'] = labels[node]
            try:
                img = PIL.Image.open('images/'+labels[node])
                G.nodes[node]['image'] = 'images/'+labels[node]
                G.nodes[node]['shape'] = 'image'
            except:
                continue

        pkl.dump(G, open(pklfile, 'wb'))
    else:
        G = pkl.load(open(pklfile,'rb'))

    # poses = nx.drawing.kamada_kawai_layout(G)


    # nx.draw_networkx(G, labels=labels, arrows=True,
    #                  node_shape= 's', node_color = 'white', font_size=2, arrowsize=1)
    # plt.title('Movies in Movies.')
    # plt.savefig('movies_in_movies.jpeg', dpi = 300)
    # plt.show()




    # G = nx.DiGraph()
    # nodes = np.arange(0, 8).tolist()
    # G.add_nodes_from(nodes)
    # G.add_edges_from([(0, 1), (0, 2),
    #                   (1, 3), (1, 4),
    #                   (2, 5), (2, 6), (2, 7)])
    # pos = {0: (10, 10),
    #        1: (7.5, 7.5), 2: (12.5, 7.5),
    #        3: (6, 6), 4: (9, 6),
    #        5: (11, 6), 6: (14, 6), 7: (17, 6)}
    # labels = {0:'CEO', 1:'Team A Lead', 2: 'Team B Lead', 3: 'Staff A', 4: 'Staff B', 5: 'Staff C',
    #           6: 'Staff D', 7: 'Staff E'}
    # nx.draw_networkx(G, pos=pos, labels=labels, arrows=True,
    #                  node_shape= 's', node_color = 'white')
    # plt.title('Organogram of a company.')
    # plt.savefig('test_networkx.jpeg', dpi = 300)
    # plt.show()