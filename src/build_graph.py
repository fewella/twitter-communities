import os

import networkx as nx
import matplotlib.pyplot as plt

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

data_dir = "../data/"
names_file = data_dir + "names.txt"
followers_dir = data_dir + "politicians_data/"

degree_threshold = 0.13


def read_political_parties(filename):
    parties = {}
    f = open(filename, "r")
    for line in f:
        username, party = line.split()
        parties[username] = party
    f.close()
    return parties


def get_followers_from_file(filename):
    f = open(filename, "r")
    followers = set([line.rstrip() for line in f])
    f.close()
    return followers


def get_names_from_file(filename):
    f = open(filename, "r")
    names = {}
    for line in f:
        items = line.split()
        names[items[0]] = "".join(items[1:])
    f.close()
    return names


def similarity_degree(u1_followers, u2_followers):
    intersect = u1_followers & u2_followers
    degree = 0
    if len(u1_followers) < len(u2_followers):
        degree = len(intersect) / len(u1_followers)
    else:
        degree = len(intersect) / len(u2_followers)
    return degree


def host_interactive_graph(G, pos, parties):
    app = dash.Dash(__name__)

    width = 1400
    height = 1000

    graph_elements = []
    for n in G.nodes:
        x = int((width / 2) * (pos[n][0] + 1))
        y = int((height / 2) * (pos[n][1] + 1))
        if n in parties:
            p = parties[n]
        else:
            p = ''
        
        graph_elements.append({
            'data': {'id': n, 'label': n}, 
            'position': {'x': x, 'y': y},
            'classes': p
        })
    
    for e in G.edges:
        if e[0] != e[1]:
            graph_elements.append({
                'data': {'source': e[0], 'target': e[1]},
            })

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            elements = graph_elements,
            layout = {'name': 'preset'},
            style = {'width': str(width) + 'px', 'height': str(height) + 'px'},
            stylesheet = [{
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                }
            }, {
                'selector': '.rep',
                'style': {
                    'background-color': '#FF0000'
                }
            }, {
                'selector': '.dem',
                'style': {
                    'background-color': '#0015BC'
                }
            }]
        )
    ])

    app.run_server(debug=True)


def main():
    labels = get_names_from_file(names_file)
    follower_ids = {}
    usernames = []
    for filename in os.listdir(followers_dir):
        username = filename.rstrip(".txt")
        follower_ids[username] = get_followers_from_file(followers_dir + filename)
        usernames.append(username)

    G = nx.Graph()
    G.add_nodes_from(usernames)
    for user1 in usernames:
        for user2 in usernames:
            if similarity_degree(follower_ids[user1], follower_ids[user2]) >= degree_threshold:
                if not G.has_edge(user1, user2):
                    G.add_edge(user1, user2)
    
    parties = read_political_parties(data_dir + "political_parties.txt")
    graph_pos = nx.spring_layout(G, k=0.3, iterations=30)
    host_interactive_graph(G, graph_pos, parties)


if __name__ == "__main__":
    main()
