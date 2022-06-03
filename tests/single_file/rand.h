#ifndef _PATMOS_CET_TEST_SUITE_RAND_H_
#define _PATMOS_CET_TEST_SUITE_RAND_H_

unsigned int patmos_cet_test_suite_seed;

/*
  init_seed initializes the seed used in the "random" number
  generator.
*/
void init_seed( unsigned int seed )
{
  if(seed == 0) {
	// Wikipedia says our PRNG function can't be used on a 0 seed
	patmos_cet_test_suite_seed = 1;
  } else {
	patmos_cet_test_suite_seed = seed;
  }
}

/*
  'Xorshift' Random number generator from wikipedia
*/
unsigned int random_integer( void )
{
  unsigned int x = patmos_cet_test_suite_seed;
  x ^= x << 13;
  x ^= x >> 17;
  x ^= x << 5;
  patmos_cet_test_suite_seed = x;
  return patmos_cet_test_suite_seed;
}

#endif