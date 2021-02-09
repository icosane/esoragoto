from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import mpld3

N = 1000  #число осциляторов
K = 3  #K/N = параметр амплитуды связи
interval_t = 100  #пространство i
l = random.uniform(0,2*pi,N)
theta0 = []  #начальные фазы
for i in l:
    theta0.append('%.1f' % i)  #количество точек после запятой

#omega = int2.99
omega = random.uniform(1,3,N)  #частота
#omega = [1.1, 1.12, 1.13, 1.16, 1.18]

def kuramoto(theta,t,omega,K,N):
    A,B = sin(theta), cos(theta)
    return omega + (K/N)*(B*sum(A)-A*sum(B))

t = linspace(0,2,interval_t)				 #время

theta = odeint(kuramoto,theta0,t,args=(omega,K,N))  #решение системы диф. уравнений 1 порядка

#вычисление r(t)
S1 = [sum(cos(theta[i])) for i in range(interval_t)]
d1 = array([i**2 for i in S1])

S2 = [sum(sin(theta[i])) for i in range(interval_t)]
d2 = array([i**2 for i in S2])

r = (1.0/N)*sqrt(d1 + d2)

#построение графиков
fig = figure()
ax = fig.gca()
plt.subplot(1, 2, 1)
for i in range(N):
	plt.plot(t, sin(omega[i]*t+theta[:,i]))

plt.xlabel('t')
plt.ylabel('sin(ω(t)+θ)')

plt.subplot(1, 2, 2)
plt.plot(t, r)
plt.xlabel('t')
plt.ylabel('r (t)')

plt.tight_layout()
plt.grid()
mpld3.save_json(fig,'example.JSON')

#plt.show()
