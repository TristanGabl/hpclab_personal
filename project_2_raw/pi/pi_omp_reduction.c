#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"

int main(int argc, char *argv[]) {
  long int N = 1000000000;
  double time_start, h, sum, pi;
  int number_thread;

  if ( argc > 1 ) N = atol(argv[1]);

  /* Parallelize with OpenMP using the reduction clause */
  time_start = walltime();
  h = 1./N;
  sum = 0.;
  #pragma omp parallel for reduction(+:sum)
  for (int i = 0; i < N; ++i) {
    double x = (i + 0.5)*h;
    sum += 4.0 / (1.0 + x*x);
  }
  pi = sum*h;
  double time = walltime() - time_start;
  #pragma omp parallel
  {
    number_thread = omp_get_num_threads();
  }

  printf("reduction, number_thread = %d, pi = \%.15f, N = %d, time = %.5f secs\n", number_thread, pi, N, time);

  return 0;
}
