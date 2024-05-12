from mpi4py import MPI

# get comm, size, rank & host name
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
proc = MPI.Get_processor_name()

rank_send = rank
rank_receive = 0

sum = 0
for i in range(size):
      comm.send(rank_send, dest=(rank + 1) % size)
      rank_receive = comm.recv(source=(rank - 1 + size) % size)

      sum += rank_receive
      rank_send = rank_receive

print(f"[rank {rank}]: final sum = {sum}")
