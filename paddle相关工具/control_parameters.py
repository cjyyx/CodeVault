import paddle
import numpy as np

def get_parameter(net,index):
    '''得到指定index的参数，返回tensor'''
    parameters=net.parameters()

    for tensor in parameters:
        if index >= tensor.size:
            index-=tensor.size
        else:
            flat=paddle.reshape(tensor,[tensor.size])
            return flat[int(index)]

def get_parameter_size(net):
    '''得到参数size，返回np.int'''
    parameters=net.parameters()

    size=0
    for tensor in parameters:
        size+=tensor.size
    return size

def set_parameter(net,index,value):
    '''设置指定index的参数的值'''
    parameters=net.parameters()

    for tensor in parameters:
        if index >= tensor.size:
            index-=tensor.size
        else:
            shape=tensor.shape
            flat=paddle.reshape(tensor,[tensor.size])
            flat[int(index)]=value
            tensor=paddle.reshape(flat,shape)
            return

