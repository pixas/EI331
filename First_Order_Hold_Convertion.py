import numpy as np
import matplotlib.pyplot as plt
import math
import Through_LPF
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use("seaborn-whitegrid")

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)

def first_order_hold_convertion(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7,t0 = 1/3):
    """calculate the result of the signal after first order hold convertion

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.              
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2. 
        sampling_rate (float, optional): [the sampling rate of sampling]. Defaults to 1.7. 
        t0 (float,optional): [the delay of the output compared with input(a parameter of the ideal LPF)]. Defaults to 1/3.
        
    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    fre1 = float(fre1)
    theta1 = float(theta1)
    fre2 = float(fre2)
    sampling_rate = float(sampling_rate)
    t0 = float(t0)
    (t,omega1,omega2,y1_,y2_,y3_) = Through_LPF.through_LPF(amplitude,fre1,theta1,fre2,sampling_rate,t0)
    T = 1 / sampling_rate

    #the data of time domain doesn't need to change

    #spectrum of real part
    y2_ = y2_ * (1 / T) * ((np.sin(omega1 * T / 2) / (omega1 / 2 + 1e-10)) ** 2) # avoid 0/0 situation

    #spectrum of imaginary part
    y3_ = np.zeros(1537)

    return t,omega1,omega2,y1_,y2_,y3_

def first_order_hold_convertion_plot(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7,t0 = 1/3):
    """plot the converted signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.              
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2. 
        sampling_rate (float, optional): [the sampling rate of sampling]. Defaults to 1.7. 
        t0 (float,optional): [the delay of the output compared with input(a parameter of the ideal LPF)]. Defaults to 1/3.   

    """
    (t,omega1,omega2,y1,y2,y3) = Through_LPF.through_LPF(amplitude,fre1,theta1,fre2,sampling_rate,t0)
    (t_,omega1_,omega2_,y1_,y2_,y3_) = first_order_hold_convertion(amplitude,fre1,theta1,fre2,sampling_rate,t0)
    
    #origin signal
    #plot in time domain
    F=MyFigure()
    F.ax1=F.fig.add_subplot(231)
    F.ax1.stem(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$y(t)$")
    F.ax1.set_title('signal through LPF in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(232)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax2.set_title('signal through LPF-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(233)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax3.set_title('signal through LPF-Im')

    #through LPF signal
    #spectrum of real part
    F.ax4=F.fig.add_subplot(234)
    F.ax4.plot(t_,y1_)
    F.ax4.set_xlabel("$t$")
    F.ax4.set_ylabel("$y(t)$")
    F.ax4.set_title('converted signal in time domain')

    #spectrum of real part
    F.ax5=F.fig.add_subplot(235)
    F.ax5.plot(omega1_,y2_)
    F.ax5.set_xlabel("$\omega$")
    F.ax5.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax5.set_title('converted signal-Re')

    #spectrum of imaginary part
    F.ax6=F.fig.add_subplot(236)
    F.ax6.plot(omega2_,y3_)
    F.ax6.set_xlabel("$\omega$")
    F.ax6.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax6.set_title('converted signal-Im')
    F.fig.subplots_adjust(wspace = 1,hspace = 0.7)
    return F
#if __name__ == "__main__":
#    first_order_hold_convertion_plot(theta1=np.pi/3)
#    plt.subplots_adjust(wspace = 0.7,hspace = 0.7)
#    plt.show()