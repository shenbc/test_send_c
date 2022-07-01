import math
from ctypes import *
from multiprocessing import Pool
import time
import numpy as np

TENSOR_NUM_PER_PACKET = 128
AGGREGATOR_SIZE = 199665
PARA_LEN = 25557032

_send = cdll.LoadLibrary("./send.so") 

_send.send_gradients.argtypes = [
    POINTER(c_uint32), 
    c_int, 
    c_int, 
    c_uint32, 
    c_int, 
    c_uint32
]

dst_ip_str = "172.16.200.32"
node_id = 1

def ip2int(ip):
    ip_list = ip.strip().split('.')
    ip_int = int(ip_list[0])*256**3+int(ip_list[1])*256**2+int(ip_list[2])*256**1+int(ip_list[3])*256**0
    return ip_int

def c_send_wrapper(gradient: "numpy.array", offset: int, packet_num, dst_ip: int, worker_id, aggregator_index):
    c_pointer_gradient=gradient.ctypes.data_as(POINTER(c_uint32))
    c_offset=c_int(offset)
    c_packet_num=c_int(packet_num)
    c_dst_ip=c_uint32(dst_ip)
    c_worker_id=c_int(worker_id)
    c_aggregator_index=c_uint32(aggregator_index)

    _send.send_gradients(c_pointer_gradient, c_offset, c_packet_num, c_dst_ip, c_worker_id, c_aggregator_index)
    
def single_process_send():
    test_data=np.arange(100000)
    c_send_wrapper(test_data, 0, int(len(test_data) / TENSOR_NUM_PER_PACKET), ip2int(dst_ip_str),0,0)
    
def multi_process_send(process_pool):
   
    test_data=np.arange(100000)
    
    total_packet = int(len(test_data) / TENSOR_NUM_PER_PACKET)
    packet_num_per_process= int(total_packet / process_num)
    remained_packets= int(total_packet % process_num)
    offset=0

    for i in range(process_num):
        if i != process_num-1:
            process_pool.apply_async(c_send_wrapper, (test_data, offset, packet_num_per_process, ip2int(dst_ip_str), 0, 0))
        else:
            process_pool.apply_async(c_send_wrapper, (test_data, offset, packet_num_per_process+ remained_packets, ip2int(dst_ip_str), 0, 0))

        offset+=packet_num_per_process * TENSOR_NUM_PER_PACKET

if __name__ =="__main__":
    start= time.time()
    single_process_send()
    end=time.time()
    print("Single process cost: {} sec.".format(str(end-start)))
    
    process_num=20
    process_pool = Pool(process_num)
    
    start= time.time()
    multi_process_send(process_pool)
    end=time.time()
    
    process_pool.close()
    process_pool.join()
    

    print("{} processes cost: {} sec.".format(str(process_num), str(end-start)))