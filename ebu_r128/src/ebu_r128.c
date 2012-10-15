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


#include "ebu_r128.h"



// Initialize the config struct, and calculate various values
int ebu_r128_init(s_ebu_r128 *cfg, unsigned char channels, unsigned char resolution, unsigned int samplerate ,unsigned char mode) {

    memset(cfg, 0, sizeof(s_ebu_r128));

    if (channels == 0 || mode == EBU_MODE_NONE || resolution == 0) { 
	fprintf(stderr, "Invalid channels, ebu_mode and/or resolution\n");
	return 0;
    }


    switch (mode) {

	case EBU_MODE_MOMENTARY:
	    cfg->buffer_size_ms=400;    
	    cfg->temp_buffer_size_ms=200;
	break;

	case EBU_MODE_SHORT_TERM:
	    cfg->buffer_size_ms=3000;    
	    cfg->temp_buffer_size_ms=100;  // 10 hz
	break;

	case EBU_MODE_INTEGRATED:
	    cfg->buffer_size_ms=400;    
	    cfg->temp_buffer_size_ms=200;
	break;

	default:
	    return 0;

    }
     

    cfg->channels=channels;
    cfg->samplerate=samplerate;
    cfg->mode=mode;
    cfg->resolution = resolution;
    cfg->relative_gate = 8;

    // "normal" buffer size
    cfg->buffer_size_samples=(cfg->buffer_size_ms * cfg->samplerate) / 1000;

    // "temp" buffer size
    // When the temp buffer is full, calculation is done...
    cfg->temp_buffer_size_samples=(cfg->temp_buffer_size_ms * cfg->samplerate) / 1000;

    // Create mem area for the audio channels
    cfg->audio_channels = malloc(channels * sizeof(s_audio_channel));

    if (!cfg->audio_channels)
	return 0;

    // Clear the area
    memset(cfg->audio_channels, 0,  channels * sizeof(s_audio_channel));


    unsigned char i=0;
    for (i=0; i < cfg->channels; i++) {



	// Initialize PRE filtering
	filter_init_pre_filter(&cfg->audio_channels[i].pre_filter, cfg->samplerate);

	// Initialize RLB filtering
	filter_init_rlb_filter(&cfg->audio_channels[i].rlb_filter, cfg->samplerate);

	// Create main and temp buffer
	cfg->audio_channels[i].audio_buffer = malloc(cfg->buffer_size_samples * sizeof(float));
	cfg->audio_channels[i].temp_audio_buffer = malloc(cfg->temp_buffer_size_samples * sizeof(float));

	if (!cfg->audio_channels[i].audio_buffer || !cfg->audio_channels[i].temp_audio_buffer) {
	    return 0;
	}

	// Clear the buffers	
	memset(cfg->audio_channels[i].audio_buffer, 0, cfg->buffer_size_samples * sizeof(float));
	memset(cfg->audio_channels[i].temp_audio_buffer, 0, cfg->temp_buffer_size_samples * sizeof(float));

	// L, R, C channel have 0dB Gain
	cfg->audio_channels[i].gain = 1.0;

	// Left and Right surround  (normally ch 3 and 4) have gain 1.5dB approx 1.41
	if (i == 3 || i == 4) {
	    cfg->audio_channels[i].gain = calculate_ampl_from_db(1.5);
	}

	if (i > 4) {
	    cfg->audio_channels[i].gain = 0; // LFE (and above) should be muted. If you need more channels, change the gain using the ebu_r128_adjust_gain() function after init.
	}


    }

    // EBU I mode buffer (to store g*z values in)
    cfg->integrator_gz = malloc(sizeof(float));
    
    if (!cfg->integrator_gz)
	return 0;


    return 1;
}




// Calculate amplification ratio from a dB Value
float calculate_ampl_from_db(float db_in) {
    return pow(10.0f,   db_in / 10.0f);
}





// Calculate the mean square value z over all samples in input y
float calculate_mean_square(float *y, size_t samples) {

    double z=0;
    size_t i=0;

    double v=0;

    for (i=0; i<samples; i++) {

	v= y[i] ;  
	z += (v*v) ;

    }

    z/= (double)samples;

    return (float) z;
}


int ebu_r128_adjust_gain(s_ebu_r128 *cfg, unsigned char channel, float gain){

	if (channel < cfg->channels) {
	    cfg->audio_channels[channel].gain = calculate_ampl_from_db(gain);
	    return 1;
	} 

    return 0;

}

int ebu_r128_adjust_relative_gain(s_ebu_r128 *cfg, signed char relative_gate) {

    cfg->relative_gate = abs(relative_gate);
    return 1;	    
}


int ebu_r128_calculate_lkfs(s_ebu_r128 *cfg){

    // size of buffers    
    size_t size_of_temp = (cfg->temp_buffer_size_samples*sizeof(float));
    size_t size_of_main = (cfg->buffer_size_samples*sizeof(float));

    // Summed Mean Square over all channels
    float z_total=0;

    unsigned char ch=0;

    for (ch = 0; ch < cfg->channels; ch++) {
	void *p=cfg->audio_channels[ch].audio_buffer;
	void *q=cfg->audio_channels[ch].temp_audio_buffer;

	// Move one data in main buffer size_of_tmp samples to the left
	memcpy(p, 		  p+size_of_temp, size_of_main - size_of_temp);

	// Add the new samples to (the end of) the main buffer
	memcpy(p+(size_of_main - size_of_temp), q, 	         size_of_temp);
	
	// Calculate Mean Square of the main buffer and add to total
	z_total+=cfg->audio_channels[ch].gain * calculate_mean_square(cfg->audio_channels[ch].audio_buffer, cfg->buffer_size_samples);
    }


    cfg->lk=-0.691 + 10*log10(z_total);

	if (cfg->mode == EBU_MODE_INTEGRATED) {
	    if (cfg->lk > -70) { // Absolute Gate

		// expand the buffer
		cfg->integrator_len++;
		cfg->integrator_gz = realloc(cfg->integrator_gz, cfg->integrator_len * sizeof(float));

		if (!cfg->integrator_gz) {
		    fprintf(stderr, "can not alloc integrator mem\n");
		    exit(1); // TODO: Handle this better
		}    

		cfg->integrator_gz[cfg->integrator_len-1] = z_total;
	    }

	}

    return 1;

}


// Process a buffer of samples; convert from whatever to double, filter and if needed calculate. Returns -1 if error, 1 if new value calculated, 0 else
// Input is a buffer of interleaved samples of cfg->resolution bits
int ebu_r128_process_samples(s_ebu_r128 *cfg, void *audio, size_t num_samples){

    int ret=1;
    size_t i=0;

    unsigned int divider = (1 << (cfg->resolution-1))-1;


    for (i=0; i<num_samples; i++) {

	unsigned char ch = 0;

	    for (ch = 0; ch < cfg->channels; ch++) {
    
	    double value=0;

		switch (cfg->resolution) {
	
		    case 8: {
			char *a = audio;
			value = (a[i * cfg->channels + ch] / (double)divider);
			}
		    break;

		    case 16: {
			short *a = audio;
			value = (a[i * cfg->channels + ch] / (double)divider);
			}
		    break;


		    case 24: {
			unsigned char *sample_start = audio + (i*cfg->channels*3  + ch*3);

			// this way we keep the signess :)
			int t= sample_start[2] << 24 | sample_start[1] << 16 | sample_start[0]<<8 | 0x0;
			value= ((t / 256) / (double)divider);

			}
		    break;

		    case 32: {
			int *a = audio;
			value = (a[i * cfg->channels + ch]  /  (double)divider);
			}
		    break;



		    default:
			fprintf(stderr, "unsupported resolution: %d bit\n", cfg->resolution);
		    return 0;

		}

		// Do filtering for this sample
		value=filter_calculate(&cfg->audio_channels[ch].pre_filter, value);
		value=filter_calculate(&cfg->audio_channels[ch].rlb_filter, value);
		cfg->audio_channels[ch].temp_audio_buffer[cfg->temp_buffer_counter]=(float)value;

	    }

	// increase position in temp buffer
	cfg->temp_buffer_counter++;

	// buffer is full, calculate!
	if (cfg->temp_buffer_counter == cfg->temp_buffer_size_samples) {

	    ebu_r128_calculate_lkfs(cfg);

	    cfg->temp_buffer_counter=0;
	    ret=2;

	}


    }

    
return ret;

}


// Calculate and return the current lufs

float ebu_r128_get_integrated_lufs(s_ebu_r128 *cfg) {

    float z=0;
    float z_total=0;

    unsigned long long int num_elements=0;    
    unsigned long long int i=0;

    // First calculate loundness over the full integration buffer. Buffer is allready gated at -70dB
    for (i=0; i<cfg->integrator_len; i++) {
	z_total+=cfg->integrator_gz[i];
    }

    z_total/=cfg->integrator_len;

    // and calculate the relative gate, 8dB below generic loudness
    float relative_gate=-0.691 + 10*log10(z_total) - cfg->relative_gate;


    // now remove all blocks with loundness < relative_gate    

    for (i=0; i<cfg->integrator_len; i++) {
	    float lk=-0.691 + 10*log10(cfg->integrator_gz[i]);

	    if (lk > relative_gate) { 
		z+=cfg->integrator_gz[i];
		num_elements++;
	    }
    }

    z/=num_elements;


    // calculate and return the integrated lufs
    return -0.691 + 10*log10(z);
}




// free any unsed mem etc...
int ebu_r128_destroy(s_ebu_r128 *cfg) {

    unsigned char i=0;

    if (cfg->audio_channels) {

	for (i=0; i < cfg->channels; i++) {

	    if(cfg->audio_channels[i].audio_buffer)
		free(cfg->audio_channels[i].audio_buffer);

	    filter_destroy(&cfg->audio_channels[i].pre_filter);
	    filter_destroy(&cfg->audio_channels[i].rlb_filter);


	}

	free(cfg->audio_channels);
    }    


	if (cfg->integrator_gz)
	free(cfg->integrator_gz);

    return 1;

}
 

