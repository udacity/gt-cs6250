#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#define MSG_FASTOPEN 0x20000000
#define TCP_FASTOPEN 23

int main(int argc, char **argv) {
	int sockfd, port, n;
	struct sockaddr_in server_address;
	struct hostent *server;

	if(argc < 3) {
		exit(0);
	}

	sockfd = socket(AF_INET, SOCK_STREAM, 1);

	memset(&server_address, 0, sizeof(struct sockaddr_in));
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = inet_addr(argv[1]);
	server_address.sin_port = htons(atoi(argv[2]));

	int qlen = 5;
	bind(sockfd, (struct sockaddr *)&server_address, sizeof(struct sockaddr));
	setsockopt(sockfd, SOL_TCP, TCP_FASTOPEN, &qlen, sizeof(qlen));
	
	listen(sockfd, 1);
	socklen_t socksize = sizeof(struct sockaddr_in);
	struct sockaddr_in dest;
	int connection = accept(sockfd, NULL, 0);

	char buf[256];
	char *data = "test test";

	while(connection) {
		int len = recv(connection, buf, 128, 0);
		buf[len] = 0;
		printf("%s", buf);
		if(len == -1) {
			send(connection, data, strlen(data)+1, 0);
			close(connection);
			connection = accept(sockfd, NULL, 0);
		}
	}

	close(sockfd);
}
