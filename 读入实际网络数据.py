#读入实际网络的数据
import networkx as nx
import numpy as np
'''
G=nx.Graph()
with open("Slashdot.txt","r") as f:
    for line in f.readlines():
        if line[0]!="#":
            node1,node2,edge=line.replace("\n","").split(sep="	")
            if int(edge) == 1:
                attr1={"po_weight":int(1),"ne_weight":int(0)}
            if int(edge) == -1:
                attr1={"po_weight":int(0),"ne_weight":int(1)}
            G.add_edges_from([(int(node1),int(node2),attr1)])
np.savez("Slashdot",G={"network":G})
'''
G1=np.load("Slashdot.npz",allow_pickle=True)["G"].item()["network"]
N=len(G1.nodes())

