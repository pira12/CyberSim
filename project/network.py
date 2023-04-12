import networkx as nx
import matplotlib.pyplot as plt

G = nx.powerlaw_cluster_graph(20, 1, 0.4)

print(nx.info(G))
print([e for e in G.edges])

nx.draw(G, with_label=1)
plt.show()
