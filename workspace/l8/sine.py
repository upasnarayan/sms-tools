import numpy as np
from scipy.signal import get_window
import sys
sys.path.append('../../software/models')
sys.path.append('../../software/transformations')
import sineModel as SM
import sineTransformations as ST
import utilFunctions as UF

inputFile = '../../sounds/piano.wav'
window = 'hamming'
M = 1001
N = 2048
t = -100
minSineDur = 0.01
maxnSines = 150
freqDevOffset = 30
freqDevSlope = 0.02

Ns = 512
H = 128

(fs, x) = UF.wavread(inputFile)

w = get_window(window, M)

tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

y = SM.sineModelSynth(tfreq, tmag, np.array([]), Ns, H, fs)

UF.wavwrite(y, fs, 'sinemodel.wav')