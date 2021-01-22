'''
Created on Jan 21, 2021

@author: Miguel
'''
from t_sources import Enum

#===============================================================================
# OUTPUT RECOVER OF THE FILES
#===============================================================================

class Result():
    
    class outputFilesEnum(Enum):
        occupation_numbers = 'occupation_numbers.dat'
        canonical_basis    = 'canonicalbasis.dat'
        eigenbasis_h       = 'eigenbasis_h.dat'
        eigenbasis_H11     = 'eigenbasis_H11.dat'
        final_wave_function     = 'final_wf.bin'
        reduced_hamiltonian     = 'usdb.red'
            