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


#include "wave.h"

int parse_wavefile(FILE *f, s_wave_header *wh) {

    memset(wh, 0, sizeof(s_wave_header));

    size_t read=0;
    unsigned int riff=0x0;
    
    read=fread(&riff, 1, sizeof(riff), f); 

    if (read != 4)
	return 0;

    if (riff != 0x46464952)  // RIFF
	return 0;



    unsigned int chunksize=0;

    read=fread(&chunksize, 1, sizeof(chunksize), f); 

    if (read != 4)
	return 0;

    wh->total_size = chunksize;



    unsigned int wave=0x0;
    
    read=fread(&wave, 1, sizeof(wave), f); 

    if (read != 4)
	return 0;

    if (wave != 0x45564157)  // WAVE
	return 0;

    wh->headers_valid = 1;


    while (!feof(f)) {

	unsigned int chunk_id=0;
	unsigned int chunk_len=0;

	read=fread(&chunk_id, 1, sizeof(chunk_id), f); 

	if (read != 4)
	    return 0;

	read=fread(&chunk_len, 1, sizeof(chunk_len), f); 

	if (read != 4)
	    return 0;

	switch (chunk_id) {

	    case 0x20746d66:  // fmt
		wave_parse_fmt(f, wh, chunk_len);		
	    break;
	
	    case 0x61746164: // data
		wh->audio_size=chunk_len;
		return 1;
    

	    default:
		fprintf(stderr, "Unknown chunk type 0x%04x\n", chunk_id);
		fseek(f, chunk_len, SEEK_CUR);
		return 0;
	}
    }

    return 1;
}




void wave_parse_fmt(FILE *f, s_wave_header *wh, unsigned int len) {

    unsigned char data[len];
    size_t read = fread(data, 1, len, f);

    if (read == len) {
	wh->compression = data[1] << 8 | data[0];
	wh->channels =    data[3] << 8 | data[2];
	wh->sample_rate =  data[7] << 24 | data[6] << 16 |data[5] << 8 | data[4];
	wh->resolution = data[15] << 8 | data[14];
	wh->block_align =  data[13] << 8 | data[12];
    }

}
