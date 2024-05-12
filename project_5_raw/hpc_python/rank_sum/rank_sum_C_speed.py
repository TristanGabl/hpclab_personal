from mpi4py import MPI
import numpy as np

# get comm, size, rank & host name
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

sum_send = np.array([rank], dtype=np.int64)
sum_receive = np.array([0], dtype=np.int64)
sum = 0
for i in range(size):
      comm.Send(sum_send, dest=(rank + 1) % size)
      comm.Recv(sum_receive, source=(rank - 1 + size) % size)

      sum += sum_receive
      sum_send = sum_receive 

print(f"[rank {rank}]: final sum = {sum[0]}")

