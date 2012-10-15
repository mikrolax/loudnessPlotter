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


#include "main.h"

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>



int main(int argc, char * argv[]) {


    if (argc != 2 && argc != 3 && argc != 4) {
	fprintf(stderr, "use: %s <filename> [ebu_mode (m,s,i) [audiostream_id] ]\n", argv[0]);
	return 0;
    } 	


    // Av codec stuff
    AVFormatContext *formatContext;
    AVCodecContext *codecContext;
    AVCodec *codec;
    AVPacket packet;

    // Loudness library stuff
    s_ebu_r128 config;
    unsigned char ebu_mode = EBU_MODE_INTEGRATED;


    // User have decideded which mode to use
    if (argc > 2) {
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


    // Which audiostream to decode; -1 find first
    int audioStream=-1;

    // User have decideded which stream to decode
    if (argc > 3) {
	audioStream=atoi(argv[3]);
    }


    // Insert audio here...
    unsigned char decoded_audio[AVCODEC_MAX_AUDIO_FRAME_SIZE];



    int i=0;
    int out_size=0;


    // Register avcodec stuff
    av_register_all();

    // Open the file
    if(av_open_input_file(&formatContext, argv[1], NULL, 0, NULL)!=0) {
	fprintf(stderr, "Could not open file '%s'\n", argv[1]);
	return -1; 
    }


    // get info about stream (type, codec etc).
    if(av_find_stream_info(formatContext)<0) {
	fprintf(stderr, "Could not find any information of streams in file\n");
	 return -1; // Couldn't find stream information
    }



    for(i=0; i<formatContext->nb_streams; i++) {
	    if(formatContext->streams[i]->codec->codec_type==CODEC_TYPE_AUDIO) {

		// if not set, select it
		if (audioStream == -1)
		audioStream=i;

		fprintf(stdout, "Audio Stream %d has %d channels %s\n", i, formatContext->streams[i]->codec->channels, i==audioStream ? "<-- selected": "");


	    }
    }

    // File does not have any audio tracks
    if(audioStream==-1) {
	fprintf(stderr, "No audio streams!\n");
	 return -1; 
    }

    // Select the codec
    codecContext=formatContext->streams[audioStream]->codec;


    // Show info; for debugging
//    dump_format(formatContext, 0, argv[1], 0);
//    fprintf(stdout, "Using stream %d - %dhz, %d channels\n", audioStream, codecContext->sample_rate, codecContext->channels);

    unsigned char resolution=0;

    switch (codecContext->sample_fmt) {
	case SAMPLE_FMT_U8:
	    resolution=8;
	break;

	case SAMPLE_FMT_S16:
	    resolution=16;
	break;

	case SAMPLE_FMT_S32:
	    resolution=32;
	break;


    }



    // Initialize library
    if (!ebu_r128_init(&config, codecContext->channels, resolution, codecContext->sample_rate, ebu_mode )) { 
	fprintf(stderr, "EBU R128 Init failed!\n");
	ebu_r128_destroy(&config);
	av_close_input_file(formatContext);
	return 0;
    }


    // Enable this if you want to change relative gain
/*    if (!ebu_r128_adjust_relative_gain(&config, 10)) {
	fprintf(stderr, "EBU R128 set realtive gain failed!\n");
	ebu_r128_destroy(&config);
	av_close_input_file(formatContext);
	return 0;
    }
*/


    // Get the codec
    codec=avcodec_find_decoder(codecContext->codec_id);

    if(codec==NULL) {
	fprintf(stderr, "Unsupported codec!\n");
	ebu_r128_destroy(&config);
	av_close_input_file(formatContext);
	return -1; // Codec not found
    }


    // Open codec
    if(avcodec_open(codecContext, codec)<0) {
	fprintf(stderr, "Could not open codec!\n");
	ebu_r128_destroy(&config);
	av_close_input_file(formatContext);
	return -1; // Could not open codec
    }



    if (codecContext->channel_layout > 0) { // Use channel map from ffmpeg
	get_ampl_from_ch_map(&config, codecContext->channel_layout);
    }



    // Read file...
    while(av_read_frame(formatContext, &packet)>=0) {	

	// Is this the selected stream?
	if(packet.stream_index==audioStream) {


	    // Still data left...
	    while (packet.size > 0) {

		// We have room for this amount of audio...
		out_size = AVCODEC_MAX_AUDIO_FRAME_SIZE;

		// Decode...
		int len=avcodec_decode_audio3(codecContext, (void *)decoded_audio, &out_size, &packet);
	     
		// There are some decoded samples...
		if (len > 0 ) {

		    // There are this many samples...
		    size_t num_samples = out_size / (config.resolution * codecContext->channels / 8);

		    // So we analyze them...
		    int r=ebu_r128_process_samples(&config, decoded_audio, num_samples);

	    	    if (!r) {
			fprintf(stderr, "Error in processing!\n");
			// destroy
			avcodec_close(codecContext);
			av_close_input_file(formatContext);
			ebu_r128_destroy(&config);		
			return 0;
		    }



		    if (r  == 2) {  // new updated loudness value available

			float lk=config.lk;

			if (config.mode == EBU_MODE_INTEGRATED) {
			// In file mode, we're usually only in to the final (overall) Lk value, so skip this calculation to save time
			// lk=ebu_r128_get_integrated_lufs(&config);
			// fprintf(stdout, "Current Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
			} else {
	    		    fprintf(stdout, "Current Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
			}
		    }



		    // Adjust and decode any bytes left over
		    packet.size-=len;
		    packet.data+=len;

		} else {
		    // no data available
		    break;
		}

	    } // while packet.size > 0

	}
    } // while av_read_frame


    // Close codec
    avcodec_close(codecContext);

    // Close file
    av_close_input_file(formatContext);

    // Now display the integrated (overall) loudness value
    if (config.mode == EBU_MODE_INTEGRATED) {
	float lk=ebu_r128_get_integrated_lufs(&config);
	fprintf(stdout, "Final Lk=%.2f LUFS,  %.2f LU\n", lk,  lk + 23);
    }


    ebu_r128_destroy(&config);



return 0;

}

void get_ampl_from_ch_map(s_ebu_r128 *cfg, int64_t channel_map) {

	unsigned char bit_pos=0;
	unsigned char ch=0;
	while (channel_map > 0) {

		int64_t bitmask = (1 << bit_pos);

		if (channel_map & bitmask) {

			switch (bitmask) {

				case CH_FRONT_CENTER:
				case CH_FRONT_LEFT:
				case CH_FRONT_RIGHT:
				    	cfg->audio_channels[ch].gain = 1;
				break;



				case CH_BACK_LEFT:
				case CH_BACK_RIGHT:
				case CH_SIDE_LEFT:
				case CH_SIDE_RIGHT:
					cfg->audio_channels[ch].gain = calculate_ampl_from_db(1.5);
				break;

				case CH_LOW_FREQUENCY:
					cfg->audio_channels[ch].gain = 0;
				break;

				default: 
					printf("Unhandled channel\n");

			}
			ch++;
			channel_map -= bitmask;
		}

		bit_pos++;

	}

    return;
}

