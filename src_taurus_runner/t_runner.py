'''
Created on Jan 7, 2021

@author: Miguel
'''

import os
import subprocess
import shutil

from src_taurus_runner.t_sources import InputSource, InteractionArgs, \
    WaveFunctionArgs, IterationArgs, ConstrainsArgs, ParticleNumberArgs, Result

class RunnerException(BaseException):
    pass

class _Runner(object):
    """ 
    Abstract class:
        Run fortran programs and manage the output textfile results
    """
    
    F90_PROGRAM     = "taurus_vap.exe"
    INPUT_FILENAME  = InputSource.INPUT_FILENAME
    OUTPUT_DIRECTORY= "output_folder"
    OUTPUT_FILENAME_TEMPLATE = "output_{}.txt"
    COMPLEMENTARY_FILES = None
    
    log_file    = OUTPUT_DIRECTORY + "logs.txt"
    
    _index_folder = 0
    _current_folder_name = ''
    
    def __new__(self, *args, **kwargs):
        """
        Create a directory and manage all mandatory attributes 
        """
        
        ## Mandatory attributes
        self.COMPLEMENTARY_FILES = self.OUTPUT_DIRECTORY+"/exe_files_"
        
        self.input_source = None
        self.output_filename = None
        self.results = {}
        
        ## create directory for the output
        _dir_name = self.OUTPUT_DIRECTORY
        self._current_folder_name = self.OUTPUT_DIRECTORY
        self._createFolder(_dir_name, new_calculation=True)
#         _createFolder(_dir_name)
        
        return object.__new__(self)
    
    @classmethod
    def _createFolder(cls, folder_name, new_calculation=False):
        """
        Remove previous results from other calculations and create folder to 
        store results.
        
        :new_calculation Resets a folder for a Runner execution (from __new__),
                         when folders are created inside a run the argument 
                         is False (default).
        """
        if new_calculation and (cls._index_folder > 0):
            folder_name = cls._updateFolderIndex(folder_name)
        
        _a = os.path.exists(folder_name)
        _b = os.getcwd()
        ## create directory for the output
        if os.path.exists(folder_name):
            # remove elements in folder (for folder tree use shutil.rmtree)
            _files = os.listdir(folder_name)
            print("Files to remove:", _files)
            if len(_files) > 0:
                shutil.rmtree(folder_name)
        
        if ('/' in folder_name) or ('\\' in folder_name):
            os.makedirs(folder_name, exist_ok=True)
        else:
            os.mkdir(folder_name)
        
        if new_calculation:
            cls._index_folder += 1
        
    @classmethod
    def _updateFolderIndex(cls, folder_name):
        """ When running a new Runner calculation, add an index to avoid 
        overwrite that results.
        """
        dirs = os.listdir(os.getcwd())
        dirs = filter(lambda d: d.startswith(folder_name), dirs)
        
        folder_name = folder_name + "({})".format(len(list(dirs))) 
        
        _comp_files = cls.COMPLEMENTARY_FILES.replace(cls.OUTPUT_DIRECTORY,
                                                     folder_name)
        cls.COMPLEMENTARY_FILES = _comp_files
        cls._current_folder_name = folder_name
        
        return folder_name
        
    def __init__(self, *args, **kwargs):
        raise RunnerException("Abstract class, implement me!")
        
    def runProcess(self):
        """
        Define here the iteration to be called from the main.
        """
        # TODO: __iter__ / __next__ ??
        raise RunnerException("Abstract method, implement me!")
    
#     def __call__(self):
#         
#         ## create input
#         self.inputProcess()
#         
#         ## run
#         self._run()
#         
#         ## get basic data.
#         self._getAllData()
#     
#     
#     def inputProcess(self):
#         raise RunnerException("Abstract method, implement me!")
        
    def _run(self):
        """
        Internal execution,
        every runner works same here: from current input file, run and keep the 
        results in a text file. Then process by implementation that info. 
        """
        _e = subprocess.call('./{} < {} > {}'.format(self.F90_PROGRAM,
                                                     self.INPUT_FILENAME,
                                                     self.output_filename), 
                             shell=True)
        # a2 = subprocess.check_output('./Debug/program_2.exe',
        #                              stderr=subprocess.STDOUT)
        
        if not os.path.exists(self.output_filename):
            raise Exception("Problem with the f90 program, it has not produced the"
                            "output file [{}]".format(self.output_filename))
        
        # get data before move
        self._getAllData()
        
        self._moveAllResultsIntoFolder()
#         shutil.copy(self.OUTPUT_FILENAME, self.OUTPUT_DIRECTORY)
        
        
    def _moveAllResultsIntoFolder(self):
        
        #TODO: change to move after debug
        
        shutil.copy(self.output_filename, self._current_folder_name)
        
        # create another auxiliary folder to keep the other files
        aux_folder = self._getDataStorageDirectoryName()
        self._createFolder(aux_folder)
        
        for _file in Result.outputFilesEnum.members():
            shutil.copy(_file, aux_folder)
            
    
    def _getDataStorageDirectoryName(self):
        """
        Return a name for the complementary data folder
        """
        return self.COMPLEMENTARY_FILES
        
    def _getAllData(self):
        """
        Get info from output_file, acts on results collection. 
        """
        raise RunnerException("Abstract method, implement me!")
        
        
    

class IsotopeRunner(_Runner):
    
    OUTPUT_DIRECTORY = "output_isotopes"
    
    def __init__(self, Z, N_list, interaction, *arg, **kwargs):
        
        assert type(Z) is int, "Z is not <int>. Got [{}]".format(Z)
        if type(N_list) is int:
            N_list = [N_list]
        if not isinstance(N_list, (list, tuple)):
            raise RunnerException("N_list is not <list/tuple>. Got [{}]"
                                  .format(N_list))
        else:
            if False in (isinstance(_n, int) for _n in N_list):
                raise RunnerException("There is a non <int> N: [{}]".format(N_list))
            
        self.z = Z
        self.N_list = N_list
        self.interaction = interaction
        
        self.optional_args = kwargs
    
    def runProcess(self):
        
        i_int   = InteractionArgs(self.interaction)
        i_wf    = WaveFunctionArgs()
        i_iter  = IterationArgs()
        i_const = ConstrainsArgs()
        
        for n in self.N_list:
            self._n = n
            
            _str = "z{}n{}".format(self.z, self._n)
            self.output_filename = self.OUTPUT_FILENAME_TEMPLATE.format(_str)
            
            i_pn = ParticleNumberArgs(self.z, n)
            
            self.input_source = InputSource(i_int, i_pn, i_wf, i_iter, i_const)
            
            self._run()
        
    
    def _getAllData(self):
        """ From the output text file """
        
        with open(self.output_filename, 'r') as f:
            _data = f.readlines()
            
        for line_ in _data:
            if not line_.starstwith('Full H '):
                continue
            else:
                print(line_)
                break
        
        
    def _getDataStorageDirectoryName(self):
        
        return self.COMPLEMENTARY_FILES + "_z{}n{}".format(self.z, self._n)
    
class ConstraintsRunner(_Runner):
    
    OUTPUT_DIRECTORY = "output_constr"
    
    def __init__(self, Z, N, interaction, constraints_dict, *arg, **kwargs):
        """
        Run one/several constraints (not nested).
        
        :constraints_dict <dict> list of values to constraint for one/several
                                constraints available in <ConstraintArgs>
        """
        
        assert type(Z) is int, "Z is not <int>. Got [{}]".format(Z)
        assert type(Z) is int, "N is not <int>. Got [{}]".format(N)
        
        self.z = Z
        self.n = N
        self.interaction = interaction
        
        # TODO: set a validator of available constrains in 
        
        if not isinstance(constraints_dict, dict):
            raise RunnerException("beta_list is not dict or keyword argument."
                                  " Got [{}]".format(constraints_dict))
        self.__validateConstraintsInput()
        self.constraints_dict = constraints_dict
        
        self.constraint_beta_lm = None
        if ConstrainsArgs.Param.constraint_beta_lm in kwargs:
            self.constraint_beta_lm = kwargs.get(ConstrainsArgs.Param
                                                 .constraint_beta_lm)
        
        self.optional_args = kwargs
    
    def __validateConstraintsInput(self):
        """ 
        Verify if all names in the constraints and lists are valid.
        
        """
        _valid_prefixes = tuple(ConstrainsArgs.ParamConstrains.members())
        
        for constr_name, constr_values in self.constraints_dict.items():
            if not constr_name.startswith(_valid_prefixes):
                raise RunnerException("Invalid constraint name. Got [{}]"
                                      .format(constr_name))
            if not isinstance(constr_values, (list, tuple, float, int)):
                raise RunnerException("Invalid constraint value types. Got[{}]"
                                      .format(constr_values))
        
    
    def runProcess(self):
        
        i_int   = InteractionArgs(self.interaction)
        i_pn    = ParticleNumberArgs(self.z, self.n)
        i_wf    = WaveFunctionArgs()
        i_iter  = IterationArgs()
        i_const = ConstrainsArgs()
        
        for constr_name, constr_values in self.constraints_dict:
            for val in constr_values:
                
                i_const.setConstraint(constr_name, val)
                
                _str = "z{}n{}_".format(self.z, 
                                        self._n, 
                                        constr_name.replace('constr_'))
                
                self.output_filename = self.OUTPUT_FILENAME_TEMPLATE.format(_str)
                
                self.input_source = InputSource(i_int, i_pn, i_wf, i_iter, i_const)
                
                self._run()
            
            # return constraint to 0
            i_const.disableConstraint(constr_name)
            
            # TODO: hacer que las ligaduras que no sean listas se traten como 
            # valores a fijar para la ejecución
        
    
    def _getAllData(self):
        """ From the output text file """
        
        with open(self.output_filename, 'r') as f:
            _data = f.readlines()
            
        for line_ in _data:
            if not line_.starstwith('Full H '):
                continue
            else:
                print(line_)
                break
        
        
    def _getDataStorageDirectoryName(self):
        
        _c_str = [c.replace('constr_') for c in self.constraints_dict.keys()]
        _c_str = "_constr{}".format('_'.join(_c_str))
        
        return self.COMPLEMENTARY_FILES + "_z{}n{}_".format(self.z, 
                                                            self._n,
                                                            _c_str)
    


