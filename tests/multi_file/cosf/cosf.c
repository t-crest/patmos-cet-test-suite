// RUN: %multi-file-test cosf_main false
// END.
/*

  This program is part of the TACLeBench benchmark suite.
  Version V 1.9

  Name: cosf

  Author: Dustin Green

  Function: cosf performs calculations of the cosinus function

  Source: 

  Original name:

  Changes:

  License: this code is FREE with no restrictions

*/

#include <stdio.h>
#include "rand.h"
#include "wcclibm.h"


/*
  Forward declaration of functions
*/

void cosf_init( int );
void cosf_main( void ) __attribute__((noinline));
int cosf_return( void );
int main( void );


/*
  Declaration of global variables
*/

float cosf_solutions;


/*
  Initialization function
*/

void cosf_init( int seed )
{
  cosf_solutions = random_or(seed,0);
}


/*
  Return function
*/

int cosf_return( void )
{
  int temp = cosf_solutions;

  if ( temp == -4 )
    return 0;
  else
    return -1;
}


/*
  Main functions
*/

void _Pragma( "entrypoint" ) cosf_main( void )
{
  float i;
  _Pragma( "loopbound min 100 max 100" )
  for ( i = 0.0f; i < 10; i += 0.1f )
    cosf_solutions += basicmath___cosf( i );
}


int main( void )
{
  int seed;
  scanf("%d", &seed);
  init_seed(seed);
  
  cosf_init(seed);
  cosf_main();
  return cosf_return();
}

