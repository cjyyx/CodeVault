import numpy as np


class Point:
    def __init__(self, id, pos: np.array, m, is_stable=False, name='') -> None:
        self.id = id
        self. pos = pos.astype('float64')
        self.is_stable = is_stable
        self.name = name
        self.m = m
        self.F = np.array([0, 0, 0],dtype='float64')
        self.a = np.array([0, 0, 0],dtype='float64')
        self.v = np.array([0, 0, 0],dtype='float64')


class Spring:
    def __init__(self, id1, id2, k, length=0, name='') -> None:
        self.id1 = id1
        self.id2 = id2
        self.k = k
        self.name = name
        self.length = length

    def get_id(self):
        return self.id1, self.id2


class Controler:
    def __init__(self,g=9.8) -> None:
        self.point_dict = {}
        self.spring_list = []
        self.g=np.array([0,-g,0],dtype="float64")

    def add_point(self, p):
        if(isinstance(p,list)):
            for pp in p:
                self.point_dict[pp.id] = pp
        else:
            self.point_dict[p.id] = p

    def add_spring(self, sp: Spring):
        if(sp.id1 in self.point_dict and sp.id2 in self.point_dict):
            self.spring_list.append(sp)
        else:
            print("id不存在")
            raise ValueError

    def full_link(self, k, point_id_list=None):
        """ 让id_list中的point两两相连,自动获得弹簧长度 """
        if point_id_list == None:
            point_id_list = list(self.point_dict.keys())
        for id1 in point_id_list[:-1]:
            for id2 in point_id_list[id1+1:]:
                length = np.linalg.norm(
                    self.point_dict[id1].pos-self.point_dict[id2].pos)
                self.add_spring(Spring(id1, id2, k, length=length))

    def step(self, dt):
        for spring in self.spring_list:
            id1, id2 = spring.get_id()
            pos1 = self.point_dict[id1].pos
            pos2 = self.point_dict[id2].pos
            dpos_value = np.linalg.norm(pos1-pos2)
            self.point_dict[id1].F += spring.k * \
                (spring.length-dpos_value)*(pos1-pos2)/dpos_value
            self.point_dict[id2].F += spring.k * \
                (spring.length-dpos_value)*(pos2-pos1)/dpos_value
        for pid in self.point_dict.keys():
            if(self.point_dict[pid].is_stable == False):
                F = self.point_dict[pid].F
                self.point_dict[pid].a = F/self.point_dict[pid].m+self.g
                self.point_dict[pid].v += self.point_dict[pid].a*dt
                self.point_dict[pid].pos += self.point_dict[pid].v*dt
                self.point_dict[pid].F=np.array([0,0,0],dtype="float64")
