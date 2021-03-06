'''
Program Description
    - Introduce a class with methods add and remove
    - How to carry out the RLock() call within the class

Rlock()
    - Use a Rlock() object, if you only want the thread that acquires a lock to release it
    - The Rlock() object has two methods:
        + acquire()
        + release()
    - It is useful when you want to have a thread-safe access from outside the class and use the same methods from inside the class
'''

import threading
import time


class Box(object):
    lock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.lock.acquire()
        self.total_items += n
        Box.lock.release()

    def add(self):
        Box.lock.acquire()
        self.execute(1)
        Box.lock.release()

    def remove(self):
        Box.lock.acquire()
        self.execute(-1)
        Box.lock.release()


# These two functions run n in separate threads and call the Box's methods
def adder(box, items):
    while items > 0:
        print("adding 1 item in the box\n")
        box.add()
        time.sleep(5)
        items -= 1


def remover(box, items):
    while items > 0:
        print("removing 1 item in the box")
        box.remove()
        time.sleep(5)
        items -= 1


#  Program build some threads and make sure it works
if __name__ == "__main__":
    items = 5
    print("putting %s items in the box " % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("%s items still remain in the box " % box.total_items)
