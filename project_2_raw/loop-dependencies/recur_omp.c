#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "walltime.h"

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
    int nthreads = omp_get_num_threads();
    int tid = omp_get_thread_num();
    int section = N / nthreads;
    int n_begin = tid * section;
    int n_end = n_begin + section;

    double Sn_private = Sn * pow(up, n_begin);
    for (n = n_begin; n <= n_end; ++n) {
      opt[n] = Sn_private;
      Sn_private *= up;
    }


    {
      Sn = Sn * pow(up, N);
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
