# twitter-communities

This is a tool to visualize communities on Twitter. 

fetch_data.py takes a list of "high-profile" Twitter accounts, and uses Twitter's API to find their account, and store a sample of their followers' ids locally.
build_graph.py builds a graph of communities, where nodes are "high-profile" Twitter accounts, and edges suggest that two accounts are closely connected. 
  In order to determine connectedness, the build_graph.py looks at the locally stored sets of followers, and compares them to determine if two given sets of followers ave a high overlap.
