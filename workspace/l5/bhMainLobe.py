import numpy as np
import sys
sys.path.append('../../software/models')
import utilFunctions as UF

bins = np.array([-4, -3, -2, -1, 0, 1, 2, 3])
X = UF.genBhLobe(bins)