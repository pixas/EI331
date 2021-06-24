from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

seaborn.set(style="whitegrid")
# this function has been tested succsessfully

class MyFigure(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        super(MyFigure,self).__init__(self.fig)

def plot_ct_unit_impulse(amplitude=1, shift=0):
    """plot ct unit impulse function with amplitude and shift from user

    Args:
        amplitude (float, optional): [amplitude of this impulse]. Defaults to 1.
        shift (float, optional): [\delta(t-shift)]. Defaults to 0.
    """

    ax = plt.gca()
    if amplitude > 0:

        plt.ylim(bottom=0, top=amplitude + 4)
    elif amplitude < 0:
        ax.xaxis.tick_top()
        plt.ylim(top=0, bottom=amplitude-4)
    else:
        raise ValueError(
            "The amplitude of CT unit impulse function must be not equal to zero!")
    t = np.arange(shift, shift + 1)
    x_of_t = np.array([amplitude])
    plt.scatter(t, x_of_t, c="r", marker="^")

    plt.plot([shift, shift], [0, amplitude], c="r")
    plt.xlabel("$t$")
    plt.ylabel("$x(t)$")
    # plt.text(shift + 0.005, amplitude, f"{amplitude}")
    plt.title("CT unit impulse function")
    # plt.axis("equal")
    plt.draw()


def plot_ct_unit_step(amplitude=1, shift=0, reverse=False):
    """plot CT unit step function

    Args:
        amplitude (float, optional): [the amplitude of step function]. Defaults to 1.
        shift (float, optional): [offset of step function]. Defaults to 0.
        reverse (bool, optional): [u(-(t-shift)) or not]. Defaults to False.

    Raises:
        ValueError: [amplitude must be not equal to zero]
    """
    ax = plt.gca()
    if amplitude > 0:

        plt.ylim(bottom=0, top=amplitude + 4)
    elif amplitude < 0:
        ax.xaxis.tick_top()
        plt.ylim(top=0, bottom=amplitude-4)
    else:
        raise ValueError(
            "The amplitude of CT unit impulse function must be not equal to zero!")
    t = np.arange(
        shift, shift + 10) if not reverse else np.arange(shift - 9, shift + 1)
    x_of_t = np.ones((10, )) * amplitude
    plt.plot(t, x_of_t, c="r")

    plt.plot([shift, shift], [0, amplitude], c="r")
    plt.xlabel("$t$")
    plt.ylabel("$x(t)$")
    # plt.text(shift + 0.05 * shift, amplitude, f"{amplitude}")
    plt.title("CT unit step function")
    if reverse:
        plt.xlim(right=shift + 5)
    else:
        plt.xlim(left=shift - 5)

    # plt.axis("equal")
    plt.draw()


def plot_ct_real_exponential(amplitude, a):
    """plot CT real exponentialL x(t) = Ce^{at}

    Args:
        amplitude ([float]): [C]
        a ([type]): [a]
    """
    assert amplitude != 0, "The amplitude of CT unit impulse function must be not equal to zero!"
    ax = plt.gca()
    if amplitude > 0:

        plt.ylim(bottom=0, top=amplitude + 4)
    elif amplitude < 0:
        ax.xaxis.tick_top()
        plt.ylim(top=0, bottom=amplitude-4)
    
    t = np.linspace(-3, 3, 100)
    filled_amplitude = amplitude
    filled_a = a 
    if filled_amplitude == -1:
        filled_amplitude = "-"
    elif filled_amplitude == 1:
        filled_amplitude = ""
    if filled_a == -1:
        filled_a = "-"
    elif filled_a == 1:
        filled_a = ""
    x_of_t = amplitude * np.exp(a * t)
    plt.plot(t, x_of_t, c="r")
    plt.xlabel("$t$")
    plt.ylabel("$x(t)$")
    plt.title(f"${filled_amplitude}e^{{{filled_a}t}}$")

    # plt.axis("equal")
    plt.draw()


#exist subplot
def plot_ct_complex_exponential(amplitude, a):
    """plot the ct complex exponential signal, make sure that amplitude and a are both in form of 
    "a + bj"

    Args:
        amplitude ([type]): [C]
        a ([type]): [a]
    """
    F=MyFigure()
    amplitude = str(amplitude)
    a = str(a)
    is_in_amplitude = "j" not in amplitude
    is_in_a = "j" not in a
    # test if j exists in amplitude
    if is_in_amplitude and is_in_a:
        plot_ct_real_exponential(float(amplitude), float(a))
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
    # plt.figure(figsize=(8, 8))
    F.ax1=F.fig.add_subplot(211)
        
    # plt.subplot(2, 1, 1)
    t = np.linspace(-2, 9, 300)
    print(magnitude, omega0, r, theta)
    x_of_t = magnitude * np.exp(r * t) * np.cos(omega0 * t + theta)
    F.ax1.plot(t, x_of_t, c="r", label="CT exponential exponential")
    # plt.plot(t, x_of_t, c="r", label="CT exponential exponential")
    F.ax1.set_xlabel("$t$")
    F.ax1.set_ylabel("$Re{x(t)}$")
    F.ax1.set_title(f"Re{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}t}}$}}")
    F.ax2=F.fig.add_subplot(212)
    #plt.subplot(2, 1, 2)
    y_of_t = magnitude * np.exp(r * t) * np.sin(omega0 * t + theta)
    F.ax2.plot(t, y_of_t, c="r", label="CT exponential exponential")
    F.ax2.set_xlabel("$t$")
    F.ax2.set_ylabel("$Im{x(t)}$")
    F.ax2.set_title(f"Im{{${magnitude:.3}e^{{j{theta:.3}}}\cdot e^{{{a}t}}$}}")
    # plt.title("Imaginary part of $%(magnitude).3fe^{%(theta).3f}e^{%(a).3ft}$")
    F.fig.subplots_adjust(hspace=0.5)
    return F

def plot_rectangle_waveform(amplitude=1, shift=0, T=0):
    """plot periodic waveform signal

    Args:
        amplitude (int, optional): [description]. Defaults to 1.
        shift (int, optional): [description]. Defaults to 0.
        T (int, optional): [period. If it is set to 0, only plot one period figure with span equal to 1]. Defaults to 1.

    Raises:
        ValueError: [The amplitude of waveform must be not equal to zero!]
    """
    amplitude = float(amplitude)
    shift = float(shift)
    T = float(T)
    ax = plt.gca()
    if amplitude > 0:

        plt.ylim(bottom=0, top=amplitude + 4)
    elif amplitude < 0:
        ax.xaxis.tick_top()
        plt.ylim(top=0, bottom=amplitude-4)
    else:
        raise ValueError(
            "The amplitude of waveform must be not equal to zero!")
    if T != 0:
        # plot the aperiodic signal
        t = np.arange(-T / 2 + shift, T / 2 + shift + 0.1, 0.1)
        x_of_t = np.ones_like(t) * amplitude
        for i in range(-2, 3):

            plt.plot(t + (i * 2 * T), x_of_t, c="r")
            plt.plot([-T / 2 + shift + (i * 2 * T), -T / 2 + shift + (i * 2 * T)], [0, amplitude], c="r")
            plt.plot([T / 2 + shift + (i * 2 * T), T / 2 + shift + (i * 2 * T)], [0, amplitude], c="r")
    else:
        t = np.arange(-1 / 2 + shift, 1 / 2 + shift + 0.1, 0.1)
        x_of_t = np.ones_like(t) * amplitude
        plt.plot(t, x_of_t, c="r")
        plt.plot([-1 / 2 + shift, -1 / 2 + shift], [0, amplitude], c="r")
        plt.plot([1 / 2 + shift, 1 / 2 + shift], [0, amplitude], c="r")
    plt.xlabel("$t$")
    plt.ylabel("$x(t)$")

    plt.title("Rectangular waveform")

    plt.draw()
    return

def plot_sampling_function(magnitude=1, scalar=1):
    magnitude = float(magnitude)
    scalar = float(scalar)
    ax = plt.gca()

    filled_magnitude = magnitude
    filled_scalar = scalar
    if filled_magnitude == -1:
        filled_magnitude = "-"
    elif filled_magnitude == 1:
        filled_magnitude = ""
    if filled_scalar == -1:
        filled_scalar = "-"
    elif filled_scalar == 1:
        filled_scalar = ""
    t = np.linspace(-10, 10, 200)
    x_of_t = magnitude * np.sin(scalar * t) / (scalar * t)
    ax.plot(t, x_of_t, c="r")
    ax.set_xlabel("$t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(fr"$Sa(t)={filled_magnitude}\frac{{\sin({filled_scalar}t)}}{{{filled_scalar}t}}$")
    
    plt.draw()
    return

if __name__ == "__main__":
    F=MyFigure()
    F.plot_ct_complex_exponential(1 + 1j , 3 + 1j)
    