#include "data.h"
#include "mpi.h"

#include <cmath>
#include <iostream>

namespace data {

// fields that hold the solution
Field y_new;
Field y_old;

// fields that hold the boundary points
Field bndN;
Field bndE;
Field bndS;
Field bndW;

// buffers used during boundary halo communication
Field buffN;
Field buffE;
Field buffS;
Field buffW;

// global domain and local sub-domain
Discretization options;
SubDomain domain;

void SubDomain::init(int mpi_rank, int mpi_size,
                     Discretization& discretization) {
    // DONE: determine the number of sub-domains in the x and y dimensions
    //       using MPI_Dims_create
    int dims[2] = {0, 0};
    MPI_Dims_create(mpi_size, 2, dims);
    ndomx = dims[0];
    ndomy = dims[1];

    // DONE: create a 2D non-periodic Cartesian topology using MPI_Cart_create
    int periods[2] = {0, 0};
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 0, &comm_cart);
    // DONE: retrieve coordinates of the rank in the topology using
    // MPI_Cart_coords
    int coords[2] = {0, 0};
    MPI_Cart_coords(comm_cart, mpi_rank, 2, coords);
    // Note that I adopt 0-based indexing here
    domx = coords[0];
    domy = coords[1];

    // DONE: set neighbours for all directions using MPI_Cart_shift
    MPI_Cart_shift(comm_cart, 0, +1, &neighbour_west, &neighbour_east);
    MPI_Cart_shift(comm_cart, 1, +1, &neighbour_south, &neighbour_north);

    // get bounding box
    nx = discretization.nx / ndomx;
    ny = discretization.nx / ndomy;
    // int split_idx_x = discretization.nx % ndomx;
    // int split_idx_y = discretization.nx % ndomy;
    // // New divisibility handling
    // if (domx < split_idx_x) {
    //     nx++;
    //     startx = domx * nx;
    // } else {
    //     startx = split_idx_x * (nx + 1) + (domx - split_idx_x) * nx;
    // }
    // if (domy < split_idx_y) {
    //     ny++;
    //     starty = domy * ny;
    // } else {
    //     starty = split_idx_y * (ny + 1) + (domy - split_idx_y) * ny;
    // }
    startx = (domx)*nx+1;
    starty = (domy)*ny+1;

    endx = startx + nx - 1;
    endy = starty + ny - 1;

    // Old divisibility handling
    // if (domx == ndomx) {
    //     endx = discretization.nx;
    //     nx = endx - startx + 1;
    // }
    // if (domy == ndomy) {
    //     endy = discretization.nx;
    //     ny = endy - starty + 1;
    // }

    // get total number of grid points in this sub-domain
    N = nx * ny;
    rank = mpi_rank;
    size = mpi_size;
}

// print domain decomposition information to stdout
void SubDomain::print() {
    for (int irank = 0; irank < size; irank++) {
        if (irank == rank) {
            std::cout << "rank " << rank << " / " << size << " : (" << domx
                      << ", " << domy << ")"
                      << " neigh N:S " << neighbour_north << ":"
                      << neighbour_south << " neigh E:W " << neighbour_east
                      << ":" << neighbour_west << " local dims " << nx << " x "
                      << ny << std::endl;
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }
}

} // namespace data
