import numpy as np
from scipy.signal import get_window
import sys, os, time
sys.path.append('../../software/models')

import harmonicModel as HM
import utilFunctions as UF

(fs, x) = UF.wavread('../../sounds/sawtooth-440.wav')
w = get_window('blackman', 2001) # 2001
N = 4096 # 2048
t = -50
minf0 = 300
maxf0 = 500
f0et = 1
H = 1000

f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)