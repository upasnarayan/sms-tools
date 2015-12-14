# functions that implement analysis and synthesis of sounds using the Sinusoidal Model
# (for example usage check the examples models_interface)

import numpy as np
from scipy.signal import blackmanharris, triang, get_window
from scipy.fftpack import ifft, fftshift
import math
import sys, os
sys.path.append('../../software/models')
import dftModel as DFT
import utilFunctions as UF  

def sineModelMultiRes(x, fs, ws, Na, Bs, t):
    """
    Analysis/synthesis of a sound using the sinusoidal multi-resolution model, without sine tracking
    x: input array sound, ws = (w1, w2, w3): analysis windows, Na = (N1, N2, N3): sizes of complex spectrums,
       Bs = (B1, B2, B3): frequency bands for multi-res sine model, t: threshold in negative dB 
    returns y: output array sound
    """

    Ns = 512                                                        # FFT size for synthesis (even)
    H = Ns/4                                                        # Hop size used for analysis and synthesis
    hNs = Ns/2                                                      # half of synthesis FFT size
    pin = max([hNs] + [int(math.floor((w.size+1)/2)) for w in ws])  # init sound pointer in middle of MAX anal window       
    pend = x.size - pin                                             # last sample to start a frame
    yw = np.zeros(Ns)                                               # initialize output sound frame
    y = np.zeros(x.size)                                            # initialize output arrays
    ws = tuple([w / sum(w) for w in ws])                            # normalize analysis windows
    sw = np.zeros(Ns)                                               # initialize synthesis window
    ow = triang(2*H)                                                # triangular window
    sw[hNs-H:hNs+H] = ow                                            # add triangular window
    bh = blackmanharris(Ns)                                         # blackmanharris window
    bh = bh / sum(bh)                                               # normalized blackmanharris window
    sw[hNs-H:hNs+H] = sw[hNs-H:hNs+H] / bh[hNs-H:hNs+H]             # normalized synthesis window
    while pin<pend:                                                 # while input sound pointer is within sound 
    #-----analysis-----
        ipfreqAll = np.array([])                                    # initialize concatenated arrays for freq/mag/phases
        ipmagAll = np.array([])
        ipphaseAll = np.array([])
        for i in range(0, len(ws)):
            w = ws[i]                                               # analysis window for band
            N = int(Na[i])                                          # FFT size for band
            upperFreq = float(Bs[i])                                # compute upper and lower frequency bands
            lowerFreq = float(0 if i == 0 else Bs[i - 1])
            upperFrame = int(np.ceil(float(upperFreq) * N / fs))    # compute corresponding frame numbers
            lowerFrame = int(np.ceil(float(lowerFreq) * N / fs))

            hM1 = int(math.floor((w.size+1)/2))                     # half analysis window size by rounding
            hM2 = int(math.floor(w.size/2))                         # half analysis window size by floor
            x1 = x[pin-hM1:pin+hM2]                                 # select frame
            mX, pX = DFT.dftAnal(x1, w, N)                          # compute dft
            ploc = UF.peakDetection(mX, t)                          # detect locations of peaks
            ploc = ploc[ploc >= lowerFrame]                         # only take locations greater than lower frame
            ploc = ploc[ploc < upperFrame]                          # and less than upper frame
            iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)     # refine peak values by interpolation
            ipfreq = fs*iploc/float(N)                              # convert peak locations to Hertz

            ipfreqAll = np.concatenate((ipfreqAll, ipfreq))         # concatenate based on values per frequency band
            ipmagAll = np.concatenate((ipmagAll, ipmag))
            ipphaseAll = np.concatenate((ipphaseAll, ipphase))

    #-----synthesis-----
        Y = UF.genSpecSines(ipfreqAll, ipmagAll, ipphaseAll, Ns, fs)   # generate sines in the spectrum         
        fftbuffer = np.real(ifft(Y))                                   # compute inverse FFT
        yw[:hNs-1] = fftbuffer[hNs+1:]                                 # undo zero-phase window
        yw[hNs-1:] = fftbuffer[:hNs+1] 
        y[pin-hNs:pin+hNs] += sw*yw                                    # overlap-add and apply a synthesis window
        pin += H                                                       # advance sound pointer
    return y

def main(inputFile='../../sounds/orchestra.wav', window='blackman', Ms = (1765, 675, 675),
                    Na=(2048, 2048, 2048), Bs=(200, 420, 22050), t=-80):
    """
    Perform analysis/synthesis using the sinusoidal multi-resolution model
    inputFile: input sound file (polyphonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)  
    M: tuple of analysis window size
    N: tuple of fft sizes (power of two, bigger or equal than M)
    B: tuple of frequency bands
    t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0   
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
    """
        
    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # read input sound
    fs, x = UF.wavread(inputFile)

    # compute analysis windows
    ws = tuple([get_window(window, M) for M in Ms])

    # analyze/synthesize the sound with the sinusoidal multi-resolution model
    y = sineModelMultiRes(x, fs, ws, Na, Bs, t)

    # output sound file name
    outputFile = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_sineModelMultiRes.wav'

    # write the synthesized sound obtained from the sinusoidal synthesis
    UF.wavwrite(y, fs, outputFile)