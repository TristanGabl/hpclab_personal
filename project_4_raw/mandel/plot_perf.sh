#!/bin/bash

module load gcc/8.2.0
module load gnuplot
LD_LIBRARY_PATH=LD_LIBRARY_PATH:/apps/gcc/gcc-6.1.0/lib64 gnuplot perf.gp