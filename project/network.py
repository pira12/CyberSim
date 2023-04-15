import networkx as nx
import matplotlib.pyplot as plt
import random



# print(nx.info(G))
# print([e for e in G.edges])
# print(G.degree(0))


class Node:
    def __init__(self, node_id, public, vulnerable, compromised):
        self.node_id = node_id
        self.public = public
        self.vulnerable = vulnerable
        self.compromised = compromised

    def make_vulnerable(self):
        self.vulnerable = True

    def patch(self):
        self.vulnerable = False

    def make_compromised(self):
        self.compromised = True


class Network:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = []
        self.public = []
        self.non_public = []
        self.edges = []

        self.compromised_nodes = []
        self.attack_visual_nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_pub(self, node_id):
        if node_id not in self.public:
            self.public.append(node_id)

    def add_non_pub(self, node_id):
        if node_id not in self.non_public:
            self.non_public.append(node_id)

    def add_edge(self, edge):
        self.edges.append(edge)

    # Random set some nodes to random
    # Perhaps also change self.nodes in sync.
    def random_vulnerable(self):
        for n in self.nodes:
            if random.random() > 0.5:
                n.make_vulnerable()

    # Add a compromised node-id to the list.
    # Also update the (non public) nodes the attacker can see.
    def add_comp(self, node_id):
        if node_id not in self.compromised_nodes:
            self.nodes[node_id].make_compromised()
            self.compromised_nodes.append(node_id)
            self.add_att_vis(node_id)

    # Add all neighbors of the given node to the
    # list of visible (non public) nodes for the attacker.
    # Add the compromised node as well.
    def add_att_vis(self, node_id):
        for neigh in self.graph.neighbors(node_id):
            if neigh not in self.attack_visual_nodes:
                self.attack_visual_nodes.append(neigh)

        if node_id not in self.attack_visual_nodes:
            self.attack_visual_nodes.append(node_id)


def get_ends(graph):
    ends = []

    for n in graph.nodes:
        if graph.degree(n) == 1:
            ends.append(n)

    return ends


def create_network(number_of_nodes):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    """

    G = nx.powerlaw_cluster_graph(number_of_nodes, 1, 0.4)
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    N = Network(G)
    pub = get_ends(G)

    for numb in range(0, number_of_nodes):
        if numb in pub:
            N.add_node(Node(numb, True, False, False))
            N.add_pub(numb)
        else:
            N.add_node(Node(numb, False, False, False))
            N.add_non_pub(numb)

    return N, pos


N, pos = create_network(20)
N.random_vulnerable()


nx.draw(N.graph, pos, nodelist=N.public, node_color="tab:orange")
nx.draw(N.graph, pos, nodelist=N.non_public, node_color="tab:blue")

labels = {}
for n in N.graph.nodes:
    labels[n] = n

nx.draw_networkx_labels(N.graph, pos, labels, font_size=11, font_color="whitesmoke")
plt.show()


N.add_comp(13)
N.add_comp(14)
N.add_comp(15)
N.add_comp(16)
N.add_comp(17)

print("compromised:", N.compromised_nodes)
print("Visible to attacker", N.attack_visual_nodes)


nx.draw(N.graph, pos, nodelist=N.public, node_color="tab:orange")
nx.draw(N.graph, pos, nodelist=N.non_public, node_color="tab:blue")
nx.draw(N.graph, pos, nodelist=N.compromised_nodes, node_color="tab:red")

labels = {}
for n in N.graph.nodes:
    labels[n] = n

nx.draw_networkx_labels(N.graph, pos, labels, font_size=11, font_color="whitesmoke")
plt.show()
