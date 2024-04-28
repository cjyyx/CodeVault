import paddle
# from control_parameters import *
from GD_fit import *
from analyser import Analyser



def eval(net):
    x=paddle.linspace(-3,3,100)
    x=paddle.reshape(x,[x.size,1])
    y=x**2
    loss_fn=paddle.nn.MSELoss(reduction='mean')
    loss=loss_fn(net(x),y)
    return loss

net = paddle.nn.Sequential(
    paddle.nn.Linear(1, 8),
    paddle.nn.ReLU(),
    paddle.nn.Linear(8, 4),
    paddle.nn.ReLU(),
    paddle.nn.Linear(4, 1),
    paddle.nn.Tanh()
)

LR=1
dx=1

GD_fit(net,eval,1)



