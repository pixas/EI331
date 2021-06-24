from re import M
import numpy as np
import matplotlib.pyplot as plt
import math
import Sampling
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use("seaborn-whitegrid")
    
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)

def through_LPF(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7,t0 = 1/3):
    """calculate the result of the sampled signal went through an ideal LPF

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
    (t,omega1,omega2,y1_,y2_,y3_) = Sampling.sampling_sinusoid(amplitude,fre1,theta1,fre2,sampling_rate)
    LPF_fre = fre1 * 1.5 + fre2 * 1.5 #set the cut-off frequency of the ideal LPF to be the half of the positive x-axis

    #time domain
    y_LPF = np.sin(LPF_fre * (t - t0)) / (np.pi * (t - t0))
    y1_ = np.convolve(y_LPF,y1_,mode = 'same')

    #spectrum of real part
    for i in range(int((-LPF_fre + (fre1 + fre2) * 3) * 1536 / ((fre1 + fre2) * 6))):
        y2_[i] = 0
    for i in range(int((LPF_fre + (fre1 + fre2) * 3 )* 1536 / ((fre1 + fre2) * 6)),1537):
        y2_[i] = 0    
    y2_ = np.cos(LPF_fre * t0) * y2_

    #spectrum of imaginary part
    for i in range(int((-LPF_fre + (fre1 + fre2) * 3) * 1536 / ((fre1 + fre2) * 6))):
        y3_[i] = 0
    for i in range(int((LPF_fre + (fre1 + fre2) * 3 )* 1536 / ((fre1 + fre2) * 6)),1537):
        y3_[i] = 0    
    y3_ = -np.sin(LPF_fre * t0) * y3_

    return t,omega1,omega2,y1_,y2_,y3_

def through_LPF_plot(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7,LPF_fre = np.pi,t0 = 1/3):
    """plot the signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.              
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2. 
        sampling_rate (float, optional): [the sampling rate of sampling]. Defaults to 1.7. 
        LPF_fre (float, optional): [the cut-off frequency of the ideal LPF]. Defaults to np.pi.
        t0 (float,optional): [the delay of the output compared with input(a parameter of the ideal LPF)]. Defaults to 1/3.   

    """
    (t,omega1,omega2,y1,y2,y3) = Sampling.sampling_sinusoid(amplitude,fre1,theta1,fre2,sampling_rate)
    (t_,omega1_,omega2_,y1_,y2_,y3_) = through_LPF(amplitude,fre1,theta1,fre2,sampling_rate,t0)
    F=MyFigure()
    #original signal   
    #plot in time domain
    F.ax1=F.fig.add_subplot(231)
    F.ax1.stem(t,y1)
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$y(t)$")
    F.ax1.set_title('modulated signal in time domain')

    #spectrum of real part
    F.ax2=F.fig.add_subplot(232)
    F.ax2.plot(omega1,y2)
    F.ax2.set_xlabel("$\omega$")
    F.ax2.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax2.set_title('spectrum of modulated signal-Re')

    #spectrum of imaginary part
    F.ax3=F.fig.add_subplot(233)
    F.ax3.plot(omega2,y3)
    F.ax3.set_xlabel("$\omega$")
    F.ax3.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax3.set_title('spectrum of modulated signal-Im')

    #through LPF signal
    #plot in time domain
    F.ax4=F.fig.add_subplot(234)
    F.ax4.stem(t_,y1_)
    F.ax4.set_xlabel("$t$")
    F.ax4.set_ylabel("$y(t)$")
    F.ax4.set_title('signal through LPF in time domain')

    #spectrum of real part
    F.ax5=F.fig.add_subplot(235)
    F.ax5.plot(omega1_,y2_)
    F.ax5.set_xlabel("$\omega$")
    F.ax5.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax5.set_title(' signal through LPF-Re')

    #spectrum of imaginary part
    F.ax6=F.fig.add_subplot(236)
    F.ax6.plot(omega2_,y3_)
    F.ax6.set_xlabel("$\omega$")
    F.ax6.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax6.set_title('signal  through LPF-Im')
    F.fig.subplots_adjust(wspace = 1,hspace = 0.7)
    return F
#if __name__ == "__main__":
#    through_LPF_plot(theta1=-np.pi/3,fre1=np.pi/2,fre2=2*np.pi)
#    plt.subplots_adjust(wspace = 0.7,hspace = 0.7)
#    plt.show()