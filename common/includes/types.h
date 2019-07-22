/**
 * @file types.h
 * @brief Header file with the basic includes, defines and functions.
 */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef TYPES_H__
#define TYPES_H__

#include <stdlib.h>
#include <stdio.h>

#include <stdarg.h>

/* Basic types */
#define ERR -1
#define OK 0
#define TRUE 1
#define FALSE 0
#define DEBUG 0
#define SYNC 0


void free_pointers (int n, ...);

void copy_1d_array (double * src, double * dst, int n_elems);

#endif // TYPES_H__

#ifdef __cplusplus
}
#endif

