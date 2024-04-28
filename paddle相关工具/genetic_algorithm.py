import random

def ran_index(n):
    '''
    返回的x越小，概率越高，且成线性关系
    
    x=0,1,...,n-1
    '''
    r=random.random()
    x=int(((4*r*n**2+4*r*n+1)**0.5-1)/2)
    x=n-1-x
    return x


def survive(net_list,survivor_num):
    '''返回survivor_num个生存的net，要求net_list中index越小越强'''
    survivor_list=[]
    for _ in range(survivor_num):
        survivor_list.append(net_list.pop(ran_index()))
    return survivor_list




if __name__=='__main__':
    li=[0]*10
    for _ in range(1000000):
        li[ran_index(10)]+=1

    print([a/li[-1] for a in li])
