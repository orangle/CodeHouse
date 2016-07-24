all: tcp.exe dayserver.exe dayclient.exe

tcp.exe: tcp_simple_server.c
	gcc tcp_simple_server.c -lpthread -o tcp.exe -v

dayserver.exe: daytimetcpsrv.c
	gcc daytimetcpsrv.c -lunp -o dayserver.exe

dayclient.exe: daytimetcpcli.c
	gcc daytimetcpcli.c -lunp -o dayclient.exe

clean:
	rm *.exe

