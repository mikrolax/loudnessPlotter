CC=gcc
CFLAGS=-D_FILE_OFFSET_BITS=64 -I includes/
#CFLAGS+=-Wall

LDFLAGS=-lm 

LDFLAGS_FFMPEG=-lavcodec -lavformat


all: wave_analyze ffmpeg_analyze
ebu_r128=src/ebu_r128.o src/itu-1770-filter.o


src/itu-1770-filter.o: src/itu-1770-filter.c
	$(CC) -c $(CFLAGS) $< -o $@

src/ebu_r128.o: src/ebu_r128.c
	$(CC) -c $(CFLAGS) $< -o $@

wave_analyze:  examples/wave/*.c $(ebu_r128)
	$(CC) $(CFLAGS) $(LDFLAGS) $^ -o $@

ffmpeg_analyze:  examples/ffmpeg/*.c $(ebu_r128)
	$(CC) $(CFLAGS) $(LDFLAGS) $(LDFLAGS_FFMPEG) $^ -o $@


clean: 
	find . -type f -name *.o -exec rm -rf {} \;
	rm -f wave_analyze ffmpeg_analyze

rebuild: clean all