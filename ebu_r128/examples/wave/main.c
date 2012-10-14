/*
 *  Loudness analyze library
 *  implementing EBU R.128  
 *
 *  Example program with simple wave/pcm library
 *
 *  Copyright (C) 2011 Staale Helleberg, Radio Nova, Oslo, Norway
 *  Released under  GNU GENERAL PUBLIC LICENSE (GPL) Version 3
 *
 */

#include "main.h"
#include "wave.h"
#include "ebu_r128.h"

int main(int argc, char * argv[]) {

    if (argc != 2 && argc != 3) {
	fprintf(stderr, "use: %s <filename.wav> [ebu_mode (m,s,i)]\n", argv[0]);
	return 0;
    } 	

    unsigned char ebu_mode = EBU_MODE_INTEGRATED;

    s_wave_header wave_info;
    s_ebu_r128 config;

    if (argc == 3) {
	unsigned char m=argv[2][0];

	switch (m) {
	    case 'm':
		ebu_mode=EBU_MODE_MOMENTARY;
	    break;

	    case 's':
		ebu_mode=EBU_MODE_SHORT_TERM;
	    break;
    
	}

    }


    FILE *in=fopen(argv[1], "rb");

    if (!in)
	return 0;

    // Parse wave header and find audio data
    if (!parse_wavefile(in, &wave_info)) {
	fprintf(stderr, "Could not parse wave header\n");
	fclose(in);
	return 0;
    }




    if (!ebu_r128_init(&config, wave_info.channels, wave_info.resolution, wave_info.sample_rate, ebu_mode )) { 
	fprintf(stderr, "EBU R128 Init failed!\n");
	ebu_r128_destroy(&config);

	fclose(in);
	return 0;
    }

    unsigned char bytes_per_sample = (wave_info.resolution / 8);
    unsigned char audiobuffer[ 1024 * config.channels * bytes_per_sample];


    while (!feof(in)){

	memset(audiobuffer, 0, sizeof(audiobuffer));

	size_t read=fread(&audiobuffer, 1, sizeof(audiobuffer),in);

	if (read > 0) {
	    unsigned short samples=read / (bytes_per_sample * config.channels);

	    int r=ebu_r128_process_samples(&config, &audiobuffer, samples);
	
	    if (!r) {
		fprintf(stderr, "Error in processing!\n");
		// destroy
		fclose(in);
	        ebu_r128_destroy(&config);		
		return 0;
	    }

	    if (r == 2) {  // new update

		float lk=config.lk;

		if (config.mode == EBU_MODE_INTEGRATED) {
    		    // In file mode, we're usually only in to the final Lk value, so skip this calculation to save time
		    // lk=ebu_r128_get_integrated_lufs(&config);
		    // fprintf(stdout, "Current Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
		} else {
	    	    fprintf(stdout, "Current Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
		}

	    }
	}
    }


    if (config.mode == EBU_MODE_INTEGRATED) {
	float lk=ebu_r128_get_integrated_lufs(&config);
	fprintf(stdout, "Final Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
    }


    ebu_r128_destroy(&config);

    return 0;
}


