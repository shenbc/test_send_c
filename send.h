#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <thread>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <sched.h>

#define TENSOR_NUM_PER_PACKET 128

struct packet_t {
    __u32 worker_bitmap;
    __u32 aggregator_index;
    __u32 gradient_index;
	__u32 gradient[TENSOR_NUM_PER_PACKET];
} __attribute__((packed));

std::thread** thread_pool;

void _send_gradients(__u32 *tensor_array,int packet_num, __u32 dst_ip, int worker_id, __u32 aggregator_index, int tensor_index);
void _thread_send_gradients(int thread_id, int thread_num, __u32 *tensor_array, int array_len, char *dst_ip, int worker_id, int aggregator_index, int tensor_index);
extern "C"{
    void multiple_threads_send_gradient(__u32 *tensor_array, int array_len, int thread_num, char *dst_ip, int worker_id, int aggregator_index, int tensor_index);
}

inline void bindingCPU(int num) {
  int result;
  cpu_set_t mask;
  CPU_ZERO(&mask);
  CPU_SET(num, &mask);
  result = sched_setaffinity(0, sizeof(mask), &mask);
  if (result < 0) {
    printf("binding CPU fails\n");
    exit(1);
  }
}