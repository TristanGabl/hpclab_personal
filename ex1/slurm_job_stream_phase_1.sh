#!/bin/bash
#SBATCH --job-name=slurm_job_memory_hierarchie                    # Job name    (default: sbatch)
#SBATCH --output=slurm_job_stream_phase_1-%j.out               # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_stream_phase_1-%j.err                # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                                                # Number of tasks
#SBATCH --cpus-per-task=1                                         # Number of CPUs per task
#SBATCH --mem-per-cpu=1G                                          # Memory per CPU
#SBATCH --time=00:01:00                                           # Wall clock time limit
#SBATCH --constraint EPYC_7H12                                    # CPU model constraint

# load some modules & list loaded modules
module load gcc
module list

# run (srun: run job on cluster with provided resources/allocation)
srun stream_c_phase_1
