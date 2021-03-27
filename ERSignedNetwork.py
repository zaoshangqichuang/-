# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:37:29 2020

@author: huangguo
"""
import numpy as np
import scipy.sparse
from scipy.sparse import coo_matrix, csr_matrix
import statsmodels.tsa.stattools as ts

#构建符号随机网络，N为符号网络的节点数，p为生成正边的概率，q为非正边中生成负边的概率
class ERSignedNetwork(object):
    
    def __init__(self,N,p,q):
        self.N=N
        self.p=p
        self.q=q
    def get_nt(self):
        x=list()
        y=list()
        for i in range(1,self.N):
            x+=list(range(i+1,self.N+1))
            y+=list(np.ones(self.N-i,dtype=np.int)*i)
        x=np.array(x)#target节点坐标
        y=np.array(y)#source节点坐标
        t=np.random.rand(int(self.N*(self.N+1)/2-self.N))
        t[t<self.p]=1
        t[t!=1]=0
        id=np.where(t==0)[0]
        t1=np.random.rand(np.size(id))
        t[id[t1<self.q]]=-1
        t=t.astype(np.int)
        d1 = coo_matrix((t, (y-1, x-1)))
        d2=d1.toarray()
        d2=np.vstack([d2, np.zeros(self.N,dtype=int)])
        d2=d2+d2.T
        return d2
