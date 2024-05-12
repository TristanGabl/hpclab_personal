from mpi4py import MPI
import numpy as np

SUBDOMAIN = 6 
DOMAINSIZE = (SUBDOMAIN+2) 

comm = MPI.COMM_WORLD
size = comm.Get_size()
if size != 16:
    raise ValueError("np can only be 16 in this script")
rank = comm.Get_rank()

data = np.ones((DOMAINSIZE, DOMAINSIZE), dtype=np.int64) * rank

dims = [4,4]
periods = [True, True]
comm = comm.Create_cart(dims, periods, reorder=True)
coords = comm.Get_coords(rank)

up, down = comm.Shift(0, 1)
left, right = comm.Shift(1, 1)

send = np.full(SUBDOMAIN, rank, dtype=np.int64)
receive_up = np.zeros(SUBDOMAIN, dtype=np.int64)
receive_down = np.zeros(SUBDOMAIN, dtype=np.int64)
receive_left = np.zeros(SUBDOMAIN, dtype=np.int64)
receive_right = np.zeros(SUBDOMAIN, dtype=np.int64)

request = [
    comm.Isend(send, dest=up),
    comm.Isend(send, dest=down),
    comm.Isend(send, dest=left),
    comm.Isend(send, dest=right),
    comm.Irecv(receive_up, source=up),
    comm.Irecv(receive_down, source=down),
    comm.Irecv(receive_left, source=left),
    comm.Irecv(receive_right, source=right)
]
MPI.Request.Waitall(request)
comm.Barrier()

data[0, 1:-1] = receive_up
data[-1, 1:-1] = receive_down
data[1:-1, 0] = receive_left
data[1:-1, -1] = receive_right



print(f"""
-----------------------------------
RANK: {rank}
{up=}
{down=}
{left=}
{right=}
data after exchange:
{data}
"""
)