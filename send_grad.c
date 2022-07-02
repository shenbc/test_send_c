#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>

#include <linux/if_ether.h>
#include <linux/in.h>


#define GRADIENT_SIZE 199665

struct payload_t {
    __u32 gradient_index;
    __u32 bitmap;
	__u32 gradient[GRADIENT_SIZE];
} __attribute__((packed));


int send_grad_thread(__u32 * gradient_array, int packet_num, int start_index, __u32 dst_ip, int node_id)
{
    print("fun send_grad_thread is running ")
    int  socket_fd;
	struct sockaddr_in sock_send;
    memset(&sock_send, 0, sizeof(struct sockaddr_in));
	sock_send.sin_family = AF_INET;
	sock_send.sin_addr.s_addr = htonl(dst_ip);

	if ((socket_fd = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)) < 0)
	{
	    perror("Build Raw Socket Error\n");
		exit(-1);
	}

    int size = 256 * 1024; //larger may work ！！！
    setsockopt(socket_fd,SOL_SOCKET,SO_SNDBUF,&size,sizeof(size));

    int bitmap = 1 << (node_id-1);
    int i;


    for (i=0; i<packet_num; i++)
    {
        struct payload_t payload;
        payload.bitmap = htonl(bitmap);
        payload.gradient_index = htonl(start_index + i);
        memcpy(payload.gradient, gradient_array + GRADIENT_SIZE * i, GRADIENT_SIZE * sizeof(__u32));

        int j;
        for (j=0; j<GRADIENT_SIZE ; j++)
        {
            payload.gradient[j] = payload.gradient[j];
        }

	    if(sendto(socket_fd, &payload, sizeof(struct payload_t), 0, (struct sockaddr *)&sock_send, sizeof(struct sockaddr_in)) < 0)
        {
            perror("sendto() Error\n");
		    exit(-1);
        }

    }

	return 0;
}

void helloworld()

{

printf("dll has called!\n");

return ;

}

// int main()
// {
//     send_grad_thread(0,1,1,0,1);
//     return 0;
// }