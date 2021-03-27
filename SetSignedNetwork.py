# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:19:54 2020

@author: 201921250004
"""
import numpy as np
import random
import networkx as nx
class SetSignedNetwork(object):
    def __init__(self,Network):
        self.NetworkType=Network["NetworkType"]
        self.N=Network["N"]
        self.k=Network["k"]
        self.p=Network.get("p",None)
        self.p_n=Network.get("p_n",None)
        if self.NetworkType=="er":#ER network
            self.nosignNetwork = nx.erdos_renyi_graph(self.N, self.k/(self.N-1))
        if self.NetworkType=="ws":#ER network
            self.nosignNetwork = nx.watts_strogatz_graph(self.N,self.k,self.p)
        if self.NetworkType=="ba":#BA network
            self.nosignNetwork = nx.barabasi_albert_graph(self.N,self.k)
        if self.NetworkType=="re":#Re network
            self.nosignNetwork = nx.random_regular_graph(self.k,self.N)
    def add_Sign(self,p_n):
        self.signedNetwork=self.nosignNetwork
        self.p_n=p_n
        for u,v,wt in self.signedNetwork.edges.data():
            if random.random()<self.p_n:
                self.signedNetwork[u][v]["ne_weight"]=int(1)
                self.signedNetwork[u][v]["po_weight"]=int(0)
            else:
                self.signedNetwork[u][v]["ne_weight"]=int(0)
                self.signedNetwork[u][v]["po_weight"]=int(1)
        return self.signedNetwork
    
    def get_degree(self):
        po_degree_array=np.array(list(self.signedNetwork.degree(weight="po_weight")))
        ne_degree_array=np.array(list(self.signedNetwork.degree(weight="ne_weight")))
        po_mean=np.mean(po_degree_array[:,1])
        ne_mean=np.mean(ne_degree_array[:,1])
        return po_mean,ne_mean
    
def WeightedMatrix(G):
    ne_W=np.array(nx.adjacency_matrix(G,weight="ne_weight").todense())
    po_W=np.array(nx.adjacency_matrix(G,weight="po_weight").todense())
    W=ne_W*-1+po_W
    return W




