/*
 *  Loudness analyze library
 *  implementing EBU R.128  
 *
 *  Small and dirty wave library
 *
 *  Copyright (C) 2011 Staale Helleberg, Radio Nova, Oslo, Norway
 *  Released under  GNU GENERAL PUBLIC LICENSE (GPL) Version 3
 *
 */

#ifndef _WAVE_H_
#define _WAVE_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>  // usleep


typedef struct s_wave_header {

    unsigned char headers_valid;
    unsigned int total_size;  // chunk data size from riff header
    unsigned short compression;
    unsigned short channels;
    unsigned int sample_rate;
    unsigned int audio_size;
    unsigned short resolution;
    unsigned short block_align;
} s_wave_header;


int parse_wavefile(FILE *f, s_wave_header *wh);
void wave_parse_fmt(FILE *f, s_wave_header *wh, unsigned int len);

#endif
