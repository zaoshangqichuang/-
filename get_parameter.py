# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:54:34 2020

@author: huangguo
"""
#use linear programing to solve p1,p2,n1,n2
import pulp
import numpy as np
import matplotlib.pyplot as plt
from me_analysis import me_analysis_1
from me_analysis import me_analysis_2
#get p1,p2 from me1
def get_sim1_p(lambda1,N,p,q,mu):
    A1=p**2+(1-p)**2*q**2
    A2=2*(1-p)*(1-q)-(1-p)**2*(1-q)**2
    A3=2*p*(1-p)*q
    prob = pulp.LpProblem(sense=pulp.LpMinimize)
    p1 = pulp.LpVariable('p1', lowBound=0,upBound=1)
    p2 = pulp.LpVariable('p2', lowBound=0,upBound=1)
    prob += p1-2*p2
    prob+=(p1-2*p2>=0)
    prob+=((A1+A2/2)*p1+(A2/2+A3)*p2==lambda1*mu/((N-2)*(N-1)*p))
    prob.solve()
    return pulp.value(p1),pulp.value(p2)

#get n1,n2 from me2
def get_sim2_n(lambda2,N,p,q,mu):
    A1=p
    A2=(1-p)*(1-q)
    A3=(1-p)*q
    prob = pulp.LpProblem(sense=pulp.LpMinimize)
    n1 = pulp.LpVariable('n1', lowBound=0,upBound=1)
    n2 = pulp.LpVariable('n2', lowBound=0,upBound=1)
    prob += n1-2*n2
    prob+=(n1-2*n2>=0)
    prob+=((A1+A2/2)*n1+(A2/2+A3)*n2==lambda2*mu/(((N-1)*p-1)*(N-1)*p/2))
    prob.solve()
    return pulp.value(n1),pulp.value(n2)
    


def test():
    lambda1=0.5
    lambda2=2.5
    N=800
    p=0.005
    q=0.003
    mu=0.3
    rho0=0.5
    #n1,n2=get_sim2_n(lambda2,N,p,q,mu)
    #m1=me_analysis_1(p1,p2,N,p,q,mu)
    #m2=me_analysis_2(m1,n1,n2,rho0)
    #lambda=0.5:2.5:0.1
    #lambda_delta=0.8,2.5
    lam_array=np.arange(lambda1,lambda2+0.1,0.1)
    p1_array=np.zeros(len(lam_array),dtype=float)
    p3_array=np.zeros(len(lam_array),dtype=float)
    lam_delta_array=np.array([0.8,2])
    n1_array=np.zeros(len(lam_delta_array),dtype=float)
    n3_array=np.zeros(len(lam_delta_array),dtype=float)
    i=0
    for lambda0 in lam_array:
        p1_array[i],p3_array[i]=get_sim1_p(lambda0,N,p,q,mu)
        i+=1
    i=0
    for lambda_delta in lam_delta_array:
        n1_array[i],n3_array[i]=get_sim2_n(lambda_delta,N,p,q,mu)
        i+=1
    
    #test
    lam_test_array=np.zeros(len(lam_array),dtype=float)
    lam_delta_test_array=np.zeros(len(lam_delta_array),dtype=float)
    i=0
    for (p1,p3) in zip(p1_array,p3_array):
        m1=me_analysis_1(p1,p3,N,p,q,mu)
        lam_test_array[i]=m1.lambda0
        i+=1
    i=0
    for (n1,n3) in zip(n1_array,n3_array):
        m1=me_analysis_1(p1,p3,N,p,q,mu)
        lam_delta_test_array[i]=me_analysis_2(m1,n1,n3,rho0).lambda_delta
        i+=1
    
    fig=plt.figure()
    ax1=fig.add_subplot(121)
    ax1.plot(lam_array,lam_test_array,'o',color='blue')
    ax1.plot(lam_array,lam_array,'-',color='red')
    ax1.set_xlabel("$\\lambda$")
    ax1.set_ylabel("$\\lambda test$")
    ax2=fig.add_subplot(122)
    ax2.plot(lam_delta_array,lam_delta_test_array,'o',color='blue')
    ax2.plot(lam_delta_array,lam_delta_array,'-',color='red')
    ax2.set_xlabel("$\\lambda_\\Delta$")
    ax2.set_ylabel("$\\lambda_\\Delta test$")
    fig.subplots_adjust(wspace =0.5, hspace =0)
    fig.show()