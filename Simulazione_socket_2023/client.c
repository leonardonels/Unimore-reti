#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

void error(char *msg){
	perror(msg);
	exit(0);
}

/*		CLIENT		*/
int main(int argc, char *argv[]){

	int sockfd, portno, n;
	char buffer[256];

	struct sockaddr_in serv_addr;
	struct hostent *server;

	if (argc < 3) {
		fprintf(stderr,"usage %s hostname port\n", argv[0]);
		exit(0);
	}

	/* port number */
	portno = atoi(argv[2]);

	/* descriptor, type: SOCK_STREAM o SOCK_DGRAM */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) {error("ERROR opening socket");}

	server = gethostbyname(argv[1]);
	if (server == NULL) {
        	fprintf(stderr, "ERROR, no such host\n");
        	exit(0);
	}

	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
	serv_addr.sin_port = htons(portno);

	/* connect(descriptor, server address, address lenght), operazione per contattare un server che ha chiamato accept(), inizia la connessione */
	if (connect(sockfd, (const struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {error("ERROR connecting");}

	printf("Please enter the message: ");
	bzero(buffer, 256);
	fgets(buffer, 255, stdin);

	/* scrittura sulla socket */
	n = write(sockfd,buffer,strlen(buffer));
	if (n < 0) {error("ERROR writing to socket");}

	//bzero(buffer,256);

	/* lettura dalla socket */
	//n = read(sockfd,buffer,255);
	//printf("%s\n",buffer);
	//if (n < 0) {error("ERROR reading from socket");}

	return 0;
}
