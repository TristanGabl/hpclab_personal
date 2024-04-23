#include <mpi.h> // MPI
#include <stdio.h>

int ring_iteration(int n_ranks, int rank, int* curr_value, int* prev_value, int* sum, MPI_Status* status) {
  int rank_next = (rank + 1) % n_ranks;
  int rank_prev = rank == 0 ? n_ranks - 1 : rank - 1;

  printf("%d: current sum = %d\n", rank, *sum);
  MPI_Send(curr_value, 1, MPI_INT, rank_next, 1, MPI_COMM_WORLD);

  printf("%d: sending value %d to rank %d\n", rank, *curr_value, rank_next);
  MPI_Recv(prev_value, 1, MPI_INT, rank_prev, 1, MPI_COMM_WORLD, status);
  
  *sum += *prev_value;
  *curr_value = *prev_value;
}

int main(int argc, char *argv[]) {

  // Initialize MPI, get size and rank
  int size, rank;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // IMPLEMENT: Ring sum algorithm
  int sum = 0; 
  int curr_value = rank;
  int prev_value;

  MPI_Status status;
  for (int i = 0; i < size; i++)
    ring_iteration(size, rank, &curr_value, &prev_value, &sum, &status);

  printf("%i:, Comm_size %i: Sum = %i\n", rank, size, sum);

  // Finalize MPI
  MPI_Finalize();

  return 0;
}