from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpld3
import numba
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
interval_t = 100

def offline(request):
    return render(request, 'offline.html')

def download(request):    
    file_path = os.path.join(settings.MEDIA_ROOT, 'wef2.py')    
    if os.path.exists(file_path):    
        with open(file_path, 'rb') as fh:    
            response = HttpResponse(fh.read(), content_type="application/py.python")    
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)    
            return response

@numba.njit
def kuramoto(theta, t, omega, K, N):
    A, B = sin(theta), cos(theta)
    return omega + (K / N) * (B * sum(A) - A * sum(B))

def adaptive_kuramoto(theta,t,omega,K,N):
    A,B = sin(theta), cos(theta)
    return omega+((K*abs(omega))/N)*(B*sum(A)-A*sum(B))

def theta(kuramoto, theta01, t, omega, K, N):
    return odeint(kuramoto, theta01, t, args=(omega, K, N))

def rt(kuramoto,theta01,t,omega,K,N,interval_t):
        S1 = [sum(cos(theta(kuramoto, theta01, t, omega, K, N)[i])) for i in range(interval_t)]
        d1 = array([i ** 2 for i in S1])

        S2 = [sum(sin(theta(kuramoto, theta01, t, omega, K, N)[i])) for i in range(interval_t)]
        d2 = array([i ** 2 for i in S2])
        return d1 + d2

def rt2(kuramoto,theta02,t,omega2,j,N2,interval_t):
            theta2 = odeint(kuramoto,theta02,t,args=(omega2,j,N2))
            S1 = [sum(cos(theta2[i])) for i in range(interval_t)]
            d1 = array([i ** 2 for i in S1])

            S2 = [sum(sin(theta2[i])) for i in range(interval_t)]
            d2 = array([i ** 2 for i in S2])
            return d1 + d2

#<------------------------------------------------------------------------->

def index(request):
    N1 = 50  # число осциляторов
    K1 = 300  # K/N = параметр амплитуды связи
    l1 = random.uniform(0, 2 * pi, N1)
    theta01 = []  # начальные фазы
    for i in l1:
        theta01.append('%.1f' % i)  # количество точек после запятой

    omega1 = random.uniform(1, 3, N1)  # частота

    t1 = linspace(0, 0.1, interval_t)  # время

    # вычисление r(t)

    r1 = (1.0 / N1) * sqrt(rt(kuramoto,theta01,t1,omega1,K1,N1,interval_t))

    # построение графиков
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
    for i in range(N1):
        ax1.plot(t1, sin(omega1[i] * t1 + theta(kuramoto, theta01, t1, omega1, K1, N1)[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t1, r1)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig1.tight_layout()
    html_fig1 = mpld3.fig_to_html(fig1, template_type='general')

    plt.close(fig1)


    N2 = 10
    m2 = 50
    K2 = linspace(0,8,m2)
    theta02 = random.uniform(0,2*pi,N2)
    omega2 = random.uniform(1,5,N2)
    
    t = linspace(0, 2, interval_t)
    L = []
    for j in K2:

        r = (1.0 / N2) * sqrt(rt2(kuramoto,theta02,t,omega2,j,N2,interval_t))

        x = sum(r[(len(r)//2):])/(interval_t//2)
        L.append(x)
    fig2, ax3 = plt.subplots()
    ax3.plot(K2, L)
    ax3.set(xlabel='K', ylabel='r ∞')
    ax3.grid()
    html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
    plt.close(fig2)

    NA = 90
    ma = 50
    Ka1 = linspace(0,4,ma)
    interval_t_a = 1000  #пространство i

    theta0a = random.uniform(0,2*pi,NA)
    omegaa = random.triangular(-10,0,10,NA)

    ta = linspace(0,100,interval_t_a)

    LA = []


    for h in Ka1: 
        thetaa = odeint(adaptive_kuramoto,theta0a,ta,args=(omegaa,h,NA))
        S1a = [sum(cos(thetaa[o])) for o in range(interval_t_a)]
        d1a = array([o**2 for o in S1a])
    
        S2a = [sum(sin(thetaa[p])) for p in range(interval_t_a)]
        d2a = array([p**2 for p in S2a])

        ra = (1.0/NA)*sqrt(d1a + d2a)
    
        xa = sum(ra[(len(ra)//2):])/(interval_t_a//2)
        LA.append(xa)

    fig3, ax4 = plt.subplots()
    ax4.plot(Ka1,LA)
    ax4.set(xlabel='K', ylabel='r ∞')
    ax4.grid()
    html_fig3 = mpld3.fig_to_html(fig3, template_type='general')
    plt.close(fig3)
    return render(request, 'index.html', {'div_figure1': html_fig1, 'div_figure2': html_fig2, 'div_figure3': html_fig3})


def graph_n1(request):
    N_ = int(request.POST['N'])
    K = int(request.POST['K'])
    t_ = int(request.POST['t'])
    l = random.uniform(0, 2 * pi, N_)
    theta0 = []  # начальные фазы
    for i in l:
        theta0.append('%.1f' % i)  # количество точек после запятой

    omega = random.uniform(1, 3, N_)  # частота


    t = linspace(0, t_, interval_t)  # время

    
    # вычисление r(t)

    r = (1.0 / N_) * sqrt(rt(kuramoto,theta0,t,omega,K,N_,interval_t))

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(15,6))
    for i in range(N_):
        ax1.plot(t, sin(omega[i] * t + theta(kuramoto, theta0, t, omega, K, N_)[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t, r)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig.tight_layout()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)

    return render(request, 'graph_n1.html', {'div_figure': html_fig})


def graph_n2(request):
    N = int(request.POST['N'])
    m = int(request.POST['m'])
    t__ = int(request.POST['t'])
    K = linspace(0,t__,m)

    theta0 = random.uniform(0,2*pi,N)
    omega = random.uniform(1,5,N)

    t = linspace(0, t__, interval_t)  # время

    L = []

    for j in K:
        r = (1.0 / N) * sqrt(rt2(kuramoto,theta0,t,omega,j,N,interval_t))

        x = sum(r[(len(r)//2):])/(interval_t//2)
        L.append(x)

    #построение графика
    fig, ax = plt.subplots()
    #for i in range(m-1):
    ax.plot(K, L)
    ax.set(xlabel='K', ylabel='r ∞')

    ax.grid()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)
    return render(request, 'graph_n2.html', {'div_figure': html_fig})


def graph_n3(request):
    NA = int(request.POST['N'])
    ma = int(request.POST['m'])
    tt = int(request.POST['t'])
    Ka1 = linspace(0,tt,ma)
    interval_t_a = 1000  #пространство i

    theta0a = random.uniform(0,2*pi,NA)
    omegaa = random.triangular(-10,0,10,NA)

    ta = linspace(0,100,interval_t_a)

    LA = []


    for h in Ka1: 
        thetaa = odeint(adaptive_kuramoto,theta0a,ta,args=(omegaa,h,NA))
        S1a = [sum(cos(thetaa[o])) for o in range(interval_t_a)]
        d1a = array([o**2 for o in S1a])
    
        S2a = [sum(sin(thetaa[p])) for p in range(interval_t_a)]
        d2a = array([p**2 for p in S2a])

        ra = (1.0/NA)*sqrt(d1a + d2a)
    
        xa = sum(ra[(len(ra)//2):])/(interval_t_a//2)
        LA.append(xa)
        
    fig, ax = plt.subplots()
    ax.plot(Ka1,LA)
    ax.set(xlabel='K', ylabel='r ∞')
    ax.grid()
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return render(request, 'graph_n3.html', {'div_figure': html_fig})

def graph_n4(request):
    NA = int(request.POST['N'])
    ma = int(request.POST['m'])
    tt = int(request.POST['t'])
    Ka1 = linspace(tt,0,ma)
    interval_t_a = 1000  #пространство i

    theta0a = random.uniform(0,2*pi,NA)
    omegaa = random.triangular(-10,0,10,NA)

    ta = linspace(0,100,interval_t_a)

    LA = []


    for h in Ka1: 
        thetaa = odeint(adaptive_kuramoto,theta0a,ta,args=(omegaa,h,NA))
        S1a = [sum(cos(thetaa[o])) for o in range(interval_t_a)]
        d1a = array([o**2 for o in S1a])
    
        S2a = [sum(sin(thetaa[p])) for p in range(interval_t_a)]
        d2a = array([p**2 for p in S2a])

        ra = (1.0/NA)*sqrt(d1a + d2a)
    
        xa = sum(ra[(len(ra)//2):])/(interval_t_a//2)
        LA.append(xa)
        
    fig, ax = plt.subplots()
    ax.plot(Ka1,LA)
    ax.set(xlabel='K', ylabel='r ∞')
    ax.grid()
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return render(request, 'graph_n4.html', {'div_figure': html_fig})


def ru(request):
    N1 = 50  # число осциляторов
    K1 = 300  # K/N = параметр амплитуды связи
    l1 = random.uniform(0, 2 * pi, N1)
    theta01 = []  # начальные фазы
    for i in l1:
        theta01.append('%.1f' % i)  # количество точек после запятой

    omega1 = random.uniform(1, 3, N1)  # частота

    t1 = linspace(0, 0.1, interval_t)  # время

    # вычисление r(t)

    r1 = (1.0 / N1) * sqrt(rt(kuramoto,theta01,t1,omega1,K1,N1,interval_t))

    # построение графиков
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
    for i in range(N1):
        ax1.plot(t1, sin(omega1[i] * t1 + theta(kuramoto, theta01, t1, omega1, K1, N1)[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t1, r1)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig1.tight_layout()
    html_fig1 = mpld3.fig_to_html(fig1, template_type='general')

    plt.close(fig1)


    N2 = 10
    m2 = 50
    K2 = linspace(0,8,m2)
    theta02 = random.uniform(0,2*pi,N2)
    omega2 = random.uniform(1,5,N2)
    
    t = linspace(0, 2, interval_t)
    L = []
    for j in K2:

        r = (1.0 / N2) * sqrt(rt2(kuramoto,theta02,t,omega2,j,N2,interval_t))

        x = sum(r[(len(r)//2):])/(interval_t//2)
        L.append(x)
    fig2, ax3 = plt.subplots()
    ax3.plot(K2, L)
    ax3.set(xlabel='K', ylabel='r ∞')
    ax3.grid()
    html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
    plt.close(fig2)

    NA = 90
    ma = 50
    Ka1 = linspace(0,4,ma)
    interval_t_a = 1000  #пространство i

    theta0a = random.uniform(0,2*pi,NA)
    omegaa = random.triangular(-10,0,10,NA)

    ta = linspace(0,100,interval_t_a)

    LA = []


    for h in Ka1: 
        thetaa = odeint(adaptive_kuramoto,theta0a,ta,args=(omegaa,h,NA))
        S1a = [sum(cos(thetaa[o])) for o in range(interval_t_a)]
        d1a = array([o**2 for o in S1a])
    
        S2a = [sum(sin(thetaa[p])) for p in range(interval_t_a)]
        d2a = array([p**2 for p in S2a])

        ra = (1.0/NA)*sqrt(d1a + d2a)
    
        xa = sum(ra[(len(ra)//2):])/(interval_t_a//2)
        LA.append(xa)

    fig3, ax4 = plt.subplots()
    ax4.plot(Ka1,LA)
    ax4.set(xlabel='K', ylabel='r ∞')
    ax4.grid()
    html_fig3 = mpld3.fig_to_html(fig3, template_type='general')
    plt.close(fig3)
    return render(request, 'ru.html', {'div_figure1': html_fig1, 'div_figure2': html_fig2, 'div_figure3': html_fig3})