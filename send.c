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


#define TENSOR_NUM 199665

struct payload_t {
    __u32 worker_bitmap;
    __u32 aggregator_index;
    __u32 gradient_index;
	__u32 gradient[TENSOR_NUM];
} __attribute__((packed));


void send_gradients(__u32 *gradient_array, int offset, int packet_num, __u32 dst_ip, int worker_id, __u32 aggregator_index) {
    
    printf("(C): Sending Gradients...");
    
    int socket_fd;
	struct sockaddr_in sock_send;
    memset(&sock_send, 0, sizeof(struct sockaddr_in));
    sock_send.sin_family = AF_INET;
	sock_send.sin_addr.s_addr = htonl(dst_ip);

	if ((socket_fd = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)) < 0) {
	    perror("ERROR: Failed to create raw socket.\n");
		exit(-1);
	}

    int send_buff_size = 256 * 1024;
    setsockopt(socket_fd,SOL_SOCKET,SO_SNDBUF,&send_buff_size,sizeof(send_buff_size));

    int bitmap = 1 << (worker_id-1);

    for (int i=0; i<packet_num; i++){
        struct payload_t payload;

        payload.worker_bitmap = htonl(bitmap);
        payload.aggregator_index= htonl(aggregator_index);
        payload.gradient_index = htonl(offset + i);
        memcpy(payload.gradient, gradient_array + i * TENSOR_NUM, TENSOR_NUM * sizeof(__u32));

        // for (int j=0; j<TENSOR_NUM ; j++)
        // {
        //     payload.gradient[j] = payload.gradient[j];
        // }
        
	    if(sendto(socket_fd, &payload, sizeof(struct payload_t), 0, (struct sockaddr *)&sock_send, sizeof(struct sockaddr_in)) < 0){
            perror("ERROR: Failed to call sendto()\n");
		    exit(-1);
        }
    }

	return;
}
