import numpy as np
from scipy.signal import get_window, resample
import math
import sys, time
from scipy.fftpack import fft, ifft
sys.path.append('../../software/models')
import utilFunctions as UF

(fs, x) = UF.wavread('../../sounds/ocean.wav')
M = N = 256
stocf = 0.2
w = get_window('hanning', M)
xw = x[10000:10000+M] * w
X = fft(xw)
mX = 20 * np.log10(abs(X[:N/2]))
mXenv = resample(np.maximum(-200, mX), N/2*stocf)

mY = resample(mXenv, N/2)
pY = 2*np.pi*np.random.rand(N/2)
Y = np.zeros(N, dtype=complex)
Y[:N/2] = 10**(mY/20) * np.exp(1j*pY)
Y[N/2+1:] = 10**(mY[:0:-1]/20) * np.exp(-1j * pY[:0:-1])
y = np.real(ifft(Y))