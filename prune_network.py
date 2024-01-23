import pickle as pkl
import imdb


selected_conns = pkl.load(open('selected_connections.pkl', 'rb'))
conns_orig = selected_conns.copy()
ia = imdb.Cinemagoer()
excluded_keywords = {'mash-up', 'archive-footage', 'clip-show', 'clips', 'halloween-special', 'music-video'}
for id, conns in selected_conns.items():
    for f, val in conns.items():
        out_list = []
        for v in val:
            print('Selecting ', v['title'])
            if 'keywords' not in v.keys():
                ia.update(v, 'keywords')
            if 'keywords' not in v.keys():
                v['keywords'] = []

            if 'award' in v['title'].lower() or 'anniversary' in v['title'].lower():
                ii = input('Include {}? (y/n)'.format(v['title']))
            elif 'final cut' in v['title'].lower() or 'paramount presents' in v['title'].lower():
                ii = input('Include {}? (y/n)'.format(v['title']))
            elif 'tv moments' in v['title'].lower() or 'tv special' in v['title'].lower():
                ii = input('Include {}? (y/n)'.format(v['title']))
            elif 'hollywood burn' in v['title'].lower() or 'dtv monster hits' in v['title'].lower():
                ii = input('Include {}? (y/n)'.format(v['title']))
            # elif len(excluded_keywords.intersection(set(v['keywords']))) != 0:
            #     ii = input('Include {}? (y/n)'.format(v['title']))
            elif 'Celluloid Bloodbath: More Prevues from Hell' in v['title'] or 'The Dirties' in v['title']:
                ii = input('Include {}? (y/n)'.format(v['title']))
            elif 'The Untitled Star Wars Mockumentary' in v['title'] or 'bollywood' in v['title'].lower():
                ii = 'n'
            else:
                ii = 'y'

            if ii == 'y':
                out_list.append(v)
        conns[f] = out_list

pkl.dump(selected_conns, open('selected_connections.pkl', 'wb'))
