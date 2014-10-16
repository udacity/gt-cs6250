#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <arpa/inet.h>
#include <netinet/in.h>
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

	int tfo = 1;

	if(argc >= 4 && (atoi(argv[3]) == 0)) {
		tfo = 0;
	}

	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	memset(&server_address, 0, sizeof(struct sockaddr_in));
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = inet_addr(argv[1]);
	server_address.sin_port = htons(atoi(argv[2]));

	int qlen = 5;
	char *data = "GET REQUEST STAND-IN";

	if(tfo) {
		sendto(sockfd, data, strlen(data)+1, MSG_FASTOPEN, (struct sockaddr *)&server_address, sizeof(struct sockaddr_in));
	}
	else {
		connect(sockfd, (struct sockaddr *)&server_address, sizeof(struct sockaddr_in));
		send(sockfd, data, strlen(data)+1, 1);
	}
	int connected = 1;
	char *buf = (char *)malloc(256);

	while(connected) {
		int len = recv(sockfd, buf, 128, 0);
		if(len == -1) {
			connected = 0;
		}
		else if(len != 0) {
			buf[len] = 0;
			printf("%s", buf);
		}
	}

	close(sockfd);
}
