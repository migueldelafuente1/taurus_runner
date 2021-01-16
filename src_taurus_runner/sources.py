'''
Created on Jan 3, 2021

@author: Miguel
'''

class Enum(object):
    
    @classmethod
    def members(cls):
        import inspect
        result = []
        for i in inspect.getmembers(cls):
            name = i[0]
            value = i[1]
            if not name.startswith('_'):
                if not inspect.ismethod(value):
                    result.append(value)
        return result

#===============================================================================
# INPUT OBJECTS AND PARTS FOR THE INPUT FILE
#===============================================================================

class DataException(BaseException):
    pass

class _Data(object):
    
    class Param(Enum):
        pass
    
    _TEMPLATE = None
    
#     @classmethod
#     def __new__(self, *args, **kwargs):
#         return object.__new__(self, *args, **kwargs)
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        """ Check if the arguments are correctly settled in the _TEMPLATE
            attribute for the class.
         
        TODO: Might move it to a testing suite to avoid call it more than once.
        """
         
        _not_in_temp = {}
        for arg in cls.Param.members():
            if arg not in cls._TEMPLATE:
                _not_in_temp.add(arg)
         
        if len(_not_in_temp) > 0:
            raise DataException("Argument/s: {} do not match with _TEMPLATE"
                                .format(list(_not_in_temp)))
        
        return super(_Data, cls).__new__(cls)
    
    
    def __init__(self, *args, **kwargs):
        raise DataException("Abstract method, implement me!")
    
    def getScientificFormat(self, value, digits=2):
        """return the number in scientific format"""
        _templ = "{:." + str(digits) + "e}"
        return _templ.format(value)

    def getStringData(self, kwargs):
        """ get template formated with the object values."""
        _str = self._TEMPLATE.format(**kwargs)
        
        # clean left tabs
        _str = '\n'.join([_s.lstrip() for _s in _str.split('\n')])
        
        return _str
    
    def __str__(self):
        raise DataException("Abstract method, implement me!")
    
    # TODO: Create a method that checks that all arguments in _TEMPLATE
    # are in the Param enumeration

class InteractionArgs(_Data):
    
    class Param(Enum):
        interaction = 'interaction'
        COM_correction = 'COM_correction'
        read_reduced_Hamiltonian = 'read_reduced_Hamiltonian'
        n_MPI_proc_per_H_team = 'n_MPI_proc_per_H_team'
    
    _TEMPLATE = """Interaction
        -----------
        Master name hamil. files      {interaction}
        Center-of-mass correction     {COM_correction}
        Read reduced hamiltonian      {read_reduced_Hamiltonian}
        No. of MPI proc per H team    {n_MPI_proc_per_H_team}
    """
    
    def __init__(self, interacion):
        
        assert isinstance(interacion, str), "interaction name must be string"
        # TODO: search valid values (put in property setter)
        
        self.interaction = interacion
        self.__COM_correction = False
        self.__read_reduced_Hamiltonian = False
        self.__n_MPI_proc_per_H_team = False
    
    @property
    def COM_correction(self):
        return self.__COM_correction * 1
    
    @COM_correction.setter
    def COM_correction(self, value):
        self.__COM_correction = value
        
    @property
    def read_reduced_Hamiltonian(self):
        return self.__read_reduced_Hamiltonian * 1
    
    @read_reduced_Hamiltonian.setter
    def read_reduced_Hamiltonian(self, value):
        self.__read_reduced_Hamiltonian = value
        
    @property
    def n_MPI_proc_per_H_team(self):
        return self.__n_MPI_proc_per_H_team * 1
    
    @n_MPI_proc_per_H_team.setter
    def n_MPI_proc_per_H_team(self, value):
        self.__n_MPI_proc_per_H_team = value
    
    def __str__(self):
        """ Get the final string for input with current data"""
        __kwargs = {
            self.Param.interaction : self.interaction,
            self.Param.COM_correction : self.COM_correction,
            self.Param.read_reduced_Hamiltonian : self.read_reduced_Hamiltonian,
            self.Param.n_MPI_proc_per_H_team : self.n_MPI_proc_per_H_team
        }
        
        return self.getStringData(__kwargs)
        
class ParticleNumberArgs(_Data):
    
    class Param(Enum):
        Z_active = 'Z_active'
        N_active = 'N_active'
        gauge_angles_p = 'gauge_angles_p'
        gauge_angles_n = 'gauge_angles_n'
    
    _TEMPLATE = """Particle Number
        ---------------
        Number of active protons      {Z_active}.00
        Number of active neutrons     {N_active}.00
        No. of gauge angles protons   {gauge_angles_p}
        No. of gauge angles neutrons  {gauge_angles_n}
    """
    
    def __init__(self, Z, N):
        
        if (not (isinstance(Z, int) and  isinstance(Z, int))
            or (Z < 0 or N < 0)):
            raise  DataException("Z:[{}], N:[{}] must be non-negative integers"
                             .format(Z, N))

        
        self.__Z_active = Z
        self.__N_active = N
        self.__gauge_angles_p = 1
        self.__gauge_angles_n = 1
    
    @property
    def Z_active(self):
        return self.__Z_active
    @Z_active.setter
    def Z_active(self, value):
        self.__Z_active = value
        
    @property
    def N_active(self):
        return self.__N_active
    @N_active.setter
    def N_active(self, value):
        self.__N_active = value
    
    
    def __str__(self):
        """ Get the final string for input with current data"""
        __kwargs = {
            self.Param.Z_active : self.Z_active,
            self.Param.N_active : self.N_active,
            self.Param.gauge_angles_p : self.__gauge_angles_p,
            self.Param.gauge_angles_n : self.__gauge_angles_n
        }
        
        return self.getStringData(__kwargs)

class WaveFunctionArgs(_Data):
    
    class Param(Enum):
        seed_type = 'seed_type'
        blocking_QP = 'blocking_QP'
        symmetry_simplifications = 'symmetry_simplifications'
        wf_file_as_text = 'wf_file_as_text'
        cuttoff_occ_sp_states = 'cuttoff_occ_sp_states'
        include_empty_sp_states = 'include_empty_sp_states'
    
    _TEMPLATE = """Wave Function   
        -------------
        Type of seed wave function    {seed_type} 
        Number of QP to block         {blocking_QP}
        No symmetry simplifications   {symmetry_simplifications}
        Read/write wf file as text    {wf_file_as_text}
        Cutoff occupied s.-p. states  {cuttoff_occ_sp_states}
        Include all empty sp states   {include_empty_sp_states}
    """
    
    def __init__(self, seed=0):
        
        self.seed_type = seed
        self.blocking_QP = 0
        self.symmetry_simplifications = 0
        self.wf_file_as_text = 0
        self.__cuttoff_occ_sp_states = 0.00e-00
        self.include_empty_sp_states = 0
        
    @property
    def cuttoff_occ_sp_states(self):
        """return the number in scientific format"""
        return self.getScientificFormat(self.__cuttoff_occ_sp_states, 
                                        digits=2)
    
    def __str__(self):
        """ Get the final string for input with current data"""
        __kwargs = {
            self.Param.seed_type : self.seed_type,
            self.Param.blocking_QP : self.blocking_QP,
            self.Param.symmetry_simplifications : self.symmetry_simplifications,
            self.Param.wf_file_as_text : self.wf_file_as_text,
            self.Param.cuttoff_occ_sp_states : self.cuttoff_occ_sp_states,
            self.Param.include_empty_sp_states : self.include_empty_sp_states
        }
        
        return self.getStringData(__kwargs)

class IterationArgs(_Data):
    
    class Param(Enum):
        iter_max = 'iter_max'
        step_intermediate = 'step_intermediate'
        log_prompt = 'log_prompt'
        grad_type = 'grad_type'
        grad_eta = 'grad_eta'
        grad_mu = 'grad_mu'
        grad_tol = 'grad_tol'
        
    
    _TEMPLATE = """Iterative Procedure
        -------------------
        Maximum no. of iterations     {iter_max}
        Step intermediate wf writing  {step_intermediate}
        More intmermediate printing   {log_prompt}
        Type of gradient              {grad_type}
        Parameter eta for gradient    {grad_eta}
        Parameter mu  for gradient    {grad_mu}
        Tolerance for gradient        {grad_tol}
    """
    
    def __init__(self, iter_max=300):
        
        assert iter_max > 0,  "iter_max:[{}] must be positive".format(iter_max)
        
        self.iter_max   = iter_max
        self.step_intermediate = 0
        self.log_prompt = 0
        self.grad_type  = 1
        self.__grad_eta = 0.1
        self.__grad_mu  = 0.3
        self.__grad_tol = 0.0001
    
    @property
    def grad_eta(self):
        """return the number in scientific format"""
        return self.getScientificFormat(self.__grad_eta, digits=3)
    @grad_eta.setter
    def grad_eta(self, value):
        self.__grad_eta = value
    
    @property
    def grad_mu(self):
        """return the number in scientific format"""
        return self.getScientificFormat(self.__grad_mu, digits=3)
    @grad_mu.setter
    def grad_mu(self, value):
        self.__grad_mu = value
    
    @property
    def grad_tol(self):
        """return the number in scientific format"""
        return self.getScientificFormat(self.__grad_tol, digits=3)
    @grad_tol.setter
    def grad_tol(self, value):
        self.__grad_tol = value
    
    
    def __str__(self):
        """ Get the final string for input with current data"""
        
        __kwargs = {
            self.Param.iter_max : self.iter_max,
            self.Param.step_intermediate : self.step_intermediate,
            self.Param.log_prompt   : self.log_prompt,
            self.Param.grad_type    : self.grad_type,
            self.Param.grad_eta     : self.grad_eta,
            self.Param.grad_mu  : self.grad_mu,
            self.Param.grad_tol : self.grad_tol
        }
        
        return self.getStringData(__kwargs)

class ConstrainsArgs(_Data):
    
    __doc__ = """ 
    Section about the Constraints :
        constraint_NZ (enforze_NZ): 0 1
        constraint_beta_lm
    """
    
    class Param(Enum):
        constraint_NZ = 'constraint_NZ'
        constraint_beta_lm = 'constraint_beta_lm'
        pair_coupling_scheme = 'pair_coupling_scheme'
        constraint_tol = 'constraint_tol'
        
        constr_Q10 = 'constr_Q10'
        constr_Q11 = 'constr_Q11'
        constr_Q20 = 'constr_Q20'
        constr_Q21 = 'constr_Q21'
        constr_Q22 = 'constr_Q22'
        constr_Q30 = 'constr_Q30'
        constr_Q31 = 'constr_Q31'
        constr_Q32 = 'constr_Q32'
        constr_Q33 = 'constr_Q33'
        constr_Q40 = 'constr_Q40'
        constr_Q41 = 'constr_Q41'
        constr_Q42 = 'constr_Q42'
        constr_Q43 = 'constr_Q43'
        constr_Q44 = 'constr_Q44'
        constr_Jx = 'constr_Jx'
        constr_Jy = 'constr_Jy'
        constr_Jz = 'constr_Jz'
        constr_P_T00_J10 = 'constr_P_T00_J10'
        constr_P_T00_J1m1 = 'constr_P_T00_J1m1'
        constr_P_T00_J1p1 = 'constr_P_T00_J1p1'
        constr_P_T10_J00 = 'constr_P_T10_J00'
        constr_P_T1m1_J00 = 'constr_P_T1m1_J00'
        constr_P_T1p1_J00 = 'constr_P_T1p1_J00'
        constr_Delta = 'constr_Delta'
    
    class ParamConstrains(Enum):
        constr_Q = 'constr_Q'
        constr_J = 'constr_J'
        constr_P_T = 'constr_P_T'
        constr_Delta = 'constr_Delta'
    
    
    _TEMPLATE = """Constraints             
        -----------
        Force constraint N/Z          {constraint_NZ}
        Constraint beta_lm            {constraint_beta_lm}
        Pair coupling scheme          {pair_coupling_scheme}
        Tolerence for constraints     {constraint_tol}
        Constraint multipole Q10      {constr_Q10}
        Constraint multipole Q11      {constr_Q11}
        Constraint multipole Q20      {constr_Q20}
        Constraint multipole Q21      {constr_Q21}
        Constraint multipole Q22      {constr_Q22}
        Constraint multipole Q30      {constr_Q30}
        Constraint multipole Q31      {constr_Q31}
        Constraint multipole Q32      {constr_Q32}
        Constraint multipole Q33      {constr_Q33}
        Constraint multipole Q40      {constr_Q40}
        Constraint multipole Q41      {constr_Q41}
        Constraint multipole Q42      {constr_Q42}
        Constraint multipole Q43      {constr_Q43}
        Constraint multipole Q44      {constr_Q44}
        Constraint ang. mom. Jx       {constr_Jx}
        Constraint ang. mom. Jy       {constr_Jy}
        Constraint ang. mom. Jz       {constr_Jz}
        Constraint pair P_T00_J10     {constr_P_T00_J10}
        Constraint pair P_T00_J1m1    {constr_P_T00_J1m1}
        Constraint pair P_T00_J1p1    {constr_P_T00_J1p1}
        Constraint pair P_T10_J00     {constr_P_T10_J00}
        Constraint pair P_T1m1_J00    {constr_P_T1m1_J00}
        Constraint pair P_T1p1_J00    {constr_P_T1p1_J00}
        Constraint field Delta        {constr_Delta}
    """
#     @classmethod
#     def __new__(cls, *args):
#         # add constraints to template and the params
#         
#         ## constraint multipole Q
#         for i in range(1, 5):
#             for j in range(i+1):
#                 attr_ = 'constr_Q{}{}'
#                 name_ = 'Constraint multipole Q{}      '.format(str(i)+str(j))
#                 name_ +='{} {}'
#                 
#                 setattr(cls.Param, attr_, (0, 0.000))
#         
#         ## constraint angular momentum
#         
#         ## constaint pair
    
    def __init__(self):
        
        self.constraint_NZ = 1
        self.constraint_beta_lm = 2
        self.pair_coupling_scheme = 1
        self.__constraint_tol = 1.000e-4
        
        _value_params = tuple(self.ParamConstrains.members())
        for constr_attr_ in self.Param.members():
            if not constr_attr_.startswith(_value_params):
                continue
            setattr(self, constr_attr_, (False, 0.000))
    
    @property
    def constraint_tol(self):
        """return the number in scientific format"""
        return self.getScientificFormat(self.__constraint_tol, digits=3)
    @constraint_tol.setter
    def constraint_tol(self, value):
        self.__constraint_tol = value
    
    def setConstraint(self, name, value):
        """ Constraint value setter """ 

        if not type(value) is float:
            raise DataException("Value must be float, [<{}> {}] given".format(
                type(value), value))
        if name in self.Param.members():
            if not name.startswith(tuple(self.ParamConstrains.members())):
                raise DataException("[{}] constraint value is not assignable"
                                    .format(name))
        else:
            raise DataException("[{}] invalid constraint name".format(name))
        
        setattr(self, name, (True, round(value, 3)))
    
    def disableConstraint(self, name):
        """ Disable Constraint, reset boolean to False and value to 0.0 """
        
        if name not in self.Param.members():
            raise DataException("[{}] invalid constraint name".format(name))
        
        setattr(self, name, (False, 0.0))
        
    
    def __str__(self):
        """ Get the final string for input with current data"""
        
        __kwargs = {
            self.Param.constraint_NZ : self.constraint_NZ,
            self.Param.constraint_beta_lm : self.constraint_beta_lm,
            self.Param.pair_coupling_scheme   : self.pair_coupling_scheme,
            self.Param.constraint_tol    : self.constraint_tol
        }
        
        _constr_vals = []
        _value_params = tuple(self.ParamConstrains.members())
        for constr_attr_ in self.Param.members():
            if not constr_attr_.startswith(_value_params):
                continue
            values = getattr(self, constr_attr_)
            value_str = '{} {}'.format(values[0] * 1, 
#                                        self.getScientificFormat(values[1], 
#                                                                 digits=3))
                                       round(values[1], 3))
            #v_value = self.getScientificFormat(values[1], digits=3)
            
            _constr_vals.append((constr_attr_, value_str))
        
        __kwargs = {**__kwargs, **dict(_constr_vals)}
        
        return self.getStringData(__kwargs)


class InputSourceException(BaseException):
    pass

class InputSource():
    
    __doc__ = """ Input composite object, insert in _parts when"""
    
    _input_parts = [
        InteractionArgs,
        ParticleNumberArgs,
        WaveFunctionArgs,
        IterationArgs,
        ConstrainsArgs
    ]
    
    INPUT_FILENAME = "temp_input.txt"
#     assert len(_parts) == sources.__dict__
    
    class PartParams(Enum):
        """ Data Input Classes to be settled, automatically inserted"""
        
        @classmethod
        def _setAttr(cls, _input_parts):
            if len(cls.members()) > 0:
                return
            
            for part in _input_parts:
                setattr(cls, part.__name__, part.__name__)
    
    PartParams._setAttr(_input_parts)
        
    
    _attribute_map = dict([(part, part[0].lower()+part[1:]) 
                                for part in PartParams.members()])
    
    def __init__(self, *args):
        
        """ 
        :args, all the Taurus input parametric sections
        """
        
        #set default attributes
        #for attr in self._attribute_map.values():
        #    setattr(self, attr, None)
            
        self.interactionArgs = None
        self.particleNumberArgs = None
        self.waveFunctionArgs = None
        self.iterationArgs = None
        self.constrainsArgs = None
        
        self._setArgumentParts(args)
        
        
    def _setArgumentParts(self, args):
        
        if len(args) != len(self._input_parts):
            raise InputSourceException("There is/are [{}] missing or extra Data"
                " arguments for the input".format(len(args)-len(self._input_parts)))
            
        if False in (isinstance(_a, _Data) for _a in args):
            raise InputSourceException("There are invalid data type objects for"
                " objects {}, must inherit from _Data"
                .format(str([_a.__class__.__bases__ for _a in args])))
        
        for arg in args:
            
            try:
                setattr(self, self._attribute_map[arg.__class__.__name__], arg)
                # the key error will raise before the Assignment exception
            except KeyError:
                raise InputSourceException(
                    "_Data object given [{}] is not a valid part."
                    .format(arg.__class__.__name__))
        
    def updateArgument(self, arg):
        """ Change an argument without re-instance the class. """        
        setattr(self, self._attribute_map[arg.__class__.__name__], arg)    
    
    def createInputFile(self):
        """ Creates a well defined TAURUS input file for the program to run. """
        _str = []
        
        _str.append(str(self.interactionArgs))
        _str.append(str(self.particleNumberArgs))
        _str.append(str(self.waveFunctionArgs))
        _str.append(str(self.iterationArgs))
        _str.append(str(self.constrainsArgs))
        
        _str = "\n".join(_str)
                
        with open('input_automated.txt', 'w+') as f:
            f.write(_str)
    

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
            
    
    