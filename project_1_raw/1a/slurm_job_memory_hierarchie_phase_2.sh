#!/bin/bash
#SBATCH --job-name=slurm_job_memory_hierarchie                    # Job name    (default: sbatch)
#SBATCH --output=slurm_job_memory_hierarchie_phase_2-%j.out               # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_memory_hierarchie_phase_2-%j.err                # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                                                # Number of tasks
#SBATCH --cpus-per-task=1                                         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                                        # Memory per CPU
#SBATCH --time=00:01:00                                           # Wall clock time limit
#SBATCH --constraint EPYC_7763                                    # CPU model constraint

# load some modules & list loaded modules
module load gcc
module list

# run (srun: run job on cluster with provided resources/allocation)
srun lscpu 
srun hwloc-ls --whole-system --no-io -f --of fig EPYC_7763.fig
