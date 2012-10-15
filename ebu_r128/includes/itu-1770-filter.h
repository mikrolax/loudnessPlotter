/*
 *  Loudness analyze library
 *  implementing EBU R.128  
 *
 *  ITU 1770 filtering routines
 *
 *  Copyright (C) 2011 Staale Helleberg, Radio Nova, Oslo, Norway
 *  Released under  GNU GENERAL PUBLIC LICENSE (GPL) Version 3
 *
 */


#ifndef _ITU1770_FILTER_H_
#define _ITU1770_FILTER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>  // usleep


#include <math.h>

#define FILTER_PI 	3.14159265358979323846


typedef struct itu1770_filter {

    unsigned char order;

    double a[3];
    double b[3];
    double precalc[2];
    double m[2];  // buffer of (delayed) temp values


} itu1770_filter;


    // Coeffs for 48khz (from specification)

    // Prefilter
    static double pre_coeff_a[3]={1.0,    -1.69065929318241, 0.73248077421585};
    static double pre_coeff_b[3]={1.53512485958697,   -2.69169618940638, 1.19839281085285};

    // RLB Weighting curve
    static double rlb_coeff_a[3]={1.0,    -1.99004745483398, 0.99007225036621};
    static double rlb_coeff_b[3]={1.0,   -2.0, 1.0};



void filter_init(itu1770_filter *filter);
void filter_init_pre_filter(itu1770_filter *filter, unsigned int samplerate);
void filter_init_rlb_filter(itu1770_filter *filter, unsigned int samplerate);
void filter_set_coefficients(itu1770_filter *filter, double *a, double *b);
double filter_calculate(itu1770_filter *filter, double x);
void filter_destroy(itu1770_filter *filter);

#endif
