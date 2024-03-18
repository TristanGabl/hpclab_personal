#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"

int main(int argc, char *argv[]) {
  long int N = 1000000000;
  double time_start, h, sum, pi;
  int number_thread;

  if ( argc > 1 ) N = atol(argv[1]);

  /* Parallelize with OpenMP using the critical directive */
  time_start = walltime();

  h = 1./N;
  sum = 0.;
  #pragma omp parallel
  {
    double partial_sum = 0.;
    int nthreads = omp_get_num_threads();
    number_thread = nthreads;
    int tid = omp_get_thread_num();
    int i_beg = tid * N / nthreads;
    int i_end = (tid + 1) * N / nthreads;
    for (int i = i_beg; i < i_end; ++i) {
      double x = (i + 0.5)*h;
      partial_sum += 4.0 / (1.0 + x*x);
    }
    #pragma omp critical
    sum += partial_sum;
  }
  pi = sum*h;
  double time = walltime() - time_start;

  printf("reduction, number_thread = %d, pi = \%.15f, N = %d, time = %.5f secs\n", number_thread, pi, N, time);
  

  return 0;
}
