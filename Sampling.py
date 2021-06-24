import numpy as np
import matplotlib.pyplot as plt
import math
import Amplitude_Modulation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use("seaborn-whitegrid")

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)

def sampling_sinusoid(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7):
    """calculate the sampled signal of the modulated signal

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.              
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2. 
        sampling_rate (float, optional): [the sampling rate of sampling]. Defaults to 1.7. 
        
    Returns:
        tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    amplitude = float(amplitude)
    fre1 = float(fre1)
    theta1 = float(theta1)
    fre2 = float(fre2)
    sampling_rate = float(sampling_rate)
    (_,_,_,y1,y2,y3) = Amplitude_Modulation.AM_sinusoid(amplitude,fre1,theta1,fre2)
    
    #time domain
    t_ = np.linspace(int(-8 - theta1 / fre1), int(8 - theta1 / fre1),num = int(16 * sampling_rate + 1))
    y1_ = np.zeros(int(16 * sampling_rate + 1))
    for i in range(int(16 * sampling_rate + 1)):
        y1_[i] = y1[int(i * 1024 / (16 * sampling_rate))]
    
    # spectrum of real part
    omega1_ = np.linspace(-fre1 * 3 - fre2 * 3,fre1 * 3 + fre2 * 3,num = 1537)
    y21 = np.zeros(512) #shrink the index in order to simplify calculation
    y2_ = np.zeros(1537)
    for i in range(512):
        y21[i] = y2[i + 256]
    for i in range(512,1024):
        y2_[i] = sampling_rate * y21[i - 512]
    for i in range(512):
        y2_[i] = sampling_rate * y2_[int(i + 2 * np.pi * sampling_rate * 256 / (fre1 + fre2))]
    for i in range(1025,1536):
        y2_[i] = sampling_rate * y2_[int(i - 2 * np.pi * sampling_rate * 256 / (fre1 + fre2))]        

    # spectrum of real part
    omega2_ = np.linspace(-fre1 * 3 - fre2 * 3,fre1 * 3 + fre2 * 3,num = 1537)
    y31 = np.zeros(512) #shrink the index in order to simplify calculation
    y3_ = np.zeros(1537)
    for i in range(512):
        y31[i] = y3[i + 256]
    for i in range(512,1024):
        y3_[i] = sampling_rate * y31[i - 512]
    for i in range(512):
        y3_[i] = sampling_rate * y3_[int(i + 2 * np.pi * sampling_rate * 256 / (fre1 + fre2))]
    for i in range(1025,1536):
        y3_[i] = sampling_rate * y3_[int(i - 2 * np.pi * sampling_rate * 256 / (fre1 + fre2))]           
    
    return t_,omega1_,omega2_,y1_,y2_,y3_

def sampling_sinusoid_plot(amplitude = 1,fre1 = np.pi,theta1 = 0,fre2 = np.pi/2,sampling_rate = 1.7):
    """plot the sampled signal above

    Args:
        amplitude (float, optional): [the amplitude of modulating waveform]. Defaults to 1.
        fre1 (float, optional): [the frequency of modulating waveform]. Defaults to np.pi.
        theta1 (float, optional): [the phase of modulating waveform]. Defaults to 0.              
        fre2 (float, optional): [the frequency of carrier waveform]. Defaults to np.pi/2. 
        sampling_rate (float, optional): [the sampling rate of sampling]. Defaults to 1.7.   

    """
    (t,omega1,omega2,y1,y2,y3) = Amplitude_Modulation.AM_sinusoid(amplitude,fre1,theta1,fre2)
    (t_,omega1_,omega2_,y1_,y2_,y3_) = sampling_sinusoid(amplitude,fre1,theta1,fre2,sampling_rate)
    
    #original signal   
    #plot in time domain
    F=MyFigure()
    F.ax1=F.fig.add_subplot(231)
    F.ax1.plot(t,y1)
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

    #sampled signal
    #spectrum of real part
    F.ax4=F.fig.add_subplot(234)
    F.ax4.stem(t_,y1_)
    F.ax4.set_xlabel("$t$")
    F.ax4.set_ylabel("$y(t)$")
    F.ax4.set_title('sampled signal in time domain')

    #spectrum of real part
    F.ax5=F.fig.add_subplot(235)
    F.ax5.plot(omega1_,y2_)
    F.ax5.set_xlabel("$\omega$")
    F.ax5.set_ylabel("$Re\{Y(j\omega)\}$")
    F.ax5.set_title('spectrum of sampled signal-Re')

    #spectrum of imaginary part
    F.ax6=F.fig.add_subplot(236)
    F.ax6.plot(omega2_,y3_)
    F.ax6.set_xlabel("$\omega$")
    F.ax6.set_ylabel("$Im\{Y(j\omega)\}$")
    F.ax6.set_title('spectrum of sampled signal-Im')
    F.fig.subplots_adjust(wspace = 1,hspace = 0.7)
    return F
#if __name__ == "__main__":
#    sampling_sinusoid_plot(theta1=-np.pi/3,fre1=np.pi/2,fre2=2*np.pi)
#    plt.subplots_adjust(wspace = 0.7,hspace = 0.7)
#    plt.show()
