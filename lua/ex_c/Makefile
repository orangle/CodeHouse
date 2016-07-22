all: sleep.so

sleep.so: sleep.c
	cc -bundle -undefined dynamic_lookup -o sleep.so sleep.c -llua
