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


#include "itu-1770-filter.h"

// Filter:  2nd Order Digital Filter of Direct Form II
// y[n] = b[0] * m[n] + b[1] * m[n-1] + b[2] * m[n-2]
// where
// m[n] = x[n] - (a[1] * m[n-1]) - (a[2] * m[n-2])

// y[n] = b[0] * x[n] + (b[1] - b[0]*a[1]) * m[n-1] + (b[2] - b[0]*a[2]) * m[n-2]

//      = b[0] * x[n] + precalc[0] * m[n-1] + precalc[1] * m[n-2]


void filter_init(itu1770_filter *filter) {

    memset(filter, 0, sizeof(itu1770_filter));

}


void filter_init_pre_filter(itu1770_filter *filter, unsigned int samplerate) {

    filter_init(filter);

    double a[3];
    double b[3];


if (samplerate == 48000) {

    memcpy(a, pre_coeff_a, 3*sizeof(double));
    memcpy(b, pre_coeff_b, 3*sizeof(double));

} else {  // works quite ok for 48khz as well

    // Calculate values...
    //
    // As descibed in Zolzer, DAFX book (p. 50 -55)
    // High shelving filter, gain +4dB

    int G = 4;  		// Gain
    unsigned short fc = 1682;		// Center freq  (need to verify this sometime...)
    unsigned int fs = samplerate;	// Sample rate

    double K = tan( (FILTER_PI * fc) / fs );    
    double V0 = pow(10.0, G / 20.0);

    //double sqrt2=pow(2, 0.5);

    // these give slightly closer results to  precalculated values
    double Q = 0.707189761905293;
    double sqrt2=1 / Q;	       // 1.4140476204093

    double pow_k_2 = pow(K, 2);
    double divider = (1 + sqrt2 * K + pow_k_2 );


    a[0]= 1;
    a[1]= ( 2* ( pow_k_2 - 1 ) ) / divider;
    a[2]= (1 - sqrt2*K + pow_k_2) / divider;
    b[0]= (V0 + K * sqrt2 * pow(V0, 0.5) + pow_k_2 ) / divider;
    b[1]= ( 2* ( pow_k_2 - V0 ) ) / divider;
    b[2]= (V0 - K * sqrt2 * pow(V0, 0.5) + pow_k_2 ) / divider;

}




    filter_set_coefficients(filter, a, b);

}



void filter_init_rlb_filter(itu1770_filter *filter, unsigned int samplerate) {

    filter_init(filter);

    double a[3];
    double b[3];


if (samplerate == 48000 || 1) {

    memcpy(a, rlb_coeff_a, 3*sizeof(double));
    memcpy(b, rlb_coeff_b, 3*sizeof(double));

} else {  // Works quite good for 48khz as well

    // Calculate values...
    //
    // As descibed in Zolzer, DAFX book (p. 43)
    // 

    unsigned short fc = 54;		// Center freq  (need to verify this sometime...)
    unsigned int fs = samplerate;	// Sample rate

    double K = tan( (FILTER_PI * fc) / fs );    

    double sqrt2=pow(2, 0.5);

    double pow_k_2 = pow(K, 2);
    double divider = (1 + sqrt2 * K + pow_k_2 );



    a[0]= 1;
    a[1]= ( 2* ( pow_k_2 - 1 ) ) / divider;
    a[2]= (1 - sqrt2*K + pow_k_2) / divider;

    b[0]= 1 / divider;
    b[1]= -2 / divider;
    b[2]= 1  / divider;

}



    filter_set_coefficients(filter, a, b);

}




void filter_set_coefficients(itu1770_filter *filter, double *a, double *b){

    int i=0;
    for (i=0; i< 3; i++) {
	filter->a[i] = a[i];
	filter->b[i] = b[i];
    }

    filter->precalc[0]=b[1] - (b[0] * a[1]);
    filter->precalc[1]=b[2] - (b[0] * a[2]);

}




double filter_calculate(itu1770_filter *filter, double x) {


    double y = filter->b[0] * x + filter->precalc[0] * filter->m[0] + filter->precalc[1] * filter->m[1];

    double m = x - (filter->a[1] * filter->m[0]) - (filter->a[2] * filter->m[1]);

    filter->m[1] = filter->m[0];
    filter->m[0] = m;

    return  y;

}






void filter_destroy(itu1770_filter *filter) {

    // For future use...


}
