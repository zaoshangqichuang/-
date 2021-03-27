# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:51:19 2020

@author: huangguo
"""
import numpy as np
class me_analysis_1(object):
    def __init__(self,p1,p3,N,p,q,mu):
        self.p1=p1
        self.p2=(p1+p3)/2
        self.p3=p3
        self.N=N
        self.p=p
        self.q=q
        self.mu=mu
        self.beta=((p**2+(1-p)**2*q**2)*p1+(2*(1-p)*(1-q)-(1-p)**2*(1-q)**2)*self.p2+2*p*(1-p)*q*p3)*(N-2)
        self.lambda0=self.beta*(N-1)*p/mu
        self.testz=1-1/self.lambda0 if 1-1/self.lambda0>0 else 0
    
class me_analysis_2(object):
    def __init__(self,m1,n1,n3,rho0):
        self.N,N=m1.N,m1.N
        self.p,p=m1.p,m1.p
        self.q,q=m1.q,m1.q
        self.mu,mu=m1.mu,m1.mu
        self.n1=n1
        self.n2=(n1+n3)/2
        self.n3=n3
        self.lambda_delta=(n1*p+self.n2*(1-p)*(1-q)+n3*(1-p)*q)*((N-1)*p*((N-1)*p-1)/2)/mu
        A1=self.lambda_delta
        B1=m1.lambda0-self.lambda_delta
        C1=1-m1.lambda0
        delta=B1**2-4*A1*C1
        if delta>0:
            self.rho1=(-B1+np.sqrt(delta))/(2*A1)
            self.rho2=(-B1-np.sqrt(delta))/(2*A1)
            if self.rho2>0:
                if rho0>self.rho2:
                    self.testz1=self.rho1
                else:
                    self.testz1=0
            elif self.rho1>0:
                self.testz1=self.rho1
            else:
                self.testz1=0
        else:
            self.rho1=None
            self.rho2=None
            self.testz1=0            
        
        
