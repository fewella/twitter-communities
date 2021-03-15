import os

import networkx as nx
import matplotlib.pyplot as plt

data_dir = "../data/"
names_file = data_directory + "names.txt"
followers_dir = data_directory + "politicians_data/"

degree_threshold = 0.10


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


def main():
    read_names_to_labels = True

    labels = get_names_from_file(names_file)
    follower_ids = {}
    usernames = []
    for filename in os.listdir(followers_dir):
        username = filename.rstrip(".txt")
        follower_ids[username] = get_followers_from_file(data_directory + filename)
        usernames.append(username)

    G = nx.Graph()
    G.add_nodes_from(usernames)
    for user1 in usernames:
        for user2 in usernames:
            if similarity_degree(follower_ids[user1], follower_ids[user2]) >= degree_threshold:
                if not G.has_edge(user1, user2):
                    G.add_edge(user1, user2)

    plt.figure(figsize=(18,18))
    
    graph_pos = nx.spring_layout(G, k=0.25, iterations=30)
    nx.draw_networkx_nodes(G, graph_pos)
    nx.draw_networkx_edges(G, graph_pos)
    if read_names_to_labels:
        nx.draw_networkx_labels(G, graph_pos, labels=labels)
    else:
        nx.draw_networkx_labels(G, graph_pos)

    plt.savefig("graph.png")


if __name__ == "__main__":
    main()
