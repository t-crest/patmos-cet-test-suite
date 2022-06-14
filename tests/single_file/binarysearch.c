// RUN: %single-file-test binarysearch_main
// END.
/*

  This program is part of the TACLeBench benchmark suite.
  Version V 2.0

  Name: binarysearch

  Author: Sung-Soo Lim <sslim@archi.snu.ac.kr>

  Function: binarysearch performs binary search in an array of 15 integer
    elements.
    This program is completely structured (no unconditional jumps, no exits
    from loop bodies), and does not contain switch statements, no do-while
    loops.

  Source: MRTC
          http://www.mrtc.mdh.se/projects/wcet/wcet_bench/bs/bs.c

  Original name: bs

  Changes: 
	2022-06-02 : Now takes seed through stdin.
				 Array initialization now initializes keys in sorted order.
				 Expected result is now generated in binarysearch_init.
				 Now searchs for key that is always in array.

  License: May be used, modified, and re-distributed freely, but
           the SNU-RT Benchmark Suite must be acknowledged

*/

/*
  This program is derived from the SNU-RT Benchmark Suite for Worst
  Case Timing Analysis by Sung-Soo Lim
*/
#include <stdio.h>
#include "rand.h"

/*
  Forward declaration of functions
*/

void binarysearch_init( void );
int binarysearch_return( void );
int binarysearch_binary_search( int );
void binarysearch_main( void ) ;
int main( void );


/*
  Declaration of global variables
*/

volatile int binarysearch_seed;

struct binarysearch_DATA {
  int key;
  int value;
};

struct binarysearch_DATA binarysearch_data[ 15 ];

int binarysearch_result;
int binarysearch_search_key;
int binarysearch_search_value;


/*
  Initialization- and return-value-related functions
*/

/*
  Generates random integers between 0 and 8094
*/
int binarysearch_randomInteger() {
	return random_integer() % 8095;
}

void binarysearch_init( void )
{
  int i;
  int prev_key = 0;
  _Pragma( "loopbound min 15 max 15" )
  for ( i = 0; i < 15; ++i ) {
    binarysearch_data[ i ].key = prev_key + 1 + binarysearch_randomInteger();
	prev_key = binarysearch_data[ i ].key;
    binarysearch_data[ i ].value = binarysearch_randomInteger();
  }
  int idx = binarysearch_randomInteger()%15;
  
  binarysearch_search_key = binarysearch_data[idx].key;
  binarysearch_search_value = binarysearch_data[idx].value;
}


int binarysearch_return( void )
{
  return ( binarysearch_result );
}


/*
  Algorithm core functions
*/

int binarysearch_binary_search( int x )
{
  int fvalue, mid, up, low;

  low = 0;
  up = 14;
  fvalue = -1;

  _Pragma( "loopbound min 1 max 4" )
  while ( low <= up ) {
    mid = ( low + up ) >> 1;
	
    if ( binarysearch_data[ mid ].key == x ) {
      /* Item found */
      up = low - 1;
      fvalue = binarysearch_data[ mid ].value;
    } else

      if ( binarysearch_data[ mid ].key > x )
        /* Item not found */
        up = mid - 1;
      else
        low = mid + 1;
  }

  return ( fvalue );
}


/*
  Main functions
*/

void _Pragma( "entrypoint" ) binarysearch_main( void )
{
  binarysearch_result = binarysearch_binary_search( binarysearch_search_key );
}


int main( void )
{
  int seed;
  scanf("%d", &seed);
  init_seed(seed);
  
  binarysearch_init();
  binarysearch_main();

  return !( binarysearch_return() == binarysearch_search_value);
}
