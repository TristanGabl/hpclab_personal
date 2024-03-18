#!/bin/bash
#SBATCH --job-name=pi_omp_serial     # Job name    (default: sbatch)
#SBATCH --output=pi_omp_serial-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=pi_omp_serial-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list


# Run the program with N=1000000000 for OMP_NUM_THREADS equal to 1
./pi_serial
