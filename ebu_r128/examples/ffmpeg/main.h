/*
 *  Loudness analyze library
 *  implementing EBU R.128  
 *
 *  Example program using FFMPEG / AV Codec libraries for decoding
 *
 *  Copyright (C) 2011 Staale Helleberg, Radio Nova, Oslo, Norway
 *  Released under  GNU GENERAL PUBLIC LICENSE (GPL) Version 3
 *
 */

#ifndef _MAIN_H_
#define _MAIN_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "ebu_r128.h"

void get_ampl_from_ch_map(s_ebu_r128 *cfg, int64_t channel_map);


#endif
