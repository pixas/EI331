import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="whitegrid")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4):
        self.fig=Figure(figsize=(width,height))
        super(MyFigure,self).__init__(self.fig)

def ctfs_of_periodic_rectangle_waveform(T1=1, T=2, amplitude=1, N=14) -> np.ndarray:
    """get the fourier series of periodic rectangle waveform

    Args:
        T1 (int, optional): [2T1=width of rectangle waveform]. Defaults to 1.
        T (int, optional): [the period]. Defaults to 2.
        amplitude (int, optional): [the amplitude of this waveform]. Defaults to 1.
        N (int, optional): [how many fourier series to be calculated. ]. Defaults to 14.

    Returns:
        [np.ndarray]: [with shape (2N+1, ) the fourier series array]
    """
    T1 = abs(T1)
    T = abs(T)
    
    assert N > 0, "Must calculate at least one coefficient"
    omega0 = 2 * np.pi / T 
    k = np.arange(-N, N + 1)
    res = np.sin(k * omega0 * T1) / (k * np.pi) * amplitude
    res[N] = 2 * T1 * amplitude / T
    return res

def ctfs_of_cosine_function(theta=0):
    fs = [np.exp(-1j * theta) / 2, 0, np.exp(1j * theta) / 2]
    return np.array(fs)

def ctfs_of_sine_function(theta=0):
    return ctfs_of_cosine_function(theta=theta - np.pi / 2)

def ctfs_of_impulse_train(T, N=14):
    return np.ones(2 * N + 1) / T


    

def plot_ct_nth_partial_sum(fs_array: np.ndarray, T, t_begin=-10, t_end=10, t_number=500) -> None:
    """plot the nth partial sum

    Args:
        fs_array (np.ndarray): [numpy array of fourier series. its length must be 2 * N + 1]
        T ([type]): [period corresponding to the fourier series]
        t_begin (int, optional): [the start of t in the output figure]. Defaults to -10.
        t_end (int, optional): [the end of t in the output figure]. Defaults to 10.
        t_number (int, optional): [sampling points in t]. Defaults to 500.
    """
    F=MyFigure(10,5)
    # plt.style.use("seaborn-whitegrid")
    total_num = fs_array.shape[0]
    N = (total_num - 1) // 2

    t = np.linspace(t_begin, t_end, t_number)
    res = 0
    omega = 2 * np.pi / T
    for i in range(total_num):
        res += fs_array[i] * np.exp(1j * (i - N) * t * omega)
    F.ax1=F.fig.add_subplot(121)
    #fig = plt.figure(figsize=(10, 5))

    F.ax1.plot(t, np.real(res), "r")
    F.ax1.set_title("Real part")
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$Re\{x(t)\}$")
    F.ax2=F.fig.add_subplot(122)
    F.ax2.plot(t, np.imag(res), "r")
    F.ax2.set_title("Imaginary part")
    F.ax2.set_xlabel("$t$")
    F.ax2.set_ylabel("$Im\{x(t)\}$")
    return F

def plot_retangle(T1=1, T=2, amplitude=1, N=14,t_begin=-10, t_end=10, t_number=500):
    fs=ctfs_of_periodic_rectangle_waveform(T1, T, amplitude, N)
    return plot_ct_nth_partial_sum(fs,t_begin, t_end, t_number)

def plot_cosine(theta=0,t_begin=-10, t_end=10, t_number=500):
    fs=ctfs_of_cosine_function(theta)
    return plot_ct_nth_partial_sum(fs,t_begin, t_end, t_number)

def plot_sine(theta=0,t_begin=-10, t_end=10, t_number=500):
    fs=ctfs_of_sine_function(theta)
    return plot_ct_nth_partial_sum(fs,t_begin, t_end, t_number)

def plot_impulse(T, N=14,t_begin=-10, t_end=10, t_number=500):
    fs=ctfs_of_impulse_train(T,N)
    return plot_ct_nth_partial_sum(fs,t_begin, t_end, t_number)
if __name__ == "__main__":
    fs = ctfs_of_sine_function()
    plot_ct_nth_partial_sum(fs, 2, -5, 5)