import networkx as nx
import matplotlib.pyplot as plt

G = nx.powerlaw_cluster_graph(20, 1, 0.4)
pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

# print(nx.info(G))
# print([e for e in G.edges])
# print(G.degree(0))


class Node:
    def __init__(self, node_id, public, vulnerable, conpromised):
        self.node_id = node_id
        self.public = public
        self.vulnerable = vulnerable
        self.conpromised = conpromised

class Network:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)


N = Network()

def get_ends(graph):
    ends = []
    mids = []

    for n in graph.nodes:
        if graph.degree(n) == 1:
            ends.append(n)
        else:
            mids.append(n)

    return ends, mids


pub, non_pub = get_ends(G)
for p in pub:
    N.add_node(Node(p, True, False, False))

for np in non_pub:
    N.add_node(Node(np, False, False, False))


nx.draw(G, pos, nodelist=pub, node_color="tab:orange")
nx.draw(G, pos, nodelist=non_pub, node_color="tab:blue")

labels = {}
for n in G.nodes:
    labels[n] = n

nx.draw_networkx_labels(G, pos, labels, font_size=11, font_color="whitesmoke")
plt.show()

print(N.nodes[0].public)
