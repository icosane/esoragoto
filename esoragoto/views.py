from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpld3
import numba
from django.shortcuts import render
from esoragoto.forms import TextForm

def offline(request):
    return render(request, 'offline.html')

    
def home(request):
    N = 10  # число осциляторов
    K = 3  # K/N = параметр амплитуды связи
    interval_t = 100  # пространство i
    l = random.uniform(0, 2 * pi, N)
    theta0 = []  # начальные фазы
    for i in l:
        theta0.append('%.1f' % i)  # количество точек после запятой

    # omega = int2.99
    omega = random.uniform(1, 3, N)  # частота

    # omega = [1.1, 1.12, 1.13, 1.16, 1.18]

    def kuramoto(theta, t, omega, K, N):
        A, B = sin(theta), cos(theta)
        return omega + (K / N) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    theta = odeint(kuramoto, theta0, t, args=(omega, K, N))  # решение системы диф. уравнений 1 порядка

    # вычисление r(t)
    S1 = [sum(cos(theta[i])) for i in range(interval_t)]
    d1 = array([i ** 2 for i in S1])

    S2 = [sum(sin(theta[i])) for i in range(interval_t)]
    d2 = array([i ** 2 for i in S2])

    r = (1.0 / N) * sqrt(d1 + d2)

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2)
    for i in range(N):
        ax1.plot(t, sin(omega[i] * t + theta[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t, r)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig.tight_layout()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)

    return render(request, 'graph.html', {'active_page': 'graph.html', 'div_figure': html_fig})

def another(request):
    N_ = int(request.POST['N'])
    K = int(request.POST['K'])
    interval_t = 100  # пространство i
    l = random.uniform(0, 2 * pi, N_)
    theta0 = []  # начальные фазы
    for i in l:
        theta0.append('%.1f' % i)  # количество точек после запятой

    # omega = int2.99
    omega = random.uniform(1, 3, N_)  # частота

    # omega = [1.1, 1.12, 1.13, 1.16, 1.18]

    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    theta = odeint(kuramoto, theta0, t, args=(omega, K, N_))  # решение системы диф. уравнений 1 порядка

    # вычисление r(t)
    S1 = [sum(cos(theta[i])) for i in range(interval_t)]
    d1 = array([i ** 2 for i in S1])

    S2 = [sum(sin(theta[i])) for i in range(interval_t)]
    d2 = array([i ** 2 for i in S2])

    r = (1.0 / N_) * sqrt(d1 + d2)

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2)
    for i in range(N_):
        ax1.plot(t, sin(omega[i] * t + theta[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t, r)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig.tight_layout()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)

    return render(request, 'another.html', {'div_figure': html_fig})

def home2(request):
    N = 10
    m = 50
    K = linspace(0,8,m)
    interval_t = 100  #пространство i

    theta0 = random.uniform(0,2*pi,N)
    omega = random.uniform(1,5,N)
    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    L = []

    for j in K:
        theta = odeint(kuramoto,theta0,t,args=(omega,j,N))

        S1 = [sum(cos(theta[i])) for i in range(interval_t)]
        d1 = array([i ** 2 for i in S1])

        S2 = [sum(sin(theta[i])) for i in range(interval_t)]
        d2 = array([i ** 2 for i in S2])

        r = (1.0 / N) * sqrt(d1 + d2)

        x = r[len(r)-1]
        L.append(x)

    #построение графика
    fig, ax = plt.subplots()
    #for i in range(m-1):
    ax.plot(K, L)
    ax.set(xlabel='K', ylabel='r ∞')

    ax.grid()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)
    return render(request, 'graph2.html', {'div_figure': html_fig})

def another2(request):
    N = int(request.POST['N'])
    m = 50
    K = linspace(0,8,m)
    interval_t = 100  #пространство i

    theta0 = random.uniform(0,2*pi,N)
    omega = random.uniform(1,5,N)
    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    L = []

    for j in K:
        theta = odeint(kuramoto,theta0,t,args=(omega,j,N))

        S1 = [sum(cos(theta[i])) for i in range(interval_t)]
        d1 = array([i ** 2 for i in S1])

        S2 = [sum(sin(theta[i])) for i in range(interval_t)]
        d2 = array([i ** 2 for i in S2])

        r = (1.0 / N) * sqrt(d1 + d2)

        x = r[len(r)-1]
        L.append(x)

    #построение графика
    fig, ax = plt.subplots()
    #for i in range(m-1):
    ax.plot(K, L)
    ax.set(xlabel='K', ylabel='r ∞')

    ax.grid()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)
    return render(request, 'another2.html', {'div_figure': html_fig})

#<------------------------------------------------------------------------->

def index(request):
    N1 = 50  # число осциляторов
    K1 = 300  # K/N = параметр амплитуды связи
    interval_t1 = 100  # пространство t
    l1 = random.uniform(0, 2 * pi, N1)
    theta01 = []  # начальные фазы
    for i in l1:
        theta01.append('%.1f' % i)  # количество точек после запятой

    #omega = int2.99
    omega1 = random.uniform(1, 3, N1)  # частота

    #omega = [1.1, 1.12, 1.13, 1.16, 1.18]
    @numba.njit
    def kuramoto1(theta1, t1, omega1, K1, N1):
        A, B = sin(theta1), cos(theta1)
        return omega1 + (K1 / N1) * (B * sum(A) - A * sum(B))

    t1 = linspace(0, 0.1, interval_t1)  # время

    theta1 = odeint(kuramoto1, theta01, t1, args=(omega1, K1, N1))  # решение системы диф. уравнений 1 порядка

    # вычисление r(t)
    S11 = [sum(cos(theta1[i])) for i in range(interval_t1)]
    d11 = array([i ** 2 for i in S11])

    S21 = [sum(sin(theta1[i])) for i in range(interval_t1)]
    d21 = array([i ** 2 for i in S21])

    r1 = (1.0 / N1) * sqrt(d11 + d21)

    # построение графиков
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
    for i in range(N1):
        ax1.plot(t1, sin(omega1[i] * t1 + theta1[:, i]))
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
    interval_t2 = 100  #пространство i
    theta02 = random.uniform(0,2*pi,N2)
    omega2 = random.uniform(1,5,N2)
    @numba.njit
    def kuramoto2(theta2, t2, omega2, K2, N2):
        A, B = sin(theta2), cos(theta2)
        return omega2 + (K2 / N2) * (B * sum(A) - A * sum(B))
    t2 = linspace(0, 2, interval_t2)
    L2 = []
    for j2 in K2:
        theta2 = odeint(kuramoto2,theta02,t2,args=(omega2,j2,N2))

        S12 = [sum(cos(theta2[i])) for i in range(interval_t2)]
        d12 = array([i ** 2 for i in S12])

        S22 = [sum(sin(theta2[i])) for i in range(interval_t2)]
        d22 = array([i ** 2 for i in S22])

        r2 = (1.0 / N2) * sqrt(d12 + d22)

        x2 = r2[len(r2)-1]
        L2.append(x2)
    fig2, ax3 = plt.subplots()
    ax3.plot(K2, L2)
    ax3.set(xlabel='K', ylabel='r ∞')
    ax3.grid()
    html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
    plt.close(fig2)
    return render(request, 'index.html', {'div_figure1': html_fig1, 'div_figure2': html_fig2})

def graph_n1(request):
    N_ = int(request.POST['N'])
    K = int(request.POST['K'])
    interval_t = 100  # пространство i
    l = random.uniform(0, 2 * pi, N_)
    theta0 = []  # начальные фазы
    for i in l:
        theta0.append('%.1f' % i)  # количество точек после запятой

    # omega = int2.99
    omega = random.uniform(1, 3, N_)  # частота

    # omega = [1.1, 1.12, 1.13, 1.16, 1.18]

    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    theta = odeint(kuramoto, theta0, t, args=(omega, K, N_))  # решение системы диф. уравнений 1 порядка

    # вычисление r(t)
    S1 = [sum(cos(theta[i])) for i in range(interval_t)]
    d1 = array([i ** 2 for i in S1])

    S2 = [sum(sin(theta[i])) for i in range(interval_t)]
    d2 = array([i ** 2 for i in S2])

    r = (1.0 / N_) * sqrt(d1 + d2)

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(15,6))
    for i in range(N_):
        ax1.plot(t, sin(omega[i] * t + theta[:, i]))
    ax1.set(xlabel='t', ylabel='sin(ω(t)+θ)')

    ax2.plot(t, r)
    ax2.set(xlabel='t', ylabel='r (t)')

    ax1.grid()
    ax2.grid()
    fig.tight_layout()
    html_fig = mpld3.fig_to_html(fig, template_type='general')

    plt.close(fig)

    return render(request, 'graph_n1.html', {'div_figure': html_fig})



def graph_n11(request):
    N_ = int(request.POST['N'])
    K = int(request.POST['K'])
    interval_t = 100  # пространство i
    l = random.uniform(0, 2 * pi, N_)
    theta0 = []  # начальные фазы
    for i in l:
        theta0.append('%.1f' % i)  # количество точек после запятой

    # omega = int2.99
    omega = random.uniform(1, 3, N_)  # частота

    # omega = [1.1, 1.12, 1.13, 1.16, 1.18]

    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 0.1, interval_t)  # время

    theta = odeint(kuramoto, theta0, t, args=(omega, K, N_))  # решение системы диф. уравнений 1 порядка

    # вычисление r(t)
    S1 = [sum(cos(theta[i])) for i in range(interval_t)]
    d1 = array([i ** 2 for i in S1])

    S2 = [sum(sin(theta[i])) for i in range(interval_t)]
    d2 = array([i ** 2 for i in S2])

    r = (1.0 / N_) * sqrt(d1 + d2)

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(15,6))
    for i in range(N_):
        ax1.plot(t, sin(omega[i] * t + theta[:, i]))
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
    m = 50
    K = linspace(0,8,m)
    interval_t = 100  #пространство i

    theta0 = random.uniform(0,2*pi,N)
    omega = random.uniform(1,5,N)
    def kuramoto(theta, t, omega, K, N_):
        A, B = sin(theta), cos(theta)
        return omega + (K / N_) * (B * sum(A) - A * sum(B))

    t = linspace(0, 2, interval_t)  # время

    L = []

    for j in K:
        theta = odeint(kuramoto,theta0,t,args=(omega,j,N))

        S1 = [sum(cos(theta[i])) for i in range(interval_t)]
        d1 = array([i ** 2 for i in S1])

        S2 = [sum(sin(theta[i])) for i in range(interval_t)]
        d2 = array([i ** 2 for i in S2])

        r = (1.0 / N) * sqrt(d1 + d2)

        x = r[len(r)-1]
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

