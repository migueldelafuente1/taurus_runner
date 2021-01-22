'''
Created on Jan 3, 2021

@author: Miguel
'''

from src_taurus_runner.t_sources import InteractionArgs, WaveFunctionArgs, \
    ParticleNumberArgs, IterationArgs, ConstrainsArgs, InputSource
from src_taurus_runner.t_runner import IsotopeRunner, ConstraintsRunner
from t_runner import SingleRunner


if __name__ == '__main__':
    
    _args = {
        InteractionArgs.Param.interaction : 'usbd',
        InteractionArgs.Param.COM_correction : True, 
        InteractionArgs.Param.read_reduced_Hamiltonian : True
    }
     
    i1 = InteractionArgs(**_args)
#     i1 = InteractionArgs('usdb')
    i2 = WaveFunctionArgs()
    _args = {
        ParticleNumberArgs.Param.Z_active : 2,
        ParticleNumberArgs.Param.N_active : 2,
        ParticleNumberArgs.Param.gauge_angles_n : 5
    }
     
    i3 = ParticleNumberArgs(**_args)
    i4 = IterationArgs()
    
    _args = {
        ConstrainsArgs.Param.constr_Q40 : 1.50,
        ConstrainsArgs.Param.constraint_NZ : False
    }
    i5 = ConstrainsArgs(**_args)
    i5.setConstraint(ConstrainsArgs.Param.constr_Q10, -0.1)
     
    _input = InputSource(i1, i2, i3, i4, i5)
    _input.createInputFile()
    
    ir = SingleRunner(2, 2, 'usdb')
    ir.runProcess()

#     
#     z = 0
#     n_list = [i for i in range(0, 5, 2)]
#     interaction = 'usdb'
#     
#     ir = IsotopeRunner(z, n_list, interaction)
#     ir.runProcess()
#     
#     _constrains = {ConstrainsArgs.Param.constr_Q20 : [-0.1, 0.0, 0.1, 0.2, 0.3],
#                    ConstrainsArgs.Param.constr_Jz  : 0.5,
#                    ConstrainsArgs.Param.constr_Q10 : [0.5]}
#     ir = ConstraintsRunner(z, n_list, interaction, _constrains)
#     ir.runProcess()
    
    
    
    