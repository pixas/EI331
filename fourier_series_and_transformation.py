import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import warnings
import seaborn
seaborn.set(style="whitegrid")
# seaborn.lineplot()


def fourier_transform_aperiodic_rectangle_waveform(T1=2, amplitude=1, omega_begin=-30, omega_end = 30, omega_number=200):
    omega = np.linspace(omega_begin, omega_end, omega_number)
    spectrum = 2 * amplitude * np.sin(omega * T1) / omega
    plt.plot(omega, spectrum)
    plt.xlabel("$\omega$")
    plt.ylabel(r"$X(j\omega)$")
    filled_amplitude = amplitude
    if filled_amplitude == -1:
        filled_amplitude = "-"
    elif filled_amplitude == 1:
        filled_amplitude = ""
    plt.title(fr"$2{filled_amplitude}\frac{{\sin({T1}\omega)}}{{\omega}}$")
    plt.draw()
    return


def plot_periodic_unit_impulse_spectrum(N=1, amplitude=1, cycles=5):
    # time_domain_signal = np.zeros((2 * cycles * N + 1, ))
    # idx = np.arange(0, 2 * cycles * N + 1, N)
    # time_domain_signal[idx] = amplitude
    
    freq_domain_N = 2 * np.pi / N
    freq_domain_amplitude = 2 * np.pi / N
    
    # freq_range = [freq_domain_N * i for i in range(-cycles, cycles + 1, 1)]
    freq_range = np.arange(-cycles * freq_domain_N, (cycles + 1) * freq_domain_N, freq_domain_N)
    freq_value = np.ones_like(freq_range) * freq_domain_amplitude
    # fig = plt.figure(figsize=(7, 7))
    if amplitude > 0:

        plt.ylim(bottom=0, top=freq_domain_amplitude + 4)
    total_num = freq_range.shape[0]
    for i in range(total_num):
        plt.plot([freq_range[i], freq_range[i]], [0, freq_value[i]], c="b")
    plt.scatter(freq_range, freq_value, marker="^")
    plt.xlabel("$\omega$")
    plt.ylabel("$X(e^{j\omega})$")
    plt.title(fr"$\frac{{2\pi}}{{{N}}}\sum_{{k=-\infty}}^{{+\infty}}\delta(\omega-\frac{{2\pi k}}{{{N}}})$", pad=20)
    plt.draw()
    return

def plot_aperiodic_unit_impulse_spectrum(amplitude=1, omega_begin=-30, omega_end = 30):
    plt.plot([omega_begin, omega_end], [amplitude, amplitude])
    plt.text(omega_end + 1, amplitude, "...", fontdict={"fontsize": 15})
    plt.text(omega_begin - 3, amplitude, "...", fontdict={"fontsize": 15})
    plt.xlabel("$\omega$")
    plt.ylabel("$X(e^{j\omega})$")
    plt.title(f"{amplitude}")
    plt.draw()

def plot_unit_step_spectrum(amplitude=1, time_begin=-35, time_end=36):
    """plot dt unit step function's fourier transform spectrum

    Args:
        amplitude (int, optional): [description]. Defaults to 1.
        time_begin (int, optional): [time domain sampling start point]. Defaults to -35.
        time_end (int, optional): [time domain sampling end point]. Defaults to 36.
    """
    time_domain_t = np.arange(time_begin, time_end)
    time_domain_signal = np.heaviside(time_domain_t, 1) * amplitude

    sp = np.fft.fft(time_domain_signal, time_domain_signal.size)
    freq = np.fft.fftfreq(sp.size, d=1)
    # print(sp.size)
    true_idx = list(range(time_end, sp.size)) + list(range(time_end))
    # print(true_idx)
    sp = sp[true_idx]
    freq = freq[true_idx]
   
    plt.plot(freq, sp.real, label="Real part")
    plt.plot(freq, sp.imag, label="Imaginary part")
    plt.legend()
    plt.xlabel("$\omega$")
    plt.ylabel("$X(e^{j\omega})$")
    plt.title(fr"part of $\frac{{{amplitude}}}{{1-e^{{-j\omega}}}}+\sum_{{k=\infty}}^{{+\infty}}{amplitude}\pi\delta(\omega-2\pi k)$(near origin)", pad=20)
    plt.draw()
    return

def plot_dt_exponential_spectrum(amplitude=1, omega0=1, l_begin=-10, l_end=11):
    """cannot use fft because it can't display the periodic property

    Args:
        omega0 (int, optional): [description]. Defaults to 1.
        time_begin (int, optional): [description]. Defaults to -10.
        time_end (int, optional): [description]. Defaults to 21.
    """
    freq_range = omega0 + np.arange(l_begin, l_end) * np.pi * 2
    freq_value = np.ones_like(freq_range) * amplitude * np.pi * 2
    if amplitude > 0:
        plt.ylim(bottom=0, top=amplitude * np.pi * 2 + 4)
    total_num = freq_range.shape[0]
    for i in range(total_num):
        plt.plot([freq_range[i], freq_range[i]], [0, freq_value[i]], c='b')
    plt.scatter(freq_range, freq_value, marker="^")
    plt.xlabel("$\omega$")
    plt.ylabel("$X(e^{j\omega})$")
    plt.title(fr"$2\pi·{amplitude}\sum_{{l=-\infty}}^{{+\infty}}\delta(\omega-{omega0}-2\pi l)$", pad=20)
    plt.draw()
    return
    
def plot_dt_sa_function_spectrum(amplitude=1, W=np.pi/2, cycles=5):
    """discrete sampling function

    Args:
        amplitude (int, optional): [description]. Defaults to 1.
        W ([type], optional): [must be in the range (0, \pi)]. Defaults to np.pi/2.
        cycles (int, optional): [how many filters to be plotted]. Defaults to 5.
    """
    assert 0 < W < np.pi, "The range of W must be in the range (0, pi)!"
    freq_period = 2 * np.pi
    temp1 = np.arange(-cycles * freq_period - W, (cycles + 1) * freq_period - W, freq_period)
    temp2 = np.arange(-cycles * freq_period + W, (cycles + 1) * freq_period + W, freq_period)
    freq_range = np.vstack([temp1, temp2]).T
    freq_value = amplitude
    if amplitude > 0:
        plt.ylim(bottom=0, top=amplitude + 4)
    for pair in freq_range:
        plt.plot([pair[0], pair[1]], [freq_value, freq_value], c="b")
        plt.plot([pair[0], pair[0]], [0, amplitude], c="b")
        plt.plot([pair[1], pair[1]], [0, amplitude], c="b")
    plt.xlabel("$\omega$")
    plt.ylabel("$X(e^{j\omega})$")
    plt.title(fr"$lowpass\ filter\ with\ T={{2\pi}}\ and\ \omega_c={round(W, 3)}$")
    plt.text(freq_range[-1, 1] + 1, amplitude, "···")
    plt.text(freq_range[0, 0] - 3, amplitude, "···")
    plt.draw()
    
    return

if __name__ == "__main__":
    
    plot_dt_sa_function_spectrum()