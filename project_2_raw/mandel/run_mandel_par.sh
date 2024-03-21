#!/bin/bash
#SBATCH --job-name=mandel_par     # Job name    (default: sbatch)
#SBATCH --output=mandel_par-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=mandel_par-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=32         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:15:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

make clean
make

mkdir -p pngs

# Run the program OMP_NUM_THREADS equal to 1
OMP_NUM_THREADS=4
export OMP_NUM_THREADS
build/mandel_par
