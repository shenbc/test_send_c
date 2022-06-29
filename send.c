#include"send.h"

void send_gradients(__u32 *gradient_array, int offset, int packet_num, __u32 dst_ip, int worker_id, __u32 aggregator_index) {
    
    printf("(C): Sending Gradients...\n");
    
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
    
    clock_t start, end;
    start=clock();

    for (int i=0; i<packet_num; i++){
        struct payload_t payload;

        payload.worker_bitmap = htonl(bitmap);
        payload.aggregator_index= htonl(aggregator_index);
        payload.gradient_index = htonl(offset + i);
        memcpy(payload.gradient, gradient_array + i * TENSOR_NUM, TENSOR_NUM * sizeof(__u32));
        
	    if(sendto(socket_fd, &payload, sizeof(struct payload_t), 0, (struct sockaddr *)&sock_send, sizeof(struct sockaddr_in)) < 0){
            perror("ERROR: Failed to call sendto()");
		    exit(-1);
        }
    }

    end = clock();
    printf("Time consumed: %lf s\n", (double)(end - start) / CLOCKS_PER_SEC);

	return;
}

// int main(int argc, char **argv){
//     __u32 buffer_value[1000000];

//     for (int i=0; i < 1000000; i++){
//         buffer_value[i]=htonl(i);
//     }
    
//     printf("Size of data: %ld MB\n", sizeof(__u32)*1000000/1024/1024);

//     send_gradients(buffer_value, 0, 1000000/TENSOR_NUM, inet_addr("172.16.200.32"),1,2);

//     return 0;
// }
