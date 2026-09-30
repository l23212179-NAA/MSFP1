"""
Práctica 1: Diseño de controladores para un sistema de segundo orden

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nicole Arredondo Arevalo
Número de control: 23212179
Correo institucional: l23212179@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import numpy as np 
import math as m 
import matplotlib.pyplot as plt
import control as ctrl


# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas


# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N=round(tend/dt)+1 # Número de muestras
t=np.linspace(t0,tend,N) # Vector de tiempo
u1=np.ones(N) #Step
u2=np.zeros(N); u2[round(1/dt):round(2/dt)]=1  # Impulso
u3=t/tend #Rampa
u4=np.sin(m.pi/2*t) #Sinusoidal
u=np.column_stack((u1,u2,u3,u4)) # Entrada del sistema

signals=["step","impulso","rampa","sinusoidal"] # Nombre de las señales

# Componentes del circuito RLC y función de transferencia
R,L,C=4.7E3, 10E-3, 330E-6
num=[C*L*R,C*R**2+L,R]
den=[3*C*L*R,5*C*R**2+L,2*R]
sys=ctrl.tf(num,den)
print(f"Función de Transferencia: {sys}\n")

#Polos del sistema 
L = np.roots(den)
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")

#Componentes del controlador 
kI = 177.595
Cr = 1E-6
Re = 1/(Cr*kI)
numI = [1]
denI = [Re*Cr,0]
I = ctrl.tf(numI,denI)
print(f"El valor de la capacitancia Cr es de {Cr} Faradios. \n")
print(f"El valor de la resistencia Re es de {Re} Ohms. \n")
print(f"Funcion de transferencia del controlador I: {I}\n")

#Sistema de control en lazo cerrado 
x = ctrl.series(I,sys)
sysI = ctrl.feedback(x,1, sign=-1)
print(f"Función de transferencia del sistema de control en lazo cerrado: {sysI}\n")

#Colores
clr1 = np.array([255, 120, 115])/255
clr2 = np.array([226, 47, 128])/255
clr3 = np.array([255, 202, 149])/255

#Funciones del sistema en lazo abierto y lazo cerrado 
def openloop(t,sys,u):
    _,Vsu = ctrl.forced_response(sys,t,u,x0)
    return Vsu
def closedloop(t,sysI,u):
    _,Iu = ctrl.forced_response(sysI,t,u,x0)
    return Iu

#Respuestas: Simulaciones numericas 
for i in range(0,4):
    Vsu = openloop(t,sys,u[:,i])
    Iu = closedloop(t,sysI,u[:,i])
    fg = plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.plot(t,u[:,i],'-',color=clr1,label='Ve(t)')
    plt.plot(t,Vsu,'--',color=clr2,label='Vs(t)')
    plt.plot(t,Iu,':',linewidth=2.5,color=clr3,label='I(t)')
    plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
    if i==0 or i==1 or i==2:
        plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.3,0.1))
    elif i==3:
        plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.4,0.2))
    plt.xlabel('t [s]')
    plt.ylabel('Vi(t) [V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
    plt.show()
    fg.savefig(signals[i]+'_python.pdf',bbox_inches='tight')