const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double* A, double* B, double* C) {
  // TODO: Implement the blocking optimization
  //       (The following is a placeholder naive three-loop dgemm)
  int s = 1000; // blocking with s-by-s matrix
  int block = n / s; // block iterations
  for (int i = 0; i < s; i += block) {
    for (int j = 0; j < s; j += block) {
      for (int k = 0; k < s; k += block) {
        for (int ii = i; ii < i + block; ++ii) {
          for (int jj = j; jj < j + block; ++jj) {
            for (int kk = k; kk < k + block; ++kk){
              C[ii+jj*n] += A[ii+kk*n] * B[kk+jj*n];
              
            }
          }
        }
      }
    }
  }
  for (int i = block * s; i < n; ++i) {
    for (int j = block * s; j < n; ++j) {
      for (int k = block * s; k < n; ++k) {
        C[i+j*n] += A[i+k*n] * B[k+j*n];
      }
    }
  }
}
