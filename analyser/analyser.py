import time

class Analyser:
    def __init__(self) -> None:
        self.class_start_time=time.time()
        self.data={}

    def reset(self)->None:
        self.start_time=time.time()

    def point(self,p:str)->None:
        if p not in self.data.keys():
            self.data[p]=[]

        self.data[p].append(time.time()-self.start_time)

        self.start_time=time.time()

    def __del__(self)->None:
        class_total_time=time.time()-self.class_start_time
        print('记录时长（秒）:{}'.format(class_total_time))

        for item in self.data.items():
            p=item[0]
            d=item[1]

            print('\n记录：{}'.format(p))

            total_time=sum(d)
            print('共用时（秒）：{}'.format(total_time))

            mean_time=total_time/len(d)
            print('平均用时（秒）：{}'.format(mean_time))

            print('占比：{}%'.format(int(100*total_time/class_total_time)))