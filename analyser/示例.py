from analyser import Analyser
import time

ana = Analyser()

for _ in range(5):
    ana.reset()
    time.sleep(0.05)
    ana.point('p1')
    time.sleep(0.02)
    ana.point('p2')
    time.sleep(0.1)
    ana.point('p3')
