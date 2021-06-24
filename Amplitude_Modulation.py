from re import M
from DT_convolution import MyFigure
import numpy as np
import matplotlib.pyplot as plt
import math
plt.style.use("seaborn-whitegrid")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#shift > 0 =>move to the right
#shift < 0 =>move to the left
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)

def generate_sinusoid(amplitude = 1,fre = np.pi,theta = 0):
    """generate a sinusoidal signal as modulating signal

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        fre (float, optional): [the frequency of this waveform]. Defaults to np.pi.
        theta (float, optional): [the phase of this waveform]. Defaults to 0.        

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    fre = float(fre)
    theta = float(theta)

    #time domain
    t = np.linspace(-8 - theta / fre, 8 - theta / fre, num = 1025)
    y1 = float(amplitude) * (np.cos(fre * t + theta))

    #spectrum of real part
    omega1 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y2 = np.zeros(1025)
    y2[256] = np.pi * np.cos(theta) * amplitude
    y2[768] = np.pi * np.cos(theta) * amplitude

    #spectrum of imaginary part
    omega2 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y3 = np.zeros(1025)
    y3[256] = np.pi * np.sin(theta) * amplitude
    y3[768] = -np.pi * np.sin(theta) * amplitude

    return t,omega1,omega2,y1,y2,y3

def generate_sinusoid_plot(amplitude = 1,fre = np.pi,theta = 0):
    """plot the sinusoidal signal above

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        fre (float, optional): [the frequency of this waveform]. Defaults to np.pi.
        theta (float, optional): [the phase of this waveform]. Defaults to 0.        

    Returns:
        [np.ndarray]: [the array of the value of the signal in time domain]
    """
    amplitude = float(amplitude)
    fre = float(fre)
    theta = float(theta)

    (t,omega1,omega2,y1,y2,y3) = generate_sinusoid(amplitude,fre,theta)
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$x(t)$")
    F.ax1.set_title('modulating signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{X(j\omega)\}$")
    F.ax2.set_title('spectrum of modulating signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$t$")
    F.ax3.set_ylabel("$Im\{X(j\omega)\}$")
    F.ax3.set_title('spectrum of modulating signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F

def generate_unit_step(amplitude = 1, shift = 0):
    """generate a unit step signal as modulating signal

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        shift (float, optional): [the time shift of this waveform]. Defaults to 0.        

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    shift = float(shift)

    #time domain
    t = np.linspace(-8 + shift,8 + shift,num = 1025)
    y1 = np.zeros(1025)
    for i in range(int(shift + 8) * 64,1025):
        y1[i]=amplitude

    #spectrum of real part
    omega1 = np.linspace(-8,8,num = 1025)
    y2 = np.zeros(1025)
    for i in range(1025):
        if (omega1[i] == 0):
            continue
        y2[i] = -(np.sin(omega1[i] * shift)) / omega1[i]
    y2[512] = np.pi - shift #avoid 0/0 problem(By L'Hospital's rule)

    #spectrum of imaginary part
    omega2 = np.linspace(-8,8,num = 1025)
    y3 = np.zeros(1025)
    for i in range(1025):
        if (omega1[i] == 0):
            y3[i] == np.Infinity
            continue
        y3[i] = -(np.cos(omega2[i] * shift)) / (omega2[i]) #avoid 1/0 problem
    # y3[512] -= np.pi * np.sin(omega2 * float(shift))

    return t,omega1,omega2,y1,y2,y3


def generate_unit_step_plot(amplitude = 1, shift = 0):
    """plot the unit step signal above

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        shift (float, optional): [the time shift of this waveform]. Defaults to 0.        

    Returns:
        [np.ndarray]: [the array of the value of the signal in time domain]
    """    
    amplitude = float(amplitude)
    shift = float(shift)
    (t,omega1,omega2,y1,y2,y3) = generate_unit_step(amplitude,shift)
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$x(t)$")
    F.ax1.set_title('modulating signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{X(j\omega)\}$")
    F.ax2.set_title('spectrum of modulating signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{X(j\omega)\}$")
    F.ax3.set_title('spectrum of modulating signal-Im') 
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F  


def generate_unit_impulse(amplitude = 1, shift = 0):
    """generate a unit impulse signal as modulating signal

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        shift (float, optional): [the time shift of this waveform]. Defaults to 0.        

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    shift = float(shift)

    #plot in time domain
    t = np.linspace(-8 + shift, 8 + shift, num = 1025)
    y1 = np.zeros(1025)
    y1[512] = amplitude

    #spectrum of real part
    omega1 = np.linspace(-8,8,num = 1025)
    y2 = np.cos(omega1 * shift)

    #spectrum of imaginary part
    omega2 = np.linspace(-8,8,num = 1025)
    y3 = -np.sin(omega2 * shift)

    return t,omega1,omega2,y1,y2,y3

def generate_unit_impulse_plot(amplitude = 1, shift = 0):
    """plot the unit impulse signal above

    Args:
        amplitude (float, optional): [the amplitude of this waveform]. Defaults to 1.
        shift (float, optional): [the time shift of this waveform]. Defaults to 0.        

    Returns:
        [np.ndarray]: [the array of the value of the signal in time domain]
    """ 
    amplitude = float(amplitude)
    shift = float(shift)
    (t,omega1,omega2,y1,y2,y3) = generate_unit_impulse()
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$x(t)$")
    F.ax1.set_title('modulating signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{X(j\omega)\}$")
    F.ax2.set_title('spectrum of modulating signal-Re')
    
    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{X(j\omega)\}$")
    F.ax3.set_title('spectrum of modulating signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F

def sinusoidal_carrier(fre = np.pi/2,shift_of_modulating_signal = 0):
    """generate a sinusoidal signal as carrier signal

    Args:
        fre (float, optional): [the frequency of this waveform]. Defaults to np.pi/2.
        shift_of_modulating_signal (float, optional): [the time shift/phase of modulating signal]. Defaults to 0.        

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    fre = float(fre)
    shift_of_modulating_signal = float(shift_of_modulating_signal)

    #to simplify this function,we set the theta of carrier is 0
    
    #time domain
    t = np.linspace(-8 + shift_of_modulating_signal, 8 + shift_of_modulating_signal, num = 1025) #Two signals can be multiplied by each other in AM
    y1 = np.cos(fre * t)
    
    #spectrum of real part
    omega1 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y2 = np.zeros(1025)
    y2[256] = np.pi
    y2[768] = np.pi

    #spectrum of imaginary part
    omega2 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y3 = np.zeros(1025)

    return t,omega1,omega2,y1,y2,y3

def sinusoidal_carrier_plot(fre = np.pi/2,shift_of_modulating_signal = 0):
    """plot the sinusoidal signal above

    Args:
        fre (float, optional): [the frequency of this waveform]. Defaults to np.pi/2.
        shift_of_modulating_signal (float, optional): [the time shift/phase of modulating signal]. Defaults to 0.         

    Returns:
        [np.ndarray]: [the array of the value of the signal in time domain]
    """
    fre = float(fre)
    shift_of_modulating_signal = float(shift_of_modulating_signal)
    (t,omega1,omega2,y1,y2,y3) = sinusoidal_carrier(fre,shift_of_modulating_signal)
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$c(t)$")
    F.ax1.set_title('carrier signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{C(j\omega)\}$")
    F.ax2.set_title('spectrum of carrier signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{C(j\omega)\}$")
    F.ax3.set_title('spectrum of carrier signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F             


def AM_sinusoid(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2):
    """calculate the modulated signal of sinusoidal modulating signal

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.   
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.     

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """    
    amplitude = float(amplitude)
    fre1 = float(fre1)
    theta1 = float(theta1)
    fre2 = float(fre2)

    #time domain
    (_,_,_,x,_,_) = generate_sinusoid(amplitude,fre1,theta1)
    (_,_,_,c,_,_) = sinusoidal_carrier(fre2,-theta1 / fre1)
    t = np.linspace(-8 - theta1 / fre1, 8 - theta1 / fre1, num = 1025)
    y1 = c * x

    #spectrum of real part
    omega1 = np.linspace(-fre1 * 2 - fre2 * 2,fre1 * 2 + fre2 * 2,num = 1025)
    y2 = np.zeros(1025)
    y2[256] = 1/2 * np.pi * np.cos(theta1) * amplitude
    y2[768] = 1/2 * np.pi * np.cos(theta1) * amplitude
    y2[256 + int((fre1 * 2)/(fre1 * 4 + fre2 * 4) * 1024)] = 1/2 * np.pi * np.cos(theta1) * amplitude
    y2[768 - int((fre1 * 2)/(fre1 * 4 + fre2 * 4) * 1024)] = 1/2 * np.pi * np.cos(theta1) * amplitude


    #spectrum of imaginary part
    omega2 = np.linspace(-fre1 * 2 - fre2 * 2,fre1 * 2 + fre2 * 2,num = 1025)
    y3 = np.zeros(1025)
    y3[256] = 1/2 * np.pi * np.sin(theta1) * amplitude
    y3[768] = -1/2 * np.pi * np.sin(theta1) * amplitude
    y3[256 + int((fre1 * 2)/(fre1 * 4 + fre2 * 4) * 1024)] = 1/2 * np.pi * np.sin(theta1) * amplitude
    y3[768 - int((fre1 * 2)/(fre1 * 4 + fre2 * 4) * 1024)] = -1/2 * np.pi * np.sin(theta1) * amplitude

    return t,omega1,omega2,y1,y2,y3

def AM_sinusoid_plot(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2):
    """plot the modulated signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.   
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.     

    """
    amplitude = float(amplitude)
    fre1 = float(fre1)
    theta1 = float(theta1)
    fre2 = float(fre2)
    (t,omega1,omega2,y1,y2,y3) = AM_sinusoid(amplitude,fre1,theta1,fre2)
    generate_sinusoid_plot(amplitude,fre1,theta1)
    sinusoidal_carrier_plot(fre2,-theta1 / fre1)
    F=MyFigure()
    #plot in time domain       
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$y(t)$")
    F.ax1.set_title('modulated signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax2.set_title('spectrum of modulated signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax3.set_title('spectrum of modulated signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F

def AM_unit_step(amplitude = 1, shift = 0,fre = np.pi/2):
    """calculate the modulated signal of unit step modulating signal

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        shift (float, optional): [the time shift of modulating waveform]. Defaults to 0.
        fre (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.     

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    shift = float(shift)
    fre = float(fre)

    #time domain
    (_,_,_,x,_,_) = generate_unit_step(amplitude,shift)
    (_,_,_,c,_,_) = sinusoidal_carrier(fre,shift)
    t = np.linspace(-8 + shift,8 + shift,num = 1025)
    y1 = c * x

    #spectrum of real part
    omega1 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y2 = np.zeros(1025)
    for i in range(1025):
        if (omega1[i] == -fre or omega1[i] == fre):
            continue
        y2[i] = -1/2 * (np.sin((omega1[i] - fre)  * shift)) / (omega1[i] - fre) - 1/2 * (np.sin((omega1[i] + fre)  * shift)) / (omega1[i] + fre)
    y2[256] = (1/2) * np.pi - (1/2) * shift - 1/2 * (np.sin((omega1[i] - fre)  * shift)) / (omega1[i] - fre)
    y2[768] = (1/2) * np.pi - (1/2) * shift - 1/2 * (np.sin((omega1[i] + fre)  * shift)) / (omega1[i] + fre)#avoid 0/0 problem(By L'Hospital's rule)

    #spectrum of imaginary part
    omega2 = np.linspace(-fre * 2,fre * 2,num = 1025)
    y3 = np.zeros(1025)
    for i in range(1025):
        if (omega2[i] == fre or omega2[i] == -fre):
            y3[i] == np.Infinity
            continue
        y3[i] = -(1/2) * (np.cos((omega2[i] - fre) * shift)) / (omega2[i] - fre) - (1/2) * (np.cos((omega2[i] + fre) * shift)) / (omega2[i] + fre) #avoid 1/0 problem
    
    return t,omega1,omega2,y1,y2,y3

def AM_unit_step_plot(amplitude = 1, shift = 0,fre = np.pi/2):
    """plot the modulated signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        shift (float, optional): [the time shift of modulating waveform]. Defaults to 0.
        fre (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.    

    """    
    amplitude = float(amplitude)
    shift = float(shift)
    fre = float(fre)
    (t,omega1,omega2,y1,y2,y3) = AM_unit_step(amplitude,shift,fre)
    generate_unit_step_plot(amplitude,shift)
    sinusoidal_carrier_plot(fre,shift)
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$y(t)$")
    F.ax1.set_title('modulated signal in time domain')   

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax2.set_title('spectrum of modulated signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax3.set_title('spectrum of modulated signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F

def AM_unit_impulse(amplitude = 1, shift = 0,fre = np.pi/2):
    """calculate the modulated signal of unit impulse modulating signal

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        shift (float, optional): [the time shift of modulating waveform]. Defaults to 0.
        fre (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.     

    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    shift = float(shift)
    fre = float(fre)

    #time domain
    (_,_,_,x,_,_) = generate_unit_impulse(amplitude,shift)
    (_,_,_,c,_,_) = sinusoidal_carrier(fre,shift)
    t = np.linspace(-8 + shift,8 + shift,num = 1025)
    y1 = c * x

    #spectrum of real part
    omega1 = np.linspace(-8,8,num = 1025)
    y2 = (1/2) * np.cos((omega1 - fre) * shift) + (1/2) * np.cos((omega1 + fre) * shift)

    #spectrum of imaginary part
    omega2 = np.linspace(-8,8,num = 1025)
    y3 = -(1/2) * np.sin((omega2 - fre) * shift) - (1/2) * np.sin((omega2 + fre) * shift)
    
    return t,omega1,omega2,y1,y2,y3

def AM_unit_impulse_plot(amplitude = 1, shift = 0,fre = np.pi/2):
    """plot the modulated signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        shift (float, optional): [the time shift of modulating waveform]. Defaults to 0.
        fre (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2.    

    """
    amplitude = float(amplitude)
    shift = float(shift)
    fre = float(fre)
    (t,omega1,omega2,y1,y2,y3) = AM_unit_impulse(amplitude,shift,fre)
    generate_unit_impulse_plot(amplitude,shift)
    sinusoidal_carrier_plot(fre,shift)
    F=MyFigure()
    #plot in time domain
    F.ax1=F.fig.add_subplot(211)
    F.ax1.plot(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$y(t)$")
    F.ax1.set_title('modulated signal in time domain')   

    #spectrum of real part
    F.ax2=F.fig.add_subplot(223)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax2.set_title('spectrum of modulated signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(224)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax3.set_title('spectrum of modulated signal-Im')
    F.fig.subplots_adjust(wspace=0.7, hspace=0.5) 
    return F

#if __name__ == "__main__":
    #AM_sinusoid_plot(theta1=np.pi/3)
    #or:AM_unit_step_plot()/AM_unit_impulse_plot()
    #plt.subplots_adjust(wspace = 0.7,hspace = 0.7)
    #plt.show()
    #tip:You need to hit the button "最大化" so that the images do not overlap