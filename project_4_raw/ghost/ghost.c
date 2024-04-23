/****************************************************************
 *                                                              *
 * This file has been written as a sample solution to an        *
 * exercise in a course given at the CSCS-USI Summer School     *
 * It is made freely available with the understanding that      *
 * every copy of this file must include this header and that    *
 * CSCS/USI take no responsibility for the use of the enclosed  *
 * teaching material.                                           *
 *                                                              *
 * Purpose: Exchange ghost cell in 2 directions using a topology*
 *                                                              *
 * Contents: C-Source                                           *
 *                                                              *
 ****************************************************************/

/* Use only 16 processes for this exercise
 * Send the ghost cell in two directions: left<->right and top<->bottom
 * ranks are connected in a cyclic manner, for instance, rank 0 and 12 are connected
 *
 * process decomposition on 4*4 grid
 *
 * |-----------|
 * | 0| 1| 2| 3|
 * |-----------|
 * | 4| 5| 6| 7|
 * |-----------|
 * | 8| 9|10|11|
 * |-----------|
 * |12|13|14|15|
 * |-----------|
 *
 * Each process works on a 6*6 (SUBDOMAIN) block of data
 * the D corresponds to data, g corresponds to "ghost cells"
 * xggggggggggx
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * gDDDDDDDDDDg
 * xggggggggggx
 */

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SUBDOMAIN 6
#define DOMAINSIZE (SUBDOMAIN+2)

int main(int argc, char *argv[])
{
    int rank, size, i, j, dims[2], periods[2], coords[2], dest_coords[2], rank_top, rank_bottom, rank_left, rank_right, rank_topright, rank_topleft, rank_bottomleft, rank_bottomright;
    double data[DOMAINSIZE*DOMAINSIZE];
    MPI_Request request[8];
    MPI_Status status;
    MPI_Comm comm_cart;
    MPI_Datatype data_ghost;

    // Initialize MPI
    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size!=16) {
        printf("please run this with 16 processors\n");
        MPI_Finalize();
        exit(1);
    }

    // initialize the domain
    for (i=0; i<DOMAINSIZE*DOMAINSIZE; i++) {
        data[i]=rank;
    }

    // TODO: set the dimensions of the processor grid and periodic boundaries in both dimensions
    dims[0]=4;
    dims[1]=4;
    periods[0]=1;
    periods[1]=1;

    // TODO: Create a Cartesian communicator (4*4) with periodic boundaries (we do not allow
    // the reordering of ranks) and use it to find your neighboring
    // ranks in all dimensions in a cyclic manner.
    
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 0, &comm_cart);
    
    // TODO: find your top/bottom/left/right neighbor using the new communicator, see MPI_Cart_shift()
    
    MPI_Cart_shift(comm_cart, 0, 1, &rank_top, &rank_bottom);	// rank_top, rank_bottom
    MPI_Cart_shift(comm_cart, 1, 1, &rank_left, &rank_right);	// rank_left, rank_right

    MPI_Cart_coords(comm_cart, rank, 2, coords);
    // rank_topleft
    dest_coords[0] = (coords[0] - 1 + dims[0]) % dims[0];			// top
    dest_coords[1] = (coords[1] - 1 + dims[1]) % dims[1];       // left
    MPI_Cart_rank(comm_cart, dest_coords, &rank_topleft);
    
    // rank_topright
    dest_coords[0] = (coords[0] - 1 + dims[0]) % dims[0];                 // top
    dest_coords[1] = (coords[1] + 1) % dims[1];			// right
    MPI_Cart_rank(comm_cart, dest_coords, &rank_topright);

    // rank_bottomright 
    dest_coords[0] = (coords[0] + 1) % dims[0];       // bottom
    dest_coords[1] = (coords[1] + 1) % dims[1];                 // right 
    MPI_Cart_rank(comm_cart, dest_coords, &rank_bottomright);

    // rank_bottomleft
    dest_coords[0] = (coords[0] + 1) % dims[0];       // bottom 
    dest_coords[1] = (coords[1] - 1 + dims[0]) % dims[1];       // left
    MPI_Cart_rank(comm_cart, dest_coords, &rank_bottomleft);



    //  TODO: create derived datatype data_ghost, create a datatype for sending the column, see MPI_Type_vector() and MPI_Type_commit()
    // data_ghost
    MPI_Type_vector(6, 1, DOMAINSIZE, MPI_DOUBLE, &data_ghost); //DataType
    MPI_Type_commit(&data_ghost);

    //  TODO: ghost cell exchange with the neighbouring cells in all directions
    //  use MPI_Irecv(), MPI_Send(), MPI_Wait() or other viable alternatives
    double* addr_top = &data[1];
    double* addr_bottom = &data[DOMAINSIZE * (DOMAINSIZE - 1) + 1];
    double* addr_left = &data[DOMAINSIZE];
    double* addr_right = &data[2 * DOMAINSIZE - 1];
    double* addr_topleft = &data[0];
    double* addr_topright = &data[DOMAINSIZE - 1];
    double* addr_bottomleft = &data[DOMAINSIZE * (DOMAINSIZE - 1)];
    double* addr_bottomright = &data[DOMAINSIZE * DOMAINSIZE - 1];    

    //  to the top
    MPI_Send(addr_top, 6, MPI_DOUBLE, rank_top, 0, comm_cart);
    MPI_Irecv(addr_bottom, 6, MPI_DOUBLE, rank_bottom, 0, comm_cart, &request[0]);

    //  to the bottom
    MPI_Send(addr_bottom, 6, MPI_DOUBLE, rank_bottom, 0, comm_cart);
    MPI_Irecv(addr_top, 6, MPI_DOUBLE, rank_top, 0, comm_cart, &request[1]);
    
    //  to the left
    MPI_Send(addr_left, 1, data_ghost, rank_left, 0, comm_cart);
    MPI_Irecv(addr_right, 1, data_ghost, rank_right, 0, comm_cart, &request[2]);
    
    //  to the right
    MPI_Send(addr_right, 1, data_ghost, rank_right, 0, comm_cart);
    MPI_Irecv(addr_left, 1, data_ghost, rank_left, 0, comm_cart, &request[3]);

    //  to the topleft
    MPI_Send(addr_topleft, 1, MPI_DOUBLE, rank_topleft, 0, comm_cart);
    MPI_Irecv(addr_bottomright, 1, MPI_DOUBLE, rank_bottomright, 0, comm_cart, &request[4]);

    //  to the topright
    MPI_Send(addr_topright, 1, MPI_DOUBLE, rank_topright, 0, comm_cart); 
    MPI_Irecv(addr_bottomleft, 1, MPI_DOUBLE, rank_bottomleft, 0, comm_cart, &request[5]);

    //  to the bottomright	
    MPI_Send(addr_bottomright, 1, MPI_DOUBLE, rank_bottomright, 0, comm_cart);
    MPI_Irecv(addr_topleft, 1, MPI_DOUBLE, rank_topleft, 0, comm_cart, &request[6]);

    //  to the bottomleft
    MPI_Send(addr_bottomleft, 1, MPI_DOUBLE, rank_bottomleft, 0, comm_cart);
    MPI_Irecv(addr_topright, 1, MPI_DOUBLE, rank_topright, 0, comm_cart, &request[7]);	

    for (int i = 0; i < 8; i++)
	MPI_Wait(&request[i], &status);

    if (rank==9) {
        printf("data of rank 9 after communication\n");
        for (j=0; j<DOMAINSIZE; j++) {
            for (i=0; i<DOMAINSIZE; i++) {
                printf("%.1f ", data[i+j*DOMAINSIZE]);
                //printf("%4.1f ", data[i+j*DOMAINSIZE]);
            }
            printf("\n");
        }
    }

    // Free MPI resources (e.g., types and communicators)
    // TODO
    MPI_Comm_free(&comm_cart);
    MPI_Type_free(&data_ghost);

    // Finalize MPI
    MPI_Finalize();

    return 0;
}
