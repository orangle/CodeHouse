all: server.exe client.exe

server.exe: chat_server.c
	gcc chat_server.c -o server.exe -lpthread

client.exe: chat_client.c
	gcc chat_client.c -o client.exe -lpthread

client_keep.exe: chat_client_keepalive.c
	gcc chat_client_keepalive.c -o client_keep.exe -lpthread

client_hb.exe: chat_client_heartbeat.c
	gcc chat_client_heartbeat.c -o client_hb.exe -lpthread

clean:
	rm *.exe
