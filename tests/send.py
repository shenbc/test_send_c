from ctypes import *
from multiprocessing import Pool
import sys
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

TENSOR_NUM_PER_PACKET = 128
AGGREGATOR_SIZE = 199665
PARA_LEN = 25557032

dst_ip_str = b"172.16.210.33" # must tran to byte type through b"172.xxx

_send = cdll.LoadLibrary("./send.so") 

_send.multiple_threads_send_gradient.argtypes = [
    POINTER(c_uint32), 
    c_int, 
    c_int,
    # c_uint,
    c_char_p,
    c_int,
    c_int,
    c_int
]


def ip2int(ip):
    ip_list = ip.strip().split('.')
    ip_int = int(ip_list[0])*256**3+int(ip_list[1])*256**2+int(ip_list[2])*256**1+int(ip_list[3])*256**0
    return ip_int

def c_send_wrapper(gradient: "numpy.array", array_len, thread_num, dst_ip, worker_id, aggregator_index, tensor_index):
    c_pointer_gradient=gradient.ctypes.data_as(POINTER(c_uint32))
    c_array_len=c_int(array_len)
    c_thread_num=c_int(thread_num)
    
    # c_dst_ip=c_uint(dst_ip)
    c_dst_ip=c_char_p(dst_ip)
    c_worker_id=c_int(worker_id)
    c_aggregator_index=c_int(aggregator_index)
    c_tensor_index=c_int(tensor_index)

    _send.multiple_threads_send_gradient(c_pointer_gradient, c_array_len, c_thread_num, c_dst_ip, c_worker_id, c_aggregator_index, c_tensor_index)

def single_process_send(data):
    c_send_wrapper(data, int(len(data) / TENSOR_NUM_PER_PACKET), ip2int(dst_ip_str),0,0,0)
    
def multi_process_send(process_num, data):
    start=time.time()

    process_pool = Pool(process_num)
    total_packet = int(len(data) / TENSOR_NUM_PER_PACKET)
    packet_num_per_process= int(total_packet / process_num)
    remained_packets= int(total_packet % process_num)
    offset=0

    for i in range(process_num):
        if i != process_num-1:
            process_pool.apply_async(c_send_wrapper, (data[offset: offset+packet_num_per_process * TENSOR_NUM_PER_PACKET],  packet_num_per_process, ip2int(dst_ip_str), 0, 0,offset))
        else:
            process_pool.apply_async(c_send_wrapper, (data[offset : ], packet_num_per_process + remained_packets, ip2int(dst_ip_str), 0, 0, offset))
        
        offset+=packet_num_per_process * TENSOR_NUM_PER_PACKET
    
    process_pool.close()
    process_pool.join()

    end=time.time()
    print("{} processes cost: {} sec; Throuthput {} GBps".format(str(process_num), str(end-start), str(data_size/(end-start))))

# multi process send through concurrent.futures.ThreadPoolExecutor
def multi_process_send_futures(process_num, data):
    start=time.time()

    executor=ThreadPoolExecutor()
    total_packet = int(len(data) / TENSOR_NUM_PER_PACKET)
    packet_num_per_process= int(total_packet / process_num)
    remained_packets= int(total_packet % process_num)
    offset=0
    f = []

    for i in range(process_num):
        if i != process_num-1:
            f.append(executor.submit(c_send_wrapper, data[offset: offset+packet_num_per_process * TENSOR_NUM_PER_PACKET],  packet_num_per_process, ip2int(dst_ip_str), 0, 0,offset))
        else:
            f.append(executor.submit(c_send_wrapper, data[offset : ], packet_num_per_process + remained_packets, ip2int(dst_ip_str), 0, 0, offset))
        
        offset+=packet_num_per_process * TENSOR_NUM_PER_PACKET
    
    
    executor.shutdown(wait=True)
    # for i in range(process_num):
    #     print(f'task{i}是否完成: {f[i].done()}')
    end=time.time()
    print("{} processes cost: {} sec; Throuthput {} GBps".format(str(process_num), str(end-start), str(data_size/(end-start))))

# multi process send through concurrent.features.ProcessPoolExecutor
def multi_process_send_futures_P(process_num, data):
    start=time.time()

    executor=ProcessPoolExecutor()
    total_packet = int(len(data) / TENSOR_NUM_PER_PACKET)
    packet_num_per_process= int(total_packet / process_num)
    remained_packets= int(total_packet % process_num)
    offset=0
    f = []

    for i in range(process_num):
        if i != process_num-1:
            f.append(executor.submit(c_send_wrapper, data[offset: offset+packet_num_per_process * TENSOR_NUM_PER_PACKET],  packet_num_per_process, ip2int(dst_ip_str), 0, 0,offset))
        else:
            f.append(executor.submit(c_send_wrapper, data[offset : ], packet_num_per_process + remained_packets, ip2int(dst_ip_str), 0, 0, offset))
        
        offset+=packet_num_per_process * TENSOR_NUM_PER_PACKET
    
    
    executor.shutdown(wait=True)
    # for i in range(process_num):
    #     print(f'task{i}是否完成: {f[i].done()}')
    end=time.time()
    print("{} processes cost: {} sec; Throuthput {} GBps".format(str(process_num), str(end-start), str(data_size/(end-start))))

if __name__ =="__main__":
    data_len=10000000
    thread_num=30
    test_data=np.arange(data_len, dtype=np.int32)
    data_size=(sys.getsizeof(test_data)-96)/1024/1024/1024 # GB
    print("Test data {} GB".format(str(data_size)))

    start= time.time()
    # c_send_wrapper(test_data, data_len, thread_num, ip2int(dst_ip_str), 0, 0, 0)
    c_send_wrapper(test_data, data_len, thread_num, dst_ip_str, 0, 0, 0)
    end=time.time()
    print("Total cost: {} sec; Throuthput {} GBps".format(str(end-start), str(data_size/(end-start))))

    
    