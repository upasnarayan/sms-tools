import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import sys
sys.path.append('../../software/models')
import utilFunctions as UF
import sineModel as SM

inputFile = '../../sounds/oboe-A4.wav'
window = 'hamming'
M = 501
N = 1024
t = -90
maxSineDur = 0.1
maxnSines = 20
freqDevOffset = 10
freqDevSlope = 0.001
H = 200

(fs, x) = UF.wavread(inputFile)
w = get_window(window, M)
tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, maxSineDur, freqDevOffset, freqDevSlope)

numFrames = int(tfreq[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
tfreq[tfreq <= 0] = np.nan
plt.plot(frmTime, tfreq)

plt.show()