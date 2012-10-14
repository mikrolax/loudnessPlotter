/*
 *  Loudness analyze library
 *  implementing EBU R.128  
 *
 *  Analyzis and calculation routines
 *
 *  Copyright (C) 2011 Staale Helleberg, Radio Nova, Oslo, Norway
 *  Released under  GNU GENERAL PUBLIC LICENSE (GPL) Version 3
 *
 */

#ifndef _EBU_R128_H_
#define _EBU_R128_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>  // usleep


#include <math.h>
#include "itu-1770-filter.h"

enum modes {EBU_MODE_NONE=0, EBU_MODE_MOMENTARY, EBU_MODE_SHORT_TERM, EBU_MODE_INTEGRATED};

typedef struct s_audio_channel {
    itu1770_filter pre_filter;
    itu1770_filter rlb_filter;

    float *audio_buffer;
    float *temp_audio_buffer;

    float gain;
} s_audio_channel;


typedef struct s_ebu_r128 {

    unsigned char mode;
    unsigned int samplerate;

    unsigned short buffer_size_ms;    
    unsigned int buffer_size_samples;
    unsigned int temp_buffer_size_samples;

    unsigned int temp_buffer_size_ms;
    unsigned int temp_buffer_counter;

    unsigned char resolution;

    unsigned char channels;
    s_audio_channel *audio_channels;


    float *integrator_gz;
    unsigned long long int integrator_len;
    unsigned char relative_gate;

    float lk;

} s_ebu_r128;


int ebu_r128_init(s_ebu_r128 *cfg, unsigned char channels, unsigned char resolution, unsigned int samplerate ,unsigned char mode);
int ebu_r128_adjust_gain(s_ebu_r128 *cfg, unsigned char channel, float gain);
int ebu_r128_adjust_relative_gain(s_ebu_r128 *cfg, signed char relative_gate);


int ebu_r128_process_samples(s_ebu_r128 *cfg, void *audio, size_t num_samples);
float ebu_r128_get_integrated_lufs(s_ebu_r128 *cfg);
int ebu_r128_destroy(s_ebu_r128 *cfg);


float calculate_ampl_from_db(float db_in);
float calculate_mean_square(float *y, size_t samples);
int ebu_r128_calculate_lkfs(s_ebu_r128 *cfg);


#endif
