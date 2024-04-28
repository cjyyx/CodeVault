from control_parameters import *

def GD_fit(net,eval,n,LR=0.1,dx=0.1):

    # ana=Analyser()

    for b in range(n):
        for i in range(get_parameter_size(net)):

            # ana.reset()
            loss=eval(net)
            # ana.point('eval_1')

            para=get_parameter(net,i)
            set_parameter(net,i,para+dx)
            # ana.point('para_1')

            d_loss=eval(net)-loss
            # ana.point('eval_2')

            if d_loss==0:
                continue
            grad=d_loss/dx
            new_pare=para-LR*(loss/grad)
            set_parameter(net,i,new_pare)
            # ana.point('para_2')

        if b%10==0:
            print(loss.numpy()[0])
