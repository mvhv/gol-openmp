/* 
 * CITS3402 - Assignment 1
 * Game of life: 4-neighbourhood
 * Row-loop parallel implementation
 *
 * Jesse Wyatt (20756971)
 */
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define DENSITY 0.5
#define RUN_TIME 100
#define mod(N, M) ((N) & ((M) - 1)) //fast true modulo for {M = i^2 : i E I}

int GRID_SIZE;

/*
 * Prints the supplied game grid to STDOUT for snapshots.
 */
void printGrid(bool* grid) {
  for (int i = 0; i < GRID_SIZE; ++i) {
    for (int j = 0; j < GRID_SIZE; ++j) {
      putchar(grid[i * GRID_SIZE + j] ? '1' : '0');
    }
    putchar('\n');
  }
  putchar('\n');
}

/*
 * Swaps the pointers to the supplied boolean arrays.
 */
void swapGrid(bool** g1, bool** g2) {
  bool* temp = *g1;
  *g1 = *g2;
  *g2 = temp;
}

/*
 * Simulates the game one step forward. Updates the next step of the game
 * in backgrid using the data of the current step held in maingrid.
 *
 * Parallelism is performed here. The outer loop progresses through the
 * rows of the game grid. The rows in this loop are divided up equally,
 * and each thread is assigned a set of these rows to process.
 */
void stepGame(bool* maingrid, bool* backgrid) {
  int neighbours;
  //parallelise outer for loop only
  #pragma omp parallel for private(neighbours)
  for (int i = 0; i < GRID_SIZE; ++i) {
    for (int j = 0; j < GRID_SIZE; ++j) {
      //check neighbourhood
      neighbours = 0;
      if (maingrid[i * GRID_SIZE + mod(j + 1, GRID_SIZE)]) ++neighbours; //R
      if (maingrid[i * GRID_SIZE + mod(j - 1, GRID_SIZE)]) ++neighbours; //L
      if (maingrid[mod(i + 1, GRID_SIZE) * GRID_SIZE + j]) ++neighbours; //D
      if (maingrid[mod(i - 1, GRID_SIZE) * GRID_SIZE + j]) ++neighbours; //U

      //update cell status
      if (neighbours == 3) {
        backgrid[i * GRID_SIZE + j] = true; //breed
      } else if (neighbours == 2 && maingrid[i * GRID_SIZE + j]) {
        backgrid[i * GRID_SIZE + j] = true; //steady
      } else {
        backgrid[i * GRID_SIZE + j] = false; //death
      }
    }
  }
}

/*
 * Initialises the game grid with random data. PRNG is default seeded
 * for ease of comparison between tests.
 */
void initGrid(bool* grid, double density) {
  for (int i = 0; i < GRID_SIZE; ++i) {
    for (int j = 0; j < GRID_SIZE; ++j) {
      if ((((double)rand() / (double)RAND_MAX)) < density) {
        grid[i * GRID_SIZE + j] = 1;
      } else {
        grid[i * GRID_SIZE + j] = 0;
      }
    }
  }
}


int main(int argc, char** argv) {
  //grid size is only argument
  if (argc == 2) {
    GRID_SIZE = atoi(argv[1]);
    //grid size must be a positive power of 2
    if ((GRID_SIZE & (GRID_SIZE - 1)) || GRID_SIZE <= 0) {
      return EXIT_FAILURE; 
    }
  } else {
    return EXIT_FAILURE;
  }

  //setup
  bool* maingrid = (bool*) malloc(sizeof(bool) * GRID_SIZE * GRID_SIZE);
  bool* backgrid = (bool*) malloc(sizeof(bool) * GRID_SIZE * GRID_SIZE);
  initGrid(maingrid, DENSITY);

  //run game
  for (int i = 0; i < RUN_TIME; ++i) {
    //snapshot at steps 0, 10, and 20
    if (i == 0 || i == 10 || i == 20) printGrid(maingrid);
    stepGame(maingrid, backgrid);
    swapGrid(&maingrid, &backgrid);
  }

  return EXIT_SUCCESS;
}
