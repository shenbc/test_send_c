from operator import mod
import sys
import math
from ctypes import *
from multiprocessing import Pool
import numpy as np
import torch
from utils.comm_utils import int_to_float, float_to_int

import torchvision.models as m

GRADIENT_SIZE = 128
AGGREGATOR_SIZE = 199665
PARA_LEN = 25557032

dst_ip = "172.16.200.8"
node_id = 1
pool_num = 5


def ip2int(ip):
    ip_list = ip.strip().split('.')
    ip_int = int(ip_list[0])*256**3+int(ip_list[1])*256**2+int(ip_list[2])*256**1+int(ip_list[3])*256**0
    return ip_int


def send_grad(dsp_ip, gradient_list, start_index):
    print("--------- Send gradient start: %d ---------" % start_index)

    gradient_len = len(gradient_list)
    gradient_array = (c_uint32 * gradient_len)()
    gradient_array[:] = gradient_list
    # gradient_array = (c_uint32 * gradient_len)(*gradient_list)
    packet_num = gradient_len // GRADIENT_SIZE
    dst_ip = ip2int(dsp_ip)

    send_grad_dll = cdll.LoadLibrary("./send_grad.o") # 务必用‘./’指明是当前目录下的

    send_grad_dll.send_grad_thread.argtypes = [POINTER(c_uint32 * gradient_len), c_int, c_int, c_uint32, c_int]
    send_grad_dll.send_grad_thread(gradient_array, packet_num, start_index, dst_ip, node_id)

    print("--------- Send gradient finish ---------")

    return


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
    


if __name__ =="__main__":
    model = m.vgg16().to('cpu')
    # para = torch.nn.utils.parameters_to_vector(model.parameters()).clone().detach().tolist()
    # send(float_to_int(para))
    # send(model.parameters())

    parameters = model.parameters()
    for p in parameters:
        numpy_para = p.detach().cpu().numpy()
        # print(type(numpy_para))
        # print(numpy_para.shape)
    send(numpy_para)