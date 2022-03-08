from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt


N = 100  #число осциляторов

m = 500
#K = 2
K = linspace(4,0,m)
#K = linspace(0,4,m)
#K = arange(0,8,1)
interval_t = 1000  #пространство i

theta0 = random.uniform(0,2*pi,N)
#theta0 = linspace(0,2*pi,N)

#omega = random.uniform(1,5,N)
omega = random.triangular(-10,0,10,N)
#omega = random.triangular(0,6,10,N)
#omega = random.triangular(-10,-6,-1,N)
#omega = random.triangular(2.88,2.99,3.18,N)
#omega = random.triangular(-3.18,-2.99,-2.88,N)
#omega = linspace(1,5,N)
#omega = 2.99


def kuramoto(theta,t,omega,K,N):             
    A,B = sin(theta), cos(theta)
    #return omega + (K/N)*(B*sum(A)-A*sum(B))
    #return omega*(1 + (K/N)*(B*sum(A)-A*sum(B)))
    return omega+((K*abs(omega))/N)*(B*sum(A)-A*sum(B))

t = linspace(0,100,interval_t)               #время 

L = []


for j in K: 
    theta = odeint(kuramoto,theta0,t,args=(omega,j,N))  #решение системы диф. уравнений 1 порядка

#вычисление r(t)
    S1 = [sum(cos(theta[i])) for i in range(interval_t)]
    d1 = array([i**2 for i in S1])
    
    S2 = [sum(sin(theta[i])) for i in range(interval_t)]
    d2 = array([i**2 for i in S2])

    r = (1.0/N)*sqrt(d1 + d2)
    
    x = sum(r[(len(r)//2):])/(interval_t//2) #убирание помех
    #x = sum(r[((len(r)//4)*3):])/(interval_t//4)
    #x = sum(r)/interval_t 

    #x = r[len(r)-1]
    
    L.append(x)

    
#построение графика

#for i in range(m-1):
plt.plot(K, L)
plt.xlabel('K')
plt.ylabel('r ∞')

plt.grid()
plt.show()

#print(K)
#print(L)
#print(omega)


