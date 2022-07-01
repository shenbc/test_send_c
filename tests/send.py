import math
from ctypes import *
from multiprocessing import Pool
import numpy as np

GRADIENT_NUM_PER_PACKET = 128
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
pool_num = 5

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

def send(local_para):
    # gradient_list = local_para.cpu().numpy()
    # gradient_list = local_para.to('cpu').numpy()
    # gradient_list = torch.tensor(local_para, device = 'cpu')
    # gradient_list = np.array(local_para)
    # gradient_list = gradient_list.astype(np.float)
    gradient_list = local_para
    gradient_list = (gradient_list * 100000000).astype(np.int32)

    
    pool = Pool(pool_num)
    gradient_list = np.append(gradient_list, np.zeros(GRADIENT_SIZE * AGGREGATOR_SIZE - PARA_LEN, dtype=np.int32))
    step = math.ceil(AGGREGATOR_SIZE / pool_num)
    # segmentation fault 问题？
    # send_grad(dst_ip, gradient_list[i * GRADIENT_SIZE:(i + step) * GRADIENT_SIZE], i,)
    for i in range(0, AGGREGATOR_SIZE, step):
        if (i + step) * GRADIENT_SIZE <= GRADIENT_SIZE * AGGREGATOR_SIZE:
            pool.apply_async(send_grad, (dst_ip, gradient_list[i * GRADIENT_SIZE:(i + step) * GRADIENT_SIZE], i,))
            # send_queue.add_task(send_grad, parent_ips, gradient_list[i*GRADIENT_SIZE:(i+step)*GRADIENT_SIZE], i)
        else:
            pool.apply_async(send_grad, (dst_ip, gradient_list[i * GRADIENT_SIZE:], i,))
            # send_queue.add_task(send_grad, parent_ips, gradient_list[i*GRADIENT_SIZE:], i)

    # send_queue.join()
    pool.close()
    pool.join()
    
def single_process_send():
    test_data=np.arange(100000)
    c_send_wrapper(test_data, 0, int(len(test_data) / GRADIENT_NUM_PER_PACKET), ip2int(dst_ip_str),0,0)
    

if __name__ =="__main__":
    single_process_send()