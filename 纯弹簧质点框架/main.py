import numpy as np
import vpython as vp
from framework import *


vp.scene.height = 600
vp.scene.width = 800

plane = vp.box(
    pos=vp.vec(0, -1.5, 0),
    height=0.001,
    width=5,
    length=5,
    cloor=vp.color.white
)

con = Controler(g=2)

# 1
p0=Point(0, np.array([0, 0, 0]), 1,is_stable=True)
p1=Point(1, np.array([1/2, 0, 1]), 1)
p2=Point(2, np.array([1/2, 1, 0]), 1)
p3=Point(3, np.array([1/2, 0, -1]), 1)
p4=Point(4, np.array([1/2, -1, 0]), 1)

p2.v[2]=10
p4.v[2]=-10

# 2
# p0=Point(0, np.array([0, 0, 0]), 1,is_stable=True)
# p1=Point(1, np.array([0, 0.55, 1]), 1)
# p2=Point(2, np.array([1, 1/2, 0]), 1)
# p3=Point(3, np.array([0, 0.45, -1]), 1)
# p4=Point(4, np.array([-1, 1/2, 0]), 1)

# p2.v[2]=10
# p4.v[2]=-10

con.add_point([p0,p1,p2,p3,p4])


con.full_link(1000)

draw_point_list = []
draw_spring_list = []
for i in range(con.point_dict.__len__()):
    draw_point_list.append(vp.sphere(radius=0.05, color=vp.color.green))
for i in range(con.spring_list.__len__()):
    draw_spring_list.append(vp.cylinder(radius=0.02, color=vp.color.red))

dt = 0.01
while 1:
    vp.rate(100)
    con.step(dt)

    for i, pid in enumerate(con.point_dict.keys()):
        p = con.point_dict[pid]
        d = draw_point_list[i]
        d.pos = vp.vec(p.pos[0], p.pos[1], p.pos[2])
    for i in range(draw_spring_list.__len__()):
        s = con.spring_list[i]
        p1 = con.point_dict[s.id1]
        p2 = con.point_dict[s.id2]
        d = draw_spring_list[i]
        d.pos = vp.vec(p1.pos[0], p1.pos[1], p1.pos[2])
        dp = p2.pos-p1.pos
        d.axis = vp.vec(dp[0], dp[1], dp[2])
