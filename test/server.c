#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

#include <ctype.h>

void error (char *msg) {
    perror(msg);
    exit(1);
}

/*
	The BSD server creates a socket, uses bind to attach that socket to a port,
	and configures it as a listening socket.
	This allows the server to receive incoming connection requests.
	Afterwards, accept is called, which will block the socket,
	until an incoming connection request is received
*/
int main (int argc, char *argv[]) {
	int sockfd, newsockfd, portno, clilen, pid;
    char buffer[256];
	/* sockaddr_in: IPv4 Socket Address structure */
    struct sockaddr_in serv_addr, cli_addr;

	// control arguments
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
	portno = atoi(argv[1]);
	clilen = sizeof(cli_addr);

	/*
		SOCKET
		Creates a communication socket
		AF_INET means using IPv4
		SOCK_STREAM means using TCP
		use SOCK_DGRAM for UDP
		INADDR_ANY means all IP addresses accepted

		int socket(family, type, protocol)
	*/
	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
		error("ERROR opening socket");
	bzero((char *) &serv_addr, sizeof(serv_addr));	// bzero: function to clear buffer
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(portno);

	/*
		BINDING
		Assigns a name (local address) to a socket
		bind(socket descriptor, local address, address lenght)
	*/
	if ((bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr))) < 0)
		error("ERROR on binding");
	/*
		LISTEN
		Sets the socket in a listen mode
		listen(socket descriptor, queue size)
	*/
	listen(sockfd, 5);

	/* LOOP */
	while (true) {
		/*
			ACCEPT
			Accepts a connection request queued for a listening socket
			The function accept accepts a connection request queued for a listening socket.
			If a connection request is pending, accept removes the request from the queue,
			and a new socket is created for the connection.
			The original listening socket remains open and continues to queue new connection requests

			int accept(socket descriptor, client address, address lenght)
		*/
		if ((newsockfd = accept(sockfd, (struct sockaddr*) &cli_addr, &clilen)) < 0)
			error("ERROR on accept");

		/* fork, generating child */
		if ((pid = fork()) < 0) error("Error on fork");

		/* parent with pid > 0 */
		if (pid > 0) {
			/* close parent process side socket */
			close(newsockfd);
			}

		/* child with pid = 0 */
		else {
			

			/* lettura dalla socket */
			bzero(buffer, 256);
			if (read(newsockfd, buffer, 255) < 0)
				error("ERROR reading from socket");

			// debug print
			printf("%s\n", buffer);

			char reply[256]="token from client: ";

			for(int i = 15; i < 250;i++){
				if(buffer[i]=='\0') break;
				reply[i+2]=toupper(buffer[i]);
			}
			printf("%s\n", reply);

			/* scrittura su socket */
			if (write(newsockfd, reply, strlen(reply)) < 0)
				error("ERROR writing to socket");

		}
	}
	return 0; 
}

/* getHostname *//*
	char buf[87];
	int size=sizeof(buf);
	gethostname(buf, size); 
	char welcome[100]="welcome from ";
	strcat(welcome,buf);
*/