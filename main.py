import networkx as nx
import community
import numpy as np
import pandas as pd
import operator
import collections
import math
import matplotlib.pyplot as plt

def show_nodes(graph):
    plt.figure(figsize = (10,9))
    nx.draw_networkx(graph, with_labels=False, node_size=10, node_color='g', edge_color='r')
    plt.axis('off')
    plt.show()

#first compute the best partition
# df = pd.read_pickle('full_df.pkl')
df = pd.read_pickle('half_df.pkl')
G = nx.from_pandas_edgelist(df, source='src', target='dst')


print 'trimming off nodes with degree 1...'
to_remove = [n for n, d in G.degree() if d == 1]
# print "Degree sequence", degree_sequence
for n in to_remove:
    G.remove_node(n)

print 'computing partitions...'
# sorted_ptt = sorted([com for n, com in partition], reverse=True)  # degree sequence
partition = community.best_partition(G)
print 'modularity', community.modularity(partition, G)

print 'computing metrics'

comMemberCount = collections.Counter(partition.values())

# computing separability
# ratio of num edges within community / num edges to rest of network
# comms = comMemberCount.most_common(5)
# for comm in comms:
#     comm_nodes = [nodes for nodes in partition.keys() if partition[nodes] == comm[0]]
#     n = len(comm_nodes)
#     print 'community number', comm[0], 'size', n

#     # separability
#     internal, external = 0, 0
#     for src, dst in nx.edges(G, comm_nodes):
#         if partition[src] == comm[0] and partition[dst] == comm[0]:
#             internal += 1.
#         else: # one of the node is not from the community meaning it is a global bridge
#             external += 1.

#     print 'separability', internal/external

#     # density, internal / all possible nodes
#     max_edges = n*(n-1)/2
#     print 'density', internal/max_edges

    


# drawing

# print comMemberCount
# fig, axs = plt.subplots(2, 2)
# for com in comMemberCount.most_common(4):
#     list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com[0]]
#     k = G.subgraph(list_nodes)
#     pos = nx.spring_layout(k)

#     nx.draw_networkx(k, pos, node_size=5, with_labels=False)
# plt.show()
#drawing
size = 10
# pos = nx.spring_layout(G)
count = 0.

# # for com in set(partition.values()):
all_nodes = []
for com in comMemberCount.most_common(4):
    all_nodes = all_nodes + [nodes for nodes in partition.keys() if partition[nodes] == com[0]]

subG = G.subgraph(all_nodes)
pos = nx.spring_layout(subG)
plt.axis('off')

for com in comMemberCount.most_common(4):
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com[0]]
    # k = subG.subgraph(list_nodes)
    # nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 5, node_color = str(count / size))
    nx.draw_networkx_nodes(subG, pos, nodelist=list_nodes, node_size=5, node_color=str(count / size), with_labels=False)

nx.draw_networkx_edges(subG, pos, alpha=0.3)

plt.show()

# CG = nx.make_max_clique_graph(G)
# node_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)


# node with highest degree: ILGI5CILN3M

# cli = nx.algorithms.clique.cliques_containing_node(G, nodes='ILGI5CILN3M')
# max_cli = nx.algorithms.clique.node_clique_number(G, nodes='ILGI5CILN3M')
# print (cli)

# cliques_with_len = [(len(clique), clique) for clique in cli]
# res = sorted(cliques_with_len, key=lambda x: x[0], reverse=True)

# max_cli

# get the highest degree nodes
# get the cliques these nodes belong too
# get the cliques with the highest number of nodes in it
# get the nodes of these cliques
# get the clusters these nodes belong too