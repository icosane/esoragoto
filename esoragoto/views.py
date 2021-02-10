from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render
#from subprocess import run,PIPE
#import sys
from esoragoto.forms import TextForm
from django.core.management import call_command
#from nettools import tasks
#def external(request):
   # inp = request.POST.get('param')
    #out = run(sys.executable,['.//prog.py',int(inp)],shell=False,stdout=PIPE)
    #return render(request,'result.html',{'data1':out})

def post(self,request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            data1 = form.cleaned_data['post']

            context = another(data1)
        return render(request, 'another.html', context)


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

    return render(request, 'home.html', {'active_page': 'home.html', 'div_figure': html_fig})

def another(request):
    N_ = {{'data1'}}
    K = 3
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
