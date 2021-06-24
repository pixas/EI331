import numpy as np 
import matplotlib.pyplot as plt 
import scipy.signal as sg
import math
import seaborn
seaborn.set(style="whitegrid")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
'''
DT_convolution of any combination 2 typical signals
本文函数名都采用 plotconv_函数1_函数2() 形式
统一参数(m1*f1[n+n1]与m2*f2[n+n2]卷积):
    n1:函数1时移
    m1:函数1模的变化
    n2:函数2时移
    m2:函数2模的变化
    其余特定参数见具体函数注释
函数名称：
    DT unit impulse function：impulse
    DT unit step function: step
    DT Real exponential: real_exp
    DT complex exponential: complex_exp
    DT Sampling function: sample
    DT Rectangle waveform: rectangle
'''
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)
#1
def plotconv_impulse_step(n1=0,m1=1,n2=0,m2=1): 
    '''plot convolution between impulse function and step function

    args:
        n1(int): [time shift of impulse function]. Defaults to 0.
        m1(float,optional): [amplitude of impulse function]. Defaults to 1.
        n2(int): [time shift of step function]. Defaults to 0.
        m2(float,optional): [amplitude of step function]. Defaults to 1.
    '''
    F=MyFigure()
    impulse_y = np.zeros(10)
    impulse_y[0]=m1
    impulse_x=np.arange(n1*(-1),n1*(-1)+10)
    step_y = np.ones(10) * m2
    
    step_x = np.arange((-1)*n2,(-1)*n2+10)
    conv_x = np.arange((-1)*(n1+n2),(-1)*(n1+n2)+10)
    conv_y = np.ones(10) * (m2 * m1)
    
    #待卷积
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(impulse_x,impulse_y,use_line_collection=False)
    # plt.grid(True)
    F.ax1.set_title('unit impulse function')
    F.ax1.set_xlabel('time index n')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(step_x,step_y,use_line_collection=False)
    # plt.grid(True)
    F.ax2.set_title('unit step function')
    F.ax2.set_xlabel('time index n')
    #卷积
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,'-',use_line_collection=True)
    # plt.grid(True)
    F.ax3.set_title('convolution')
    F.ax3.set_xlabel('time index n')
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5) 
    return F
# plotconv_impulse_step()
#2
def plotconv_rectangle_impulse(T1=1,T2=4,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between rectangle waveform and impulse function
    rectangle waveform: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    
    args:
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n1(int): [time shift of rectangle waveform]. Defaults to 0.
        m1(float,optional): [amplitude of rectangle waveform]. Defaults to 1.
        n2(int): [time shift of impulse function]. Defaults to 0.
        m2(float,optional): [amplitude of impulse function]. Defaults to 1.
    raises:
        ValueError: ('The amplitude of waveform must be not equal to 0!')
        ValueError: ('The period must be not less than 0!')
        ValueError: (We must have T1<T2/2 !)
    '''
    F=MyFigure()
    if m1 == 0 or m2==0:
        raise ValueError('The amplitude of waveform must be not equal to 0!')
    if T1<0 or T2<0:
        raise ValueError('The period must be not less than 0!')
    impulse_y = np.zeros(10)
    impulse_y[0]=m2
    impulse_x=np.arange(n2*(-1),n2*(-1)+10)
    if T2==0:
        rectangle_x = np.arange(-T1-2-n1,T1+3-n1)
        rectangle_y = np.zeros(2*T1+5)
        rectangle_y[2:2*T1+3] = m1
        conv_x = np.arange(-T1-2-n1-n2,T1+3-n1-n2)
        conv_y = m2*rectangle_y
    if T2!=0:
        if T1>=T2/2:
            raise ValueError('We must have T1<T2/2 !')
        rectangle_x = np.arange(-T2/2-2*T2-n1,T2/2+1+2*T2-n1)
        rectangle_y = np.zeros(5*T2+1)
        for i in range(0,5):
            rectangle_y[int(T2/2-T1+i*T2):int(T2/2+T1+i*T2+1)] = m1
        
        conv_x = np.arange(-T2/2-2*T2-(n1+n2),T2/2+1+2*T2-(n1+n2))
        conv_y = np.zeros(5*T2+1)
        for i in range(0,5):
            conv_y[int(T2/2-T1+i*T2):int(T2/2+T1+i*T2+1)] = m1*m2
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(impulse_x,impulse_y,use_line_collection=False)
    # plt.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit impulse function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(rectangle_x,rectangle_y,use_line_collection=False)
    # plt.grid(True)
    F.ax2.set_xlabel("time index n")
    F.ax2.set_title("Rectangle waveform")
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    F.ax3.sett_title("convolution")
    # plt.grid(True)
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
    return F
# plotconv_rectangle_impulse(2,2,0,2,-3,-3)
# plotconv_rectangle_impulse(3,8,2,2,-3,-3)
#3
def plotconv_sample_impulse(w=1,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between sampling function and impulse function
    sampling function: x[n] = m1*sin(w*n)/(πn) 0<w<π
    
    args:
        w(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n1(int): [time shift of sampling function]. Defaults to 0.
        m1(float,optional): [amplitude of sampling function]. Defaults to 1.
        n2(int): [time shift of impulse function]. Defaults to 0.
        m2(float,optional): [amplitude of impulse function]. Defaults to 1.
    raises:
        ValueError: ('The amplitude of DT unit impulse function must be not equal to zero!')
        ValueError: (The amplitude of DT sampling function must be not equal to zero!)
        ValueError: (The W must be in (0,pi)!)
    '''
    F=MyFigure()
    if m2 == 0:
        raise ValueError('The amplitude of DT unit impulse function must be not equal to zero!')
    if m1 == 0:
        raise ValueError('The amplitude of DT sampling function must be not equal to zero!')
    if w<=0 or w>=math.pi:
        raise ValueError("The W must be in (0,pi)!")
    impulse_y = np.zeros(10)
    impulse_y[0]=m2
    impulse_x=np.arange(n2*(-1),n2*(-1)+10)
    T = int((2*math.pi)/w)
    true_sample_x = np.arange(-5*T,5*T+1) #实际采用的x值
    sample_x = np.arange(-5*T-n1,5*T+1-n1) #展示的平移之后的x值
    sample_y = np.zeros(10*T+1)
    # sample_y = m1 * np.sin(w * true_sample_x) / (np.pi * true_sample_x)
    for i in range(10*T+1):
        if true_sample_x[i]==0:
            sample_y[i] = m1*w/(math.pi)
        if true_sample_x[i]!=0:
            sample_y[i] = m1*np.sin(w*true_sample_x[i])/(math.pi*true_sample_x[i])
    
    conv_x = np.arange(-5*T-n1-n2,5*T+1-n1-n2)
    conv_y = m2*sample_y
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(impulse_x,impulse_y,use_line_collection=False)
    # plt.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit impulse function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(sample_x,sample_y,use_line_collection=False)
    # plt.grid(True)
    F.ax2.set_xlabel("time index n")
    F.ax2.set_title(fr"$Sa[n]={m1}\frac{{\sin({w}n)}}{{\pi n}}$")
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title("convolution")
    # plt.grid(True)
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
    return F
#plotconv_sample_impulse(n2=1)
#4
def plotconv_real_exp_impulse(a=1,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between real exponential and impulse function
    real exponential: x[n] =  Ce^{an}
    
    args:
        a(float): []. Defaults to 1.
        n1(int): [time shift of real exponential]. Defaults to 0.
        m1(float,optional): [amplitude of real exponential]. Defaults to 1.
        n2(int): [time shift of impulse function]. Defaults to 0.
        m2(float,optional): [amplitude of impulse function]. Defaults to 1.
    '''
    assert m1!=0 and m2!=0,"The amplitude must be not equal to zero!"
    true_real_exp_x = np.arange(-2, 6)
    real_exp_x = np.arange(-2-n1,6-n1)

    real_exp_y = m1 * np.exp(a * true_real_exp_x)
    print(real_exp_y)
    impulse_y = np.zeros(10)
    impulse_y[0]=m2
    impulse_x=np.arange(-n2, -n2 + 10)
    conv_x = np.arange(-2-n1-n2, 6-n1-n2)
    conv_y = m2 * real_exp_y
    F=MyFigure()
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(impulse_x,impulse_y,use_line_collection=False)
    # plt.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit impulse function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(real_exp_x,real_exp_y,use_line_collection=False)
    # plt.grid(True)
    F.ax2.set_xlabel("time index n")
    if n1>0:
        F.ax2.set_title(f"${m1}e^{{{a}(n+{n1})}}$")
    if n1==0:
        F.ax2.set_title(f"${m1}e^{{{a}n}}$")
    if n1<0:
        F.ax2.set_title(f"${m1}e^{{{a}(n{n1})}}$")
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title("convolution")
    # plt.grid(True)
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
    return F
# plotconv_real_exp_impulse(2,2,-2,3,3)
# plotconv_real_exp_impulse()
#5
def plotconv_complex_exp_impulse(a,m1,n1=0,n2=0,m2=1):
    """plot convolution between complex exponential and impulse function
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    
    args:
        a(): [a]. 
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(): [amplitude of complex exponential]. 
        n2(int): [time shift of impulse function]. Defaults to 0.
        m2(float,optional): [amplitude of impulse function]. Defaults to 1.
    """
    amplitude = str(m1)
    a = str(a)
    is_in_amplitude = "j" not in amplitude
    is_in_a = "j" not in a
    # test if j exists in amplitude
    if is_in_amplitude and is_in_a:
        plotconv_real_exp_impulse(float(a),n1,float(amplitude),n2,m2)
        return
    elif is_in_amplitude and not is_in_a:
        complex_a = eval(a)
        r = complex_a.real
        omega0 = complex_a.imag
        theta = 0.0
        magnitude = float(amplitude)
    elif not is_in_amplitude and is_in_a:
        complex_amplitude = eval(amplitude)
        r = a
        omega0 = 0
        magnitude = (complex_amplitude.real ** 2 + complex_amplitude.imag ** 2) ** 0.5
        theta = math.atan(complex_amplitude.imag / (complex_amplitude.real + 1e-10))
    else:
        complex_amplitude = eval(amplitude)
        complex_a = eval(a)
        r = complex_a.real
        omega0 = complex_a.imag
        magnitude = (complex_amplitude.real ** 2 + complex_amplitude.imag ** 2) ** 0.5
        theta = math.atan(complex_amplitude.imag / (complex_amplitude.real + 1e-10))
    r = float(r)
    omega0 = float(omega0)
    
    true_complex_exp_x = np.arange(-2,10)
    complex_exp_x = np.arange(-2-n1,10-n1)
    #print(magnitude, omega0, r, theta)
    real_of_x = magnitude * np.exp(r * true_complex_exp_x) * np.cos(omega0 * true_complex_exp_x + theta)
    img_of_x = magnitude * np.exp(r * true_complex_exp_x) * np.sin(omega0 * true_complex_exp_x + theta)
    impulse_y = np.zeros(10)
    impulse_y[0]=m2
    impulse_x=np.arange(n2*(-1),n2*(-1)+10)
    conv_x = np.arange(-2-n1-n2,10-n1-n2)
    real_of_conv = m2*real_of_x
    img_of_conv = m2*img_of_x
    F=MyFigure(8,8)
    F.ax1=F.fig.add_subplot(231)
    F.ax1.stem(impulse_x,impulse_y,use_line_collection=False)
    F.ax1.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit impulse function')
    F.ax2=F.fig.add_subplot(232)
    F.ax2.stem(complex_exp_x, real_of_x,use_line_collection=False)
    F.ax2.set_xlabel("time index n")
    if n1==0:
        F.ax2.set_title(f"Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}n}}$}}")
    if n1>0:
        F.ax2.set_title(f"Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n+{n1})}}$}}")
    if n1<0:
        F.acx2.set_title(f"Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n{n1})}}$}}")
    F.ax3=F.fig.add_subplot(233)
    F.ax3.stem(complex_exp_x, img_of_x,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    if n1==0:
        F.ax3.set_title(f"Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}n}}$}}")
    if n1>0:
        F.ax3.set_title(f"Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n+{n1})}}$}}")
    if n1<0:
        F.ax3.set_title(f"Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n{n1})}}$}}")
    # plt.title(f"Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}n}}$}}")
    # plt.title("Imaginary part of $%(magnitude).3fe^{%(theta).3f}e^{%(a).3ft}$")
    F.ax4=F.fig.add_subplot(223)
    F.ax4.stem(conv_x, real_of_conv,use_line_collection=False)
    F.ax4.set_xlabel("time index n")
    if n1+n2==0:
        F.ax4.set_title(f"convolution:Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}n}}$}}")
    if n1+n2>0:
        F.ax4.set_title(f"convolution:Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n+{n1+n2})}}$}}")
    if n1+n2<0:
        F.ax4.set_title(f"convolution:Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n{n1+n2})}}$}}")
    F.ax5=F.fig.add_subplot(224)
    F.ax5.stem(conv_x, img_of_conv,use_line_collection=False)
    F.ax5.set_xlabel("time index n")
    if n1+n2==0:
        F.ax5.set_title(f"convolution:Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}n}}$}}")
    if n1+n2>0:
        F.ax5.set_title(f"convolution:Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n+{n1+n2})}}$}}")
    if n1+n2<0:
        F.ax5.set_title(f"convolution:Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}(n{n1+n2})}}$}}")
    F.fig.subplots_adjust(hspace=0.5)
    return F
# plotconv_complex_exp_impulse(1+2j,2+3j,n1=3,n2=-2)
#周期方波卷采样函数，当且仅当周期方波N=1时，卷积为周期方波本身
#6
def plotconv_impulse_impulse(n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between impulse function and impulse function
    
    args:
        n1(int): [time shift of impulse function1]. Defaults to 0.
        m1(float,optional): [amplitude of impulse function1]. Defaults to 1.
        n2(int): [time shift of impulse function2]. Defaults to 0.
        m2(float,optional): [amplitude of impulse function2]. Defaults to 1.
    '''
    F=MyFigure()
    impulse1_y = np.zeros(10)
    impulse1_y[0]=m1
    impulse1_x=np.arange(n1*(-1),n1*(-1)+10)
    impulse2_y = np.zeros(10)
    impulse2_y[0]=m2
    impulse2_x=np.arange(n2*(-1),n2*(-1)+10)
    conv_y = m1*impulse2_y
    conv_x = np.arange((n2+n1)*(-1),(n2+n1)*(-1)+10)
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(impulse1_x,impulse1_y,use_line_collection=False)
    F.ax1.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit impulse function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(impulse2_x,impulse2_y,use_line_collection=False)
    F.ax2.grid(True)
    F.ax2.set_xlabel("time index n")
    F.ax2.set_title('unit impulse function')
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    # plt.stem(conv_x,conv_y,linefmt='-',markerfmt='o',basefmt='-',color='w')
    # markerline, stemlines, baseline = plt.stem(conv_x,conv_y,linefmt='-',markerfmt='o',basefmt='-',label='TestStem')
    # plt.setp(baseline,color='w')
    F.ax3.grid(True)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title('convolution')
    return F
# plotconv_impulse_impulse()
#7
def plotconv_step_step(n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between step function and step function
    
    args:
        n1(int): [time shift of steo function1]. Defaults to 0.
        m1(float,optional): [amplitude of step function1]. Defaults to 1.
        n2(int): [time shift of step function2]. Defaults to 0.
        m2(float,optional): [amplitude of step function2]. Defaults to 1.
    '''
    step1_y = np.zeros(10)
    step1_y[:]=m1
    step1_x = np.arange((-1)*n1,(-1)*n1+10)
    step2_y = np.zeros(10)
    step2_y[:]=m2
    step2_x = np.arange((-1)*n2,(-1)*n2+10)
    true_conv_x = np.arange(0,10)
    conv_x = np.arange((-1)*(n1+n2),(-1)*(n1+n2)+10)
    conv_y = true_conv_x+1
    F=MyFigure()
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(step1_x,step1_y,use_line_collection=False)
    F.ax1.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit step function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(step2_x,step2_y,use_line_collection=False)
    F.ax2.grid(True)
    F.ax2.set_xlabel("time index n")
    F.ax2.set_title('unit step function')
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.grid(True)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title('convolution')
    return F
# plotconv_step_step()
#8
def plotconv_real_exp_step(a=1,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between real exponential and step function
    real exponential: x[n] =  Ce^{an}
    
    args:
        a(float): []. Defaults to 1.
        n1(int): [time shift of real exponential]. Defaults to 0.
        m1(float,optional): [amplitude of real exponential]. Defaults to 1.
        n2(int): [time shift of step function]. Defaults to 0.
        m2(float,optional): [amplitude of step function]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    assert m1!=0 and m2!=0,"The amplitude must be not equal to zero!"
    if a==0:
        raise OverflowError('The convolution is divergent !')
    step_y = np.zeros(10)
    step_y[:]=m2
    step_x = np.arange((-1)*n2,(-1)*n2+10)
    true_real_exp_x = np.arange(-2,6)
    real_exp_x = np.arange(-2-n1,6-n1)
    real_exp_y = m1*np.exp(a*true_real_exp_x)
    conv_x = np.arange(-2-n1-n2,6-n1-n2)
    conv_y = np.zeros(8)
    for i in range(8):
        conv_y[i] = m1*m2*np.exp(a*true_real_exp_x[i])/(1-np.exp(-a))
    F=MyFigure()
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(step_x,step_y,use_line_collection=False)
    F.ax1.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('unit step function')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(real_exp_x,real_exp_y,use_line_collection=False)
    F.ax2.grid(True)
    F.ax2.set_xlabel("time index n")
    if n1>0:
        F.ax2.set_title(f"${m1}e^{{{a}(n+{n1})}}$")
    if n1==0:
        F.ax2.set_title(f"${m1}e^{{{a}n}}$")
    if n1<0:
        F.ax2.set_title(f"${m1}e^{{{a}(n{n1})}}$")
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title("convolution")
    F.ax3.grid(True)
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
    return F
# plotconv_real_exp_step(2,2,2,-3,-3)
#9
def plotconv_real_exp_real_exp(a1=1,a2=1,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between real exponential and real exponential
    real exponential: x[n] =  Ce^{an}
    
    args:
        a1(float): []. Defaults to 1.
        n1(int): [time shift of real exponential]. Defaults to 0.
        m1(float,optional): [amplitude of real exponential]. Defaults to 1.
        a2(float): []. Defaults to 1.
        n2(int): [time shift of real exponential]. Defaults to 0.
        m2(float,optional): [amplitude of real exponential]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent !')
# plotconv_real_exp_real_exp()
#10
def plotconv_complex_exp_complex_exp(a,m1,b,m2,n1=0,n2=0):
    '''plot convolution between complex exponential and complex exponential
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    
    args:
        a1(float): [].
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(float,optional): [amplitude of complex exponential]. 
        b(float): []. 
        n2(int): [time shift of complex exponential]. Defaults to 0.
        m2(float,optional): [amplitude of complex exponential]. 
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent !')
# plotconv_complex_exp_complex_exp(1+2j,3+4j,1+2j,3+4j)  
#11
def plotconv_complex_exp_real_exp(a,m1,n1=0,b=1,n2=0,m2=1):
    '''plot convolution between complex exponential and real exponential
    real exponential: x[n] =  Ce^{an}
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    
    args:
        a(float): [].
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(float,optional): [amplitude of complex exponential]. 
        b(float): []. Defaults to 1.
        n2(int): [time shift of real exponential]. Defaults to 0.
        m2(float,optional): [amplitude of real exponential]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_complex_exp_real_exp(1+2j,3+4j)
#12
def plotconv_complex_exp_step(a,m1,n1=0,n2=0,m2=1):
    '''plot convolution between complex exponential and step function
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    
    args:
        a(float): [].
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(): [amplitude of complex exponential]. 
        n2(int): [time shift of step function]. Defaults to 0.
        m2(float,optional): [amplitude of step function]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_complex_exp_step(1+2j,3+4j)
#13
def plotconv_rectangle_step(T1=1,T2=4,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between rectangle waveform and step function
    rectangle waveform: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    
    args:
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n1(int): [time shift of rectangle waveform]. Defaults to 0.
        m1(float,optional): [amplitude of rectangle waveform]. Defaults to 1.
        n2(int): [time shift of step function]. Defaults to 0.
        m2(float,optional): [amplitude of step function]. Defaults to 1.
    raises:
        ValueError: ('The amplitude of waveform must not be equal to 0!')
        ValueError: ('The period must be not less than 0!')
        OverflowError: ('The convolution is divergent!')
    '''
    if m1==0 or m2==0:
        raise ValueError('The amplitude of waveform must not be equal to 0 !')
    if T1<0 or T2<0:
        raise ValueError('The period must be not less than 0!')
    if T2>0:
        raise OverflowError('The convolution is divergent!')
    if T2==0:
        step_y = np.zeros(10)
        step_y[:]=m2
        step_x = np.arange((-1)*n2,(-1)*n2+10)
        rectangle_x = np.arange(-T1-2-n1,T1+3-n1)
        rectangle_y = np.zeros(2*T1+5)
        rectangle_y[2:2*T1+3] = m1
        conv_x = np.arange(-T1-2-n1-n2,T1+3-n2-n1)
        conv_y = np.zeros(2*T1+5)
        for i in range(2*T1+1):
            conv_y[i+2] = (i+1)*m1*m2
        F=MyFigure()
        F.ax1=F.fig.add_subplot(221)
        F.ax1.stem(step_x,step_y,use_line_collection=False)
        F.ax1.grid(True)
        F.ax1.set_xlabel("time index n")
        F.ax1.set_title('unit step function')
        F.ax2=F.fig.add_subplot(222)
        F.ax2.stem(rectangle_x,rectangle_y,use_line_collection=False)
        F.ax2.grid(True)
        F.ax2.set_xlabel("time index n")
        F.ax2.set_title("Rectangle waveform")
        F.ax3=F.fig.add_subplot(212)
        F.ax3.stem(conv_x,conv_y,use_line_collection=False)
        F.ax3.set_xlabel("time index n")
        F.ax3.set_title("convolution")
        F.ax3.grid(True)
        F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
        return F
# plotconv_rectangle_step(T2=0)
# plotconv_rectangle_step()
#14
def plotconv_real_exp_sample(a=1,n1=0,m1=1,w=1,n2=0,m2=1):
    '''plot convolution between real exponential and sampling function
    real exponential: x[n] =  Ce^{an}
    sampling function: [x[n] = m1*sin(w*n)/(πn) 0<w<π].
    
    args:
        a(float): []. Defaults to 1.
        n1(int): [time shift of real exponential]. Defaults to 0.
        m1(float,optional): [amplitude of real exponential]. Defaults to 1.
        w(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n2(int): [time shift of sampling function]. Defaults to 0.
        m2(float,optional): [amplitude of sampling function]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_real_exp_sample()
#15
def plotconv_real_exp_rectangle(a=1,n1=0,m1=1,T1=1,T2=4,n2=0,m2=1):
    '''plot convolution between real exponential and rectangle waveform
    real exponential: x[n] =  Ce^{an}
    rectangle waveform: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    
    args:
        a(float): []. Defaults to 1.
        n1(int): [time shift of real exponential]. Defaults to 0.
        m1(float,optional): [amplitude of real exponential]. Defaults to 1.
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n2(int): [time shift of rectangle waveform]. Defaults to 0.
        m2(float,optional): [amplitude of rectangle waveform]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_real_exp_rectangle()
#16
def plotconv_complex_exp_sample(a,m1,n1=0,w=1,n2=0,m2=1):
    '''plot convolution between complex exponential and sampling function
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    sampling function: [x[n] = m1*sin(w*n)/(πn) 0<w<π]. 
    
    args:
        a(float): []. 
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(): [amplitude of complex exponential].
        w(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n2(int): [time shift of sampling function]. Defaults to 0.
        m2(float,optional): [amplitude of sampling function]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_complex_exp_sample(1+2j,3+4j)
#17
def plotconv_complex_exp_rectangle(a,m1,n1=0,T1=1,T2=4,n2=0,m2=1):
    '''plot convolution between complex exponential and rectangle waveform
    The complex exponential signal, make sure that m1 and a are both in form of "a + bj"
    rectangle waveform: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    
    args:
        a(float): []. 
        n1(int): [time shift of complex exponential]. Defaults to 0.
        m1(): [amplitude of complex exponential]
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n2(int): [time shift of rectangle waveform]. Defaults to 0.
        m2(float,optional): [amplitude of rectangle waveform]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_complex_exp_rectangle(1+2j,3+4j)
#18
def plotconv_sample_sample(w1=1,n1=0,m1=1,w2=1,n2=0,m2=1):
    '''plot convolution between sampling function and sampling function
    sampling function: [x[n] = m*sin(w*n)/(πn) 0<w<π]. 
    
    args:
        w1(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n1(int): [time shift of sampling function1]. Defaults to 0.
        m1(float,optional): [amplitude of sampling function1]. Defaults to 1.
        w2(float.optional): [x[n] = m2*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n2(int): [time shift of sampling function2]. Defaults to 0.
        m2(float,optional): [amplitude of sampling function2]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
    '''
    raise OverflowError('The convolution is divergent!')
# plotconv_sample_sample()
#19
def plotconv_sample_step(n=0,accu=0.00001,w=1,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between sampling function and step function
    sampling function: [x[n] = m1*sin(w*n)/(πn) 0<w<π]. 
    since the convolution is divergent, we can have the value with corresponding accuracy, such as 0.000001
    args:
        n(int): [the value of time index n]. Defaults to 0
        accu(float,optional) :[the corresponding accuracy] Defaults to 0.00001
        w(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n1(int): [time shift of sampling function]. Defaults to 0.
        m1(float,optional): [amplitude of sampling function]. Defaults to 1.
        n2(int): [time shift of step function]. Defaults to 0.
        m2(float,optional): [amplitude of step function]. Defaults to 1.
    raises:
        ValueError: ('The accuracy must be larger than 0 !')
        ValueError: ('The amplitude of DT sampling function must be not equal to zero!')
        ValueError: ("The W must be in (0,pi)!")
        ValueError: ('The accuracy is too large !')
    '''
    if accu<=0:
        raise ValueError('The accuracy must be larger than 0 !')
    if m1==0 or m2==0:
        raise ValueError('The amplitude of DT sampling function must be not equal to zero!')
    if w<=0 or w>=math.pi:
        raise ValueError("The W must be in (0,pi)!")
    #由于有π的限制，我们需对π保留一定小数点后位数
    show_n = n
    n = n+n1+n2
    num = 0 
    test_accu = accu
    while test_accu<1:
        test_accu *= 10
        num += 1
    # print(num)
    pi = round(math.pi,num)
    # print(pi)
    if abs(m1*m2*w/pi)<=accu:
        raise ValueError('The accuracy is too large !')
    tmp = -1
    while abs(m1*m2*np.sin(w*tmp)/(pi*tmp))>=accu:
        tmp -= 1
    if n<0:
        if tmp+1>n:
            raise ValueError('The accuracy is too large !')
        if tmp+1==n:
            conv = m1*m2*np.sin(w*n)/(pi*n)
        if tmp+1<n:
            conv=0
            for i in range(tmp+1,n+1):
                conv += m1*m2*np.sin(w*i)/(pi*i)
            conv = round(conv,num)
    if n==0:
        if tmp+1>n:
            raise ValueError('The accuracy is too large !')
        if tmp+1==n:
            conv = m1*m2*w/(pi)
            conv = round(conv,num)
        if tmp+1<n:
            conv=0
            for i in range(tmp+1,0):
                conv += m1*m2*np.sin(w*i)/(pi*i)
            conv += m1*m2*w/(pi)
            conv = round(conv,num)
    if n>0:
        if tmp+1>n:
            raise ValueError('The accuracy is too large !')
        if tmp+1==n:
            conv = m1*m2*np.sin(w*n)/(pi*n)
            conv = round(conv,num)
        if 0<tmp+1<n:
            conv=0
            for i in range(tmp+1,n+1):
                conv += m1*m2*np.sin(w*i)/(pi*i)
            conv = round(conv,num)
        if tmp+1<=0:
            conv = 0
            for i in range(tmp+1,0):
                conv += m1*m2*np.sin(w*i)/(pi*i)
            conv += m1*m2*w/(pi)
            for i in range(1,n+1):
                conv += m1*m2*np.sin(w*i)/(pi*i)
            conv = round(conv,num)
    # print(conv)
    return ('conv[{}] = {} with accuracy = {}'.format(show_n,conv,accu))
    
# plotconv_sample_step()
# plotconv_sample_step(n=3,accu=0.000001)
# plotconv_sample_step(accu=1)
#20
def plotconv_rectangle_rectangle(T1=1,T2=0,T3=1,T4=0,n1=0,m1=1,n2=0,m2=1):
    '''plot convolution between rectangle waveform1 and rectangle waveform2
    rectangle waveform1: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    rectangle waveform2: x = m2 when |x|<=T3, x = 0 when |x|<T4/2
    
    args:
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        T3(int): [x = m2 when |x|<=T3]. Defaults to 1.
        T4(int): [x = 0 when |x|<T4/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n1(int): [time shift of rectangle waveform1]. Defaults to 0.
        m1(float,optional): [amplitude of rectangle waveform1]. Defaults to 1.
        n2(int): [time shift of rectangle waveform2]. Defaults to 0.
        m2(float,optional): [amplitude of rectangle waveform2]. Defaults to 1.
    raises:
        OverflowError: ('The convolution is divergent !')
        ValueError: ('The period must be even !')
        ValueError: ('The amplitude of waveform must be not equal to 0!')
        ValueError: ('The period must be not less than 0!')
        ValueError: ('We must have T3<T4/2 !')
    '''
    if T2%2!=0 or T4%2!=0:
        raise ValueError('The period must be even !')
    if m1 == 0 or m2==0:
        raise ValueError('The amplitude of waveform must be not equal to 0!')
    if T1<0 or T2<0 or T3<0 or T4<0:
        raise ValueError('The period must be not less than 0!')
    if T2!=0 and T4!=0:
        raise OverflowError('The convolution is divergent !')
    if T2==0 and T4==0:
        rectangle1_x = np.arange(-T1-2-n1,T1+3-n1)
        rectangle1_y = np.zeros(2*T1+5)
        rectangle1_y[2:2*T1+3] = m1
        rectangle2_x = np.arange(-T3-2-n2,T3+3-n2)
        rectangle2_y = np.zeros(2*T3+5)
        rectangle2_y[2:2*T3+3] = m2
        conv_x = np.arange(-T1-T3-n1-n2,T1+T3-n1-n2+1)
        conv_y = np.zeros(1+2*(T1+T3))
        if T1<=T3:
            for i in range(2*T1):
                conv_y[i] = (i+1)*m1*m2
            conv_y[2*T1:2*T3+1] = (2*T1+1)*m1*m2
            for i in range(2*T3+1,1+2*(T1+T3)):
                conv_y[i] = (2*(T1+T3)-i+1)*m1*m2
        if T1>T3:
            for i in range(2*T3):
                conv_y[i] = (i+1)*m1*m2
            conv_y[2*T3:2*T1+1] = (2*T3+1)*m1*m2
            for i in range(2*T1+1,1+2*(T1+T3)):
                conv_y[i] = (2*(T1+T3)-i+1)*m1*m2
    if T2!=0 and T4==0:
        T2,T4 = T4,T2
        T1,T3 = T3,T1
        n1,n2 = n2,n1
        m1,m2 = m2,m1
    if T2==0 and T4!=0:
        if T3>=T4/2:
            raise ValueError('We must have T3<T4/2 !')
        rectangle1_x = np.arange(-T1-2-n1,T1+3-n1)
        rectangle1_y = np.zeros(2*T1+5)
        rectangle1_y[2:2*T1+3] = m1
        rectangle2_x = np.arange(-T4/2-2*T4-n2,T4/2+1+2*T4-n2)
        rectangle2_y = np.zeros(5*T4+1)
        for i in range(0,5):
            rectangle2_y[int(T4/2-T3+i*T4):int(T4/2+T3+i*T4+1)] = m2
        if (T1+T3)<T4/2:
            gap = int((T4/2)-T3-T1)
            conv_x = np.arange(-T4-T4/2-n1-n2,-n1-n2+1+T4+T4/2)
            conv_y = np.zeros(1+3*(T4))
            conv_y1 = np.zeros(1+3*(T4))
            conv_y2 = np.zeros(1+3*(T4))
            conv_y3 = np.zeros(1+3*(T4))
            if T1<=T3:
                for i in range(2*T1):
                    conv_y1[int(i+gap)] = (i+1)*m1*m2
                conv_y1[int(2*T1+gap):int(2*T3+1+gap)] = (2*T1+1)*m1*m2
                for i in range(2*T3+1,1+2*(T1+T3)):
                    conv_y1[int(i+gap)] = (2*(T1+T3)-i+1)*m1*m2
            if T1>T3:
                for i in range(2*T3):
                    conv_y1[i+gap] = (i+1)*m1*m2
                conv_y1[2*T3+gap:2*T1+1+gap] = (2*T3+1)*m1*m2
                for i in range(2*T1+1,1+2*(T1+T3)):
                    conv_y1[i+gap] = (2*(T1+T3)-i+1)*m1*m2
            for j in range(gap,gap+2*(T1+T3)+1):
                conv_y2[j+T4] = conv_y1[j]
                conv_y3[j+2*T4] = conv_y1[j]
            for k in range(3*T4+1):
                conv_y[k] = conv_y1[k]+conv_y2[k]+conv_y3[k]
        if (T1+T3)>=T4/2:
            conv_x = np.arange(-3*(T1+T3)-n1-n2,-n1-n2+1+3*(T1+T3))
            conv_y = np.zeros(1+6*(T1+T3))
            conv_y1 = np.zeros(1+6*(T1+T3))
            conv_y2 = np.zeros(1+6*(T1+T3))
            conv_y3 = np.zeros(1+6*(T1+T3))
            gap = int(2*(T1+T3))
            if T1<=T3:
                for i in range(2*T1):
                    conv_y1[int(i+gap)] = (i+1)*m1*m2
                conv_y1[int(2*T1+gap):int(2*T3+1+gap)] = (2*T1+1)*m1*m2
                for i in range(2*T3+1,1+2*(T1+T3)):
                    conv_y1[int(i+gap)] = (2*(T1+T3)-i+1)*m1*m2
            if T1>T3:
                for i in range(2*T3):
                    conv_y1[i+gap] = (i+1)*m1*m2
                conv_y1[2*T3+gap:gap+2*T1+1] = (2*T3+1)*m1*m2
                for i in range(2*T1+1,1+2*(T1+T3)):
                    conv_y1[i+gap] = (2*(T1+T3)-i+1)*m1*m2
            for j in range(gap,gap+2*(T1+T3)+1):
                conv_y2[j-T4] = conv_y1[j]
                conv_y3[j+T4] = conv_y1[j]
            for k in range(1+6*(T1+T3)):
                conv_y[k] = conv_y1[k]+conv_y2[k]+conv_y3[k]
    F=MyFigure()
    F.ax1=F.fig.add_subplot(221)
    F.ax1.stem(rectangle1_x,rectangle1_y,use_line_collection=False)
    F.ax1.grid(True)
    F.ax1.set_xlabel("time index n")
    F.ax1.set_title('Rectangle waveform 1')
    F.ax2=F.fig.add_subplot(222)
    F.ax2.stem(rectangle2_x,rectangle2_y,use_line_collection=False)
    F.ax2.grid(True)
    F.ax2.set_xlabel("time index n")
    F.ax2.set_title("Rectangle waveform 2")
    F.ax3=F.fig.add_subplot(212)
    F.ax3.stem(conv_x,conv_y,use_line_collection=False)
    F.ax3.set_xlabel("time index n")
    F.ax3.set_title("convolution")
    F.ax3.grid(True)
    F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
    return F
#plotconv_rectangle_rectangle(T2=4,T4=6)
#plotconv_rectangle_rectangle(T4=8,T2=0,T1=2,T3=1)
# plotconv_rectangle_rectangle(T4=4,T2=0,T1=2,T3=1)
# plotconv_rectangle_rectangle(T4=0,T2=0,T1=2,T3=1)
def plotconv_rectangle_sample(T1=1,T2=4,n1=0,m1=1,w=1,n2=0,m2=1):
    '''plot convolution between rectangle waveform and sampling function
    rectangle waveform: x = m1 when |x|<=T1, x = 0 when |x|<T2/2
    sampling function: x[n] = m1*sin(w*n)/(πn) 0<w<π

    args:
        T1(int): [x = m1 when |x|<=T1]. Defaults to 1.
        T2(int): [x = 0 when |x|<T2/2,If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 4.
        n1(int): [time shift of rectangle waveform]. Defaults to 0.
        m1(float,optional): [amplitude of rectangle waveform]. Defaults to 1.
        w(float.optional): [x[n] = m1*sin(w*n)/(πn) 0<w<π]. Defaults to 1.
        n2(int): [time shift of sampling function]. Defaults to 0.
        m2(float,optional): [amplitude of sampling function]. Defaults to 1.
    raises:
        ValueError: ('The amplitude of waveform must be not equal to 0!')
        ValueError: ('The period must be not less than 0!')
        ValueError: (We must have T1<T2/2 !)
        ValueError: (The amplitude of DT sampling function must be not equal to zero!)
        ValueError: (The W must be in (0,pi)!)
        OverflowError('The convolution is divergent !')
    '''
    if m1 == 0 or m2==0:
        raise ValueError('The amplitude of waveform must be not equal to 0!')
    if T1<0 or T2<0:
        raise ValueError('The period must be not less than 0!')
    if m1 == 0:
        raise ValueError('The amplitude of DT sampling function must be not equal to zero!')
    if w<=0 or w>=math.pi:
        raise ValueError("The W must be in (0,pi)!")
    if T2!=0:
        raise OverflowError('The convolution is divergent !')
    if T2==0:
        rectangle_x = np.arange(-T1-2-n1,T1+3-n1)
        rectangle_y = np.zeros(2*T1+5)
        rectangle_y[2:2*T1+3] = m1
        T = int((2*math.pi)/w)
        true_sample_x = np.arange(-5*T,5*T+1) #实际采用的x值
        sample_x = np.arange(-5*T-n2,5*T+1-n2) #展示的平移之后的x值
        sample_y = np.zeros(10*T+1)
        # sample_y = m1 * np.sin(w * true_sample_x) / (np.pi * true_sample_x)
        for i in range(10*T+1):
            if true_sample_x[i]==0:
                sample_y[i] = m2*w/(math.pi)
            if true_sample_x[i]!=0:
                sample_y[i] = m2*np.sin(w*true_sample_x[i])/(math.pi*true_sample_x[i])
        true_conv_x = np.arange(-5,6)
        conv_x = np.arange(-5-n1-n2,6-n1-n2)
        conv_y = np.zeros(11)
        for i in range(11):
            move = true_conv_x[i]
            sum = 0
            for j in range(-T1+move,T1+1+move):
                if j==0:
                    sum += m1*m2*w/(math.pi)
                if j!=0:
                    sum += m1*m2*np.sin(w*j)/(math.pi*j)
            conv_y[i] = sum
        F=MyFigure()
        F.ax1=F.fig.add_subplot(221)
        F.ax1.stem(rectangle_x,rectangle_y,use_line_collection=False)
        # plt.grid(True)
        F.ax1.set_xlabel("time index n")
        F.ax1.set_title('rectangle waveform')
        F.ax2=F.fig.add_subplot(222)
        F.ax2.stem(sample_x,sample_y,use_line_collection=False)
        # plt.grid(True)
        F.ax2.set_xlabel("time index n")
        F.ax2.set_title(fr"$Sa[n]={m1}\frac{{\sin({w}n)}}{{\pi n}}$")
        F.ax3=F.fig.add_subplot(212)
        F.ax3.stem(conv_x,conv_y,use_line_collection=False)
        F.ax3.set_xlabel("time index n")
        F.ax3.set_title("convolution")
        # plt.grid(True)
        F.fig.subplots_adjust(top=0.9, wspace=0.4, hspace=0.5)  
        return F