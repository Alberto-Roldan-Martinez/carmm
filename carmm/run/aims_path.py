def set_aims_command(hpc='hawk', basis_set='light'):
    '''
    Choose supercomputer and basis_set to obtain FHI-aims run command.
    Can be useful to e.g perform a calcaluation with a larger basis set
    after a geometry optimisation.
    #
    # basis_set :
    Parameters:

    hpc: String
        Name of the HPC facility where the jobs is being run
        Options: 'hawk', 'isambard', 'archer'  ## needs Thomas
    basis_set: String
        Name of basis set for FHI-aims
        Options: 'light', 'intermediate', 'tight', 'really_tight' etc.
    '''
    import os

    # TODO: Be a bit more rigorous on system variables. We could load them here
    #       and then not reference them in further strings?
    mpirun = "time mpirun -np $SLURM_NTASKS "
    aprun = "time aprun -n $NPROCS /home"
    executable = "bin/aims.$VERSION.scalapack.mpi.x"
    species = "species_defaults/"+basis_set

    if hpc.lower() == 'hawk':
        fhi_aims_directory="/home/scw1057/software/fhi-aims/"
        preamble = mpirun
    elif hpc.lower() == 'isambard':
        fhi_aims_directory="/home/ca-alogsdail/fhi-aims-gnu/"
        preamble = aprun
    elif hpc.lower() == 'archer':
        fhi_aims_directory="/home3/e05/e05/ajl340/fhi-aims-src-intel/"
        preamble = aprun

    os.environ["ASE_AIMS_COMMAND"]= preamble + fhi_aims_directory + executable
    os.environ["AIMS_SPECIES_DIR"] = fhi_aims_directory + species
