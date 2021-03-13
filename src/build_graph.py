import os

import networkx as nx
import matplotlib.pyplot as plt

data_directory = "../data/follower_data/"
degree_threshold = 0.10


def get_followers_from_file(filename):
    f = open(filename, "r")
    followers = set([line.rstrip() for line in f])
    f.close()
    return followers


def similarity_degree(u1_followers, u2_followers):
    intersect = u1_followers & u2_followers
    degree = 0
    if len(u1_followers) < len(u2_followers):
        degree = len(intersect) / len(u1_followers)
    else:
        degree = len(intersect) / len(u2_followers)
    return degree


def main():
    follower_ids = {}
    usernames = []
    for filename in os.listdir(data_directory):
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
    nx.draw_networkx_labels(G, graph_pos)

    plt.savefig("graph.png")


if __name__ == "__main__":
    main()
