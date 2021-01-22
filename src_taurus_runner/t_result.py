'''
Created on Jan 21, 2021

@author: Miguel
'''
from t_sources import Enum
# import pandas as pd

#===============================================================================
# OUTPUT RECOVER OF THE FILES
#===============================================================================
class ResultException(BaseException):
    pass

class Result():
    
    class outputFilesEnum(Enum):
        occupation_numbers = 'occupation_numbers.dat'
        canonical_basis    = 'canonicalbasis.dat'
        eigenbasis_h       = 'eigenbasis_h.dat'
        eigenbasis_H11     = 'eigenbasis_H11.dat'
        final_wave_function     = 'final_wf.bin'
        reduced_hamiltonian     = 'usdb.red'
        
    class OutputBlocks(Enum):
        INPUT_PARAMETERS  = "INPUT_PARAMETERS"
        NUCLEUS  = "NUCLEUS"
        HO_BASIS  = "HO_BASIS"
        HAMILTONIAN  = "HAMILTONIAN"
        WAVE_FUNCTION  = "WAVE_FUNCTION"
        ITERATIVE_MINIMIZATION  = "ITERATIVE_MINIMIZATION"
        QUASIPARTICLE_STATE_PROPERTIES  = "QUASIPARTICLE_STATE_PROPERTIES"

    
    def __init__(self, output_filename):
        
        try:
            with open(output_filename, 'r') as f:
                _data = f.readlines()
        except Exception as e:
            raise ResultException(str(e))
        
        self._extractDataBlocks(_data)
        self._processBlockStrings()
        
    
    def _extractDataBlocks(self, str_lines, separator='%'):
        """
        return the block structure as dictionaries for an array of string lines
        by an starting separator.
        """
        self.blocks = {}
        
        _block_name = None
        _block_lines = []
        
        i = 0
        while i < len(str_lines):
            line = str_lines[i].replace('\n', '')
            if not line.startswith(separator):
                # initial credits (skip)
                if _block_name and (line not in ('', '\n')):
                    _block_lines.append(line.strip())
            else:                    
                if _block_name:
                    self.blocks[_block_name] = _block_lines
                    
                    _block_lines = []
                    
                _block_name = str_lines[i+1].strip().replace(' ', '_')
                i += 2
                
            i += 1
    
        
    def _processBlockStrings(self):
        
        for block in self.OutputBlocks.members():
            
        





