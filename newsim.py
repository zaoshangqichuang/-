# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:55:42 2020

@author: huangguo
"""
import numpy as np
import random
import statsmodels.tsa.stattools as ts
import scipy.signal as signal
import itertools
class SIS_sim(object):
    def __init__(self,net,rho0,p1,p3,mu,t0,t1,t2):
        self.N=net.shape[0]
        self.p1=p1
        self.p2=(p1+p3)/2
        self.p3=p3
        self.mu=mu
        self.net=net
        self.rho0=rho0
        self.t0=t0
        self.limit_step_num=t1
        self.limit_test_step=t2
        self.beta_list=[]
#        self.m1=me_analysis_1(p1,p3,self.N,p,q,mu)
    def initial_setup(self):
        self.i_list=random.sample(list(range(0,self.N)),int(self.rho0*self.N))
        self.s_list=[val for val in range(0,self.N) if val not in self.i_list]
        self.triangle_num=np.zeros((self.t0,6),dtype=float)
        self.z=[self.rho0]
        #self.balanced_triangle=[]
        #self.weekbalanced_triangle=[]
        #self.unbalanced_triangle=[]
        #for i,j,k in itertools.combinations(np.arange(0,self.N,1),3):
            #if self.net[i,j]*self.net[j,k]*self.net[i,k]==1:
                #self.balanced_triangle.append([i,j,k])
            #elif self.net[i,j]*self.net[j,k]*self.net[i,k]==0:
                #self.weekbalanced_triangle.append([i,j,k])
            #elif self.net[i,j]*self.net[j,k]*self.net[i,k]==-1:
                #self.unbalanced_triangle.append([i,j,k])
        
    def sneighbors(self,i):
        neighbor=np.where(self.net[i,:]==1)[0]
        sneighbors=[val for val in neighbor if val in self.s_list]
        return sneighbors
    def ineighbors(self,i):
        neighbor=np.where(self.net[i,:]==1)[0]
        ineighbors=[val for val in neighbor if val in self.i_list]
        return ineighbors
    def get_zmean(self):
        return len(self.i_list)/self.N
    def infectAgent(self,i,j,t):
        h1=np.copy(self.net)[i,:]
        h2=np.copy(self.net)[j,:]
        mul_array=np.multiply(h1,h2)
        p1_num=np.sum(mul_array==1)
        p2_num=np.sum(mul_array==0)-2
        p3_num=np.sum(mul_array==-1)
        '''
        for k in np.arange(0,self.N,1):
            if k not in [i,j]:
                if self.net[i,k]*self.net[j,k]==1 and random.random()<self.p1:
                    self.newilist.append(j)
                elif self.net[i,k]*self.net[j,k]==0 and random.random()<self.p2:
                    self.newilist.append(j)
                elif self.net[i,k]*self.net[j,k]==-1 and random.random()<self.p3:
                    self.newilist.append(j)
        '''
        beta=self.p1*p1_num+self.p2*p2_num+self.p3*p3_num
        #self.triangle_num[t,0]=self.triangle_num[t,0]+p1_num
        #self.triangle_num[t,1]=self.triangle_num[t,1]+p2_num
        #self.triangle_num[t,2]=self.triangle_num[t,2]+p3_num
        #p1_rand=np.random.rand(p1_num)<self.p1 if p1_num>0 else list()
        #p2_rand=np.random.rand(p2_num)<self.p2 if p2_num>0 else list()
        #p3_rand=np.random.rand(p3_num)<self.p3 if p3_num>0 else list()
        #if True in p1_rand or True in p2_rand or True in p3_rand:
            #self.newilist.append(j)
        return beta
    
    def infectByTwoAgents(self,i,j,t):
        '''
        sneighbors1=self.sneighbors(i)
        sneighbors2=self.sneighbors(j)
        mutual_neighbors=[neighbor for neighbor in sneighbors1 if neighbor in sneighbors2]
        if len(mutual_neighbors)>0:
            if self.net[i,j]==1:
                n0=self.n1
            elif self.net[i,j]==0:
                n0=self.n2
            else:
                n0=self.n3
            for neighbor in mutual_neighbors:
                if random.random()<n0:
                    self.newilist.append(neighbor)
        '''
        if self.net[i,j]==1:
            return self.n1
        elif self.net[i,j]==0:
            return self.n2
        else:
            return self.n3
        #h1=np.copy(self.net)[ineighbors,:][:,ineighbors]
        #n1_num=int(np.sum(h1==1)/2)
        #n2_num=int((np.sum(h1==0)-len(ineighbors))/2)
        #n3_num=int(np.sum(h1==-1)/2)
        #self.triangle_num[t,3]=self.triangle_num[t,3]+n1_num
        #self.triangle_num[t,4]=self.triangle_num[t,4]+n2_num
        #self.triangle_num[t,5]=self.triangle_num[t,5]+n3_num
        #n1_rand=np.random.rand(n1_num)<self.n1 if n1_num>0 else list()
        #n2_rand=np.random.rand(n2_num)<self.n2 if n2_num>0 else list()
        #n3_rand=np.random.rand(n3_num)<self.n3 if n3_num>0 else list()
        #if True in n1_rand or True in n2_rand or True in n3_rand:
        #if random.random()<n1_num*self.n1+n2_num*self.n2+n3_num*self.n3:
            #self.newilist.append(i)
    def recoverAgent(self,agent):
        if random.random()<self.mu:
            self.newslist.append(agent)
        return 1

    def is_stable(self):#adf test to verity whether z is stable
        a=False
        z_mean=self.z[-1]
        if len(self.z)>self.limit_step_num:
            z_mean=np.max(self.z[-self.limit_test_step:])
            a=True
        return a,z_mean
        '''
        if len(self.z)>self.limit_step_num:
            p_value=ts.adfuller(self.z[-self.limit_test_step:])[2]
            if p_value<0.05:
                if self.z[-1]<0.1:
                    z_mean=np.min(self.z[-self.limit_test_step:])
                else:
                    z_mean=np.mean(self.z[-self.limit_test_step:])
                   #z_mean= max(np.array(self.z)[signal.argrelextrema(np.array(self.z), np.greater)])
                a=True
                '''


    def simlulation_1_simplex(self):
        self.initial_setup()
        t=0
        while t<self.t0 and len(self.i_list)!=self.N and len(self.s_list)!=self.N:
            self.newilist=list()#store the new infected nodes
            self.newslist=list()#store the new susceptible nodes
            '''
            snodes_array=np.array(self.s_list)
            self.state=np.zeros((self.N,1),dtype=int)
            self.state[np.array(self.i_list),:]=1
            ind_array=0.25*np.dot(self.net[snodes_array,:],self.state)>np.random.random((len(self.s_list),1))
            for node in snodes_array[ind_array[:,0]]:
                self.newilist.append(node)
            '''
            for j in self.s_list:
                beta=0
                for i in self.ineighbors(j):
                    beta+=self.infectAgent(i,j,t)
                self.beta_list.append(beta)
                if random.random()<beta:
                    self.newilist.append(j)
            for newi in list(set(self.newilist)):
                self.i_list.append(newi)
                self.s_list.remove(newi)
            #recover the agent
            if len(self.i_list)<self.N and len(self.i_list)>=1:
                for i in self.i_list:
                    if i in set(self.newilist):
                        continue
                    else:
                        self.recoverAgent(i)
                for news in list(set(self.newslist)):
                    self.s_list.append(news)
                    self.i_list.remove(news)
            self.z.append(self.get_zmean())
            t+=1
            stable,z_mean=self.is_stable()
            print("\rIterated {} times".format(t),end="")
            if stable is True and len(self.s_list) not in [0,self.N]:
                print("\n"+"already stable,jammed state")
                break
            if t==self.t0 and stable==False:
                print("\n"+"not stable,pls increase t0")
            if len(self.s_list) in [0,self.N]:
                print("\n"+"all node's state are same,exit")
        return self.z,z_mean
    
    def simlulation_2_simplex(self,n1,n3):
        self.initial_setup()
        t=0
        z_mean=self.rho0
        self.z=[z_mean]
        self.n1=n1
        self.n2=(n1+n3)/2
        self.n3=n3
        while t<self.t0 and len(self.i_list)!=self.N and len(self.s_list)!=self.N:
            self.newilist=list()#store the new infected nodes
            self.newslist=list()#store the new susceptible nodes
            #i nodes infected s nodes
            for j in self.s_list:
                beta=0
                for i in self.ineighbors(j):
                    beta+=self.infectAgent(i,j,t)
                if random.random()<beta:
                    self.newilist.append(j)
            #s nodes infected by two i nodes
            for k in self.s_list:
                if k in self.newilist:
                    continue
                beta=0
                if len(self.ineighbors(k))>=2:
                    for i,j in itertools.combinations(self.ineighbors(k),2):
                        beta+=self.infectByTwoAgents(i,j,t)
                if random.random()<beta:
                    self.newilist.append(k)
            
            '''
            for i,j in itertools.combinations(self.i_list,2):
                self.infectByTwoAgents(i,j,t)
            '''
            for newi in list(set(self.newilist)):
                self.i_list.append(newi)
                self.s_list.remove(newi)
            #recover the agent
            if len(self.i_list)<self.N and len(self.i_list)>=1:
                for i in self.i_list:
                    if i in set(self.newilist):
                        continue
                    else:
                        self.recoverAgent(i)
                for news in list(set(self.newslist)):
                    self.s_list.append(news)
                    self.i_list.remove(news)
            self.z.append(self.get_zmean())
            t+=1
            stable,z_mean=self.is_stable()
            print("\rIterated {} times".format(t),end="")
            if stable is True and len(self.s_list) not in [0,self.N]:
                print("\n"+"already stable,jammed state")
                break
            if t==self.t0 and stable==False:
                print("\n"+"not stable,pls increase t0")
            if len(self.s_list) in [0,self.N]:
                print("\n"+"all node's state are same,exit")
        return self.z,z_mean
    
    def TrackTriangles(self):
        size0=len(self.z)
        self.triangle_num=self.triangle_num[np.arange(0,size0),:]
        for i in range(0,size0):
            sum1=self.triangle_num[i,0]+self.triangle_num[i,1]+self.triangle_num[i,2]
            sum2=self.triangle_num[i,3]+self.triangle_num[i,4]+self.triangle_num[i,5]
            self.triangle_num[i,0]=self.triangle_num[i,0]/sum1
            self.triangle_num[i,1]=self.triangle_num[i,1]/sum1
            self.triangle_num[i,2]=self.triangle_num[i,2]/sum1
            self.triangle_num[i,3]=self.triangle_num[i,3]/sum2
            self.triangle_num[i,4]=self.triangle_num[i,4]/sum2
            self.triangle_num[i,5]=self.triangle_num[i,5]/sum2
        return self.triangle_num