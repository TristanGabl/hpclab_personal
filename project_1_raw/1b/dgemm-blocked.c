const char* dgemm_desc = "Blocked dgemm.";

#include <stdio.h>
#include <math.h>

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */



#define MIN(A, B) (((A) < (B)) ? (A) : (B))

void square_dgemm(int n, double* A, double* B, double* C) {
  // TODO: Implement the blocking optimization
  //       (The following is a placeholder naive three-loop dgemm)

  // long int l2 = 1 << 29;
  // int s = sqrt(l2 / 3 / sizeof(double));
  int s = 100; 
  
  for (int i = 0; i < n; i += s) {
    for (int j = 0; j < n; j += s) {
      for (int k = 0; k < n; k += s) {
        for (int ii = i; ii < MIN(i + s, n); ++ii) {
          for (int jj = j; jj < MIN(j + s, n); ++jj) {
            double tmp = 0.0;
            int kk_rest = k;
            for (int kk = k; kk < MIN(k + s, n) - 8; kk += 8) {
              tmp += A[ii+kk*n] * B[kk+jj*n];
              tmp += A[ii+(kk+1)*n] * B[kk+1+jj*n];
              tmp += A[ii+(kk+2)*n] * B[kk+2+jj*n];
              tmp += A[ii+(kk+3)*n] * B[kk+3+jj*n];
              tmp += A[ii+(kk+4)*n] * B[kk+4+jj*n];
              tmp += A[ii+(kk+5)*n] * B[kk+5+jj*n];
              tmp += A[ii+(kk+6)*n] * B[kk+6+jj*n];
              tmp += A[ii+(kk+7)*n] * B[kk+7+jj*n];
              kk_rest = kk + 8;
            }
            for (int kk = kk_rest; kk < MIN(k + s, n); ++kk) {
              tmp += A[ii+kk*n] * B[kk+jj*n];
            }
            C[ii+jj*n] += tmp;
          }
        }
      }
    }
  }
}
