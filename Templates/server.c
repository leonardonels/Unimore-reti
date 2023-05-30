/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void error(char *msg){
	perror(msg);
	exit(1);
}

/*		SERVER		*/
int main(int argc, char *argv[]){
	int sockfd, newsockfd, portno, clilen;
	int n;
	char buffer[256];
	struct sockaddr_in serv_addr, cli_addr;

	/* controllo argomenti */
	if (argc < 2) {
	fprintf(stderr,"ERROR, no port provided\n");
	exit(1);
	}

	/* descriptor, type: SOCK_STREAM o SOCK_DGRAM */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) {error("ERROR opening socket");}

	/* bzero funzione che azzera e ripulisce il buffer */
	bzero((char *) &serv_addr, sizeof(serv_addr));

	/* port number */
	portno = atoi(argv[1]);

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(portno);

	/* bind(descriptor, local address, address lenght), binding: operazione per fornire un numero di porta */
	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {error("ERROR on binding");}

	/* listen(descriptor, queue size), operazione per preparare il socket a ricevere una connessione */
	listen(sockfd, 5);
	clilen = sizeof(cli_addr);

	/* fork */
	int pid;
	while(1) {
		//Connection establishment
		newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		if(newsockfd < 0) {
			error("Error on accepting");
		}
	
		if((pid = fork()) < 0) {
			error("Error on fork");
		}
		if(pid == 0) {
			bzero(buffer,256);

			/* lettura dalla socket */
			n = read(newsockfd, buffer, 255);
			if (n < 0) {error("ERROR reading from socket");}

			printf("Here is the message: %s\n",buffer);
			n = write(newsockfd,"I got your message",18);
	
			if (n < 0) {error("ERROR writing to socket");}
		}
		else {
			close(newsockfd);
		}
	}

	/* non_fork */

//	/* accettazione nuova richiesta */
//	newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
//	if (newsockfd < 0) {error("ERROR on accept");}

//	bzero(buffer,256);

	/* lettura dalla socket */
//	n = read(newsockfd, buffer, 255);
//	if (n < 0) {error("ERROR reading from socket");}

//	printf("Here is the message: %s\n",buffer);

	/* scrittura su socket */	
//	n = write(newsockfd,"I got your message",18);
//	if (n < 0) {error("ERROR writing to socket");}

	return 0;
}

/* getHostname *//*
	char buf[87];
	int size=sizeof(buf);
	gethostname(buf, size); 
	char welcome[13]="welcome from ";
	strcat(welcome,buf);
*/
	/* scrittura su socket *//*
	n = write(newsockfd, welcome, 100);*/