import time as tm

running = True

t = 0.0
dt = 0.1

while running:
    # t = t + dt
    t += dt
    tm.sleep(0.1)
    print('Time: ', t)