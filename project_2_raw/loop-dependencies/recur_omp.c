#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "walltime.h"
#include <omp.h>

int main(int argc, char *argv[]) {
  int N = 2000000000;
  double up = 1.00000001;
  double Sn = 1.00000001;
  int n;

  /* allocate memory for the recursion */
  double *opt = (double *)malloc((N + 1) * sizeof(double));
  if (opt == NULL) {
    perror("failed to allocate problem size");
    exit(EXIT_FAILURE);
  }

  double time_start = walltime();
  // TODO: YOU NEED TO PARALLELIZE THIS LOOP 
  #pragma omp parallel shared(opt, Sn)
  {
    int tid = omp_get_thread_num();
    int nthreads = omp_get_num_threads();
    int chunk = N / nthreads;
    int start = tid * chunk;
    int end = (tid == nthreads - 1) ? N : start + chunk;

    double Sn_i = Sn * pow(up, start);

    for (n = start; n <= end; ++n) {
      opt[n] = Sn_i;
      Sn_i *= up;
    }

    if (tid == nthreads - 1) {
      Sn = Sn_i;
    }
  }

  printf("Parallel RunTime  :  %f seconds\n", walltime() - time_start);
  printf("Final Result Sn   :  %.17g \n", Sn);

  double temp = 0.0;
  for (n = 0; n <= N; ++n) {
    temp += opt[n] * opt[n];
  }
  printf("Result ||opt||^2_2 :  %f\n", temp / (double)N);
  printf("\n");

  return 0;
}
