#include"send.h"

void _send_gradients(__u32 *tensor_array, int packet_num, __u32 dst_ip, int worker_id, __u32 aggregator_index, int tensor_index) {
    // TODO: remove socket inition from this function.
    int socket_fd;
	struct sockaddr_in sock_send;
    memset(&sock_send, 0, sizeof(struct sockaddr_in));
    sock_send.sin_family = AF_INET;
	sock_send.sin_addr.s_addr = htonl(dst_ip);

	if ((socket_fd = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)) < 0) {
	    perror("ERROR: Failed to create raw socket.\n");
		exit(-1);
	}

    int send_buff_size = 4096 * 4096;
    setsockopt(socket_fd,SOL_SOCKET,SO_SNDBUF,&send_buff_size,sizeof(send_buff_size));

    int bitmap = 1 << (worker_id-1);
    
    clock_t start, end;
    start=clock();

    for (int i=0; i<packet_num; i++){
        struct packet_t packet;

        packet.worker_bitmap = htonl(bitmap);
        packet.aggregator_index= htonl(aggregator_index);
        packet.gradient_index = htonl(tensor_index + i);
        memcpy(packet.gradient, tensor_array + i * TENSOR_NUM_PER_PACKET, TENSOR_NUM_PER_PACKET * sizeof(__u32));

        // for endian conversion
        for (int j=0; j<TENSOR_NUM_PER_PACKET ; j++)
        {
            packet.gradient[j] = htonl(packet.gradient[j]);
        }
        
	    if(sendto(socket_fd, &packet, sizeof(struct packet_t), 0, (struct sockaddr *)&sock_send, sizeof(struct sockaddr_in)) < 0){
            perror("ERROR: Failed to call sendto()");
		    exit(-1);
        }
    }

    end = clock();
    printf("(C++) Time consumed: %lf s\n", (double)(end - start) / CLOCKS_PER_SEC);

	return;
}

void _thread_send_gradients(int thread_id, int thread_num, __u32 *tensor_array, int array_len){
    int element_num_per_thread= array_len/thread_num;
    int start_index = thread_id *  element_num_per_thread;
    int packet_num_per_thread = element_num_per_thread/TENSOR_NUM_PER_PACKET;
    
    _send_gradients(&tensor_array[start_index], packet_num_per_thread, inet_addr("172.16.210.32"),1,1,1);
}

void multiple_threads_send_gradient(__u32 *tensor_array, int array_len, int thread_num){
    thread_pool = new std::thread*[thread_num];
    
    clock_t start, end;
    start=clock();
    for (int i=0; i < thread_num; i++){
        thread_pool[i] = new std::thread(_thread_send_gradients, i, thread_num, tensor_array, array_len);
    }

    for (int i=0; i < thread_num; i++){
        thread_pool[i]->join();
    }
    end=clock();
    printf("(C++) Total time consumed: %lf s\n", (double)(end - start) / CLOCKS_PER_SEC);
}

// int main(int argc, char **argv){
//     int thread_num=20;
    
//     const __u32 buffer_size=10000;
//     __u32 buffer_value[buffer_size];
//     printf("Size of data: %ld MB\n", buffer_size/1024/1024*sizeof(int));
    
//     for (__u32 i=0; i < buffer_size; i++){
//         buffer_value[i]=htonl(i);
//     }

//     clock_t start, end;
//     start=clock();
    
//     _send_gradients(buffer_value, buffer_size/TENSOR_NUM_PER_PACKET, inet_addr("172.16.200.32"),1,1,1);
    
//     end=clock();
//     printf("Total time consumed: %lf s\n", (double)(end - start) / CLOCKS_PER_SEC);
    

//     start=clock();

//     multiple_threads_send_gradient(buffer_value, buffer_size, thread_num);

//     end = clock();
//     printf("Total time consumed: %lf s\n", (double)(end - start) / CLOCKS_PER_SEC);
    
//     return 0;
// }
