#!/bin/bash
#SBATCH --job-name=tester      # Job name    (default: sbatch)
#SBATCH --output=tester-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=tester-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=32          # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Run the program with 8 OpenMP threads
export OMP_NUM_THREADS=4
./omp_bug2
