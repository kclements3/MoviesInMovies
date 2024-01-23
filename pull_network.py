import imdb
import networkx as nx
from pyvis.network import Network
import pickle as pkl
import os


# 1. Select features/featured in connections from movie.
# 2. Form connections with these in network and mark middle as populated
# 3. Do bfs on each connection node. repeat 1 and 2 except if marked as populated

def select_connections(title, conn_list, omit_file):

    out = []
    for conn in conn_list:
        if (conn['kind'] == 'movie' or conn['kind'] == 'tv movie') and 'award' not in conn['title'].lower():
            conn_info = ia.get_movie(conn.movieID)
            excluded = {'Talk-Show', 'Documentary', 'Reality-TV', 'Biography'}
            excluded_keywords = {'mash-up', 'clip-show', 'recycling-movies', 'clips', 'halloween-special', 'music-video'}
            if 'keywords' not in conn.keys():
                ia.update(conn, info='keywords')
            if 'keywords' not in conn.keys():
                conn['keywords'] = []

            if 'genres' in conn_info.keys() and len(excluded.intersection(set(conn_info['genres']))) == 0\
                    and len(excluded_keywords.intersection(set(conn['keywords']))) == 0:
                out.append(conn)
            else:
                out_str = 'Omitting ' + conn['title'] + ' from ' + title
                omit_file.write(out_str + '\n')
        else:
            out_str = 'Omitting ' + conn['title'] + ' from ' + title
            omit_file.write(out_str + '\n')
    return out

def populate_network(movie, q):
    print('Populating '+movie['title'])
    if movie.movieID not in selected_conns.keys():
        selected_conns.setdefault(movie.movieID, {})
        connections = ia.get_movie(movie.movieID)
        ia.update(connections, info='connections')
        ia.update(connections, info='keywords')
        if 'keywords' not in connections.keys():
            connections['keywords'] = []
        if 'features' in connections['connections'].keys():
            selected_conns[movie.movieID].setdefault('features', [])
            features = select_connections(movie['title'], connections['connections']['features'], fn)
            selected_conns[movie.movieID]['features'] = features
            pkl.dump(selected_conns, open('selected_connections.pkl', 'wb'))
        if 'featured in' in connections['connections'].keys():
            selected_conns[movie.movieID].setdefault('featured in', [])
            featured_in = select_connections(movie['title'], connections['connections']['featured in'], fn)
            selected_conns[movie.movieID]['featured in'] = featured_in
            pkl.dump(selected_conns, open('selected_connections.pkl', 'wb'))

    if 'features' in selected_conns[movie.movieID].keys():
        features = selected_conns[movie.movieID]['features']
    else:
        features = []


    if 'featured in' in selected_conns[movie.movieID].keys():
        featured_in = selected_conns[movie.movieID]['featured in']
    else:
        featured_in = []
    print('selected connections')

    out_queue = []
    ids = [ms.movieID for ms in q]
    for fin in featured_in:
        if fin.movieID != movie.movieID:
            if fin.movieID not in imdb_net.nodes():
                imdb_net.add_node(fin.movieID, title=fin['long imdb title'], label=fin['long imdb title'])
                # imdb_net.nodes[fin.movieID]['populated'] = False
            if (fin.movieID, movie.movieID) not in imdb_net.edges():
                imdb_net.add_edge(fin.movieID, movie.movieID)

            if 'populated' not in imdb_net.nodes[fin.movieID].keys() and fin.movieID not in ids:
                out_queue.append(fin)
            # populate_network(fin)

    for fs in features:
        fID = fs.movieID
        if fID != movie.movieID:
            if fID not in imdb_net.nodes():
                imdb_net.add_node(fID, title=fs['long imdb title'], label=fs['long imdb title'])
            if (movie.movieID, fID) not in imdb_net.edges():
                imdb_net.add_edge(movie.movieID, fID)
            if 'populated' not in imdb_net.nodes[fID].keys() and fID not in ids:
                out_queue.append(fs)
            # populate_network(fs)
    imdb_net.nodes[movie.movieID]['populated'] = True
    return out_queue



if __name__ == '__main__':
    ia = imdb.Cinemagoer()
    top250 = ia.get_top250_movies()
    fn = open('omissions.txt', 'w')
    # Create dict of {id: title
    imdb_net = nx.DiGraph()
    if 'selected_connections.pkl' in os.listdir():
        selected_conns = pkl.load(open('selected_connections.pkl', 'rb'))
    else:
        selected_conns = {}

    q = []
    home_alone = [ia.get_movie('099785')]
    starting = [ia.get_movie('0096895')]
    for m in starting:
        # connections = ia.get_movie(m.movieID)
        # if 'features' in connections['connections'].keys():
        #     features = select_connections(m['title'], connections['connections']['features'], fn)
        # else:
        #     features = []
        #
        # if 'featured in' in connections['connections'].keys():
        #     featured_in = select_connections(m['title'], connections['connections']['featured in'], fn)
        # else:
        #     featured_in = []

        # populate_network(m, features, featured_in)
        imdb_net.add_node(m.movieID, title=m['long imdb title'], label=m['long imdb title'])

        out_queue = populate_network(m, q)
        q += out_queue
        while len(q) > 0:
            print('Added {}, {} remaining'.format(len(out_queue), len(q)))
            out_queue = populate_network(q.pop(0), q)
            q += out_queue
            pkl.dump(imdb_net, open('imdb_net.pkl', 'wb'))

    pkl.dump(imdb_net, open('imdb_net.pkl', 'wb'))
    nt = Network('1000px', '1000px', directed=True)
    nt.repulsion()
    nt.from_nx(imdb_net)
    nt.show('IMBD_top250.html')

