#ifndef _PATMOS_CET_TEST_SUITE_RAND_H_
#define _PATMOS_CET_TEST_SUITE_RAND_H_

/*
  init_seed initializes the seed used in the "random" number
  generator.
*/
void init_seed( unsigned int seed );

/*
  'Xorshift' Random number generator from wikipedia
*/
unsigned int random_integer( void );

#define random_or(random, or) (random!=0? random_integer() : or)

#endif