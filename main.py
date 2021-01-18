'''
Created on Jan 3, 2021

@author: Miguel
'''

from src_taurus_runner.tsources import InteractionArgs, WaveFunctionArgs, \
    ParticleNumberArgs, IterationArgs, ConstrainsArgs, InputSource, _Data
from src_taurus_runner.trunner import IsotopeRunner, ConstraintsRunner


if __name__ == '__main__':
    
    i1 = InteractionArgs('usdb')
    i2 = WaveFunctionArgs()
    i3 = ParticleNumberArgs(2,2)
    i4 = IterationArgs()
    i5 = ConstrainsArgs()
    i5.setConstraint(ConstrainsArgs.Param.constr_Q10, -0.1)
    
    _input = InputSource(i1, i2, i3, i4, i5)
    _input.createInputFile()
    
    z = 0
    n_list = [i for i in range(0, 5, 2)]
    interaction = 'usdb'
    
    ir = IsotopeRunner(z, n_list, interaction)
    ir.runProcess()
    
    _constrains = {ConstrainsArgs.Param.constr_Q20 : [-0.1, 0.0, 0.1, 0.2, 0.3],
                   ConstrainsArgs.Param.constr_Jz  : 0.5,
                   ConstrainsArgs.Param.constr_Q10 : [0.5]}
    ir = ConstraintsRunner(z, n_list, interaction, _constrains)
    ir.runProcess()
    
    
    
    