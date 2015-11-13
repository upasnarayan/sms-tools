import sys
sys.path.append('../../software/models')
import utilFunctions as UF
import stochasticModel as STM

(fs, x) = UF.wavread('../../sounds/ocean.wav')
H = 128
stocf = .2
stockEnv = STM.stochasticModelAnal(x, H, H*2, stocf)