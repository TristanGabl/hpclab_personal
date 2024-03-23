CC     ?= gcc-13
CFLAGS = -O3 -fopenmp

all: build/quicksort_omp build/quicksort_seq

build/quicksort_omp: build/quicksort_omp.o build/walltime.o
	$(CC) $(CFLAGS) $^ -o $@

build/quicksort_seq: build/quicksort_seq.o build/walltime.o
	$(CC) $(CFLAGS) $^ -o $@

build/quicksort_omp.o: quicksort_omp.c walltime.h
	$(CC) -c $(CFLAGS) $< -o $@

build/quicksort_seq.o: quicksort_seq.c walltime.h
	$(CC) -c $(CFLAGS) $< -o $@

build/walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $< -o $@

.PHONY: clean
clean:
	$(RM) build/*
