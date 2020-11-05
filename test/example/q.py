#!/usr/bin/env python
import time
from threading import *
import Queue


class Producer(Thread):

    def __init__(self, itemq):
        """
        Initialize a new item.

        Args:
            self: (todo): write your description
            itemq: (todo): write your description
        """
        Thread.__init__(self)
        self.itemq=itemq
        return

    def run(self):
        """
        Runs loop.

        Args:
            self: (todo): write your description
        """

        itemq=self.itemq
        i=0
        for j in range(10):
            print(currentThread(), "Produced One Item:", i)
            itemq.put(i, 1)
            i+=1
            time.sleep(1)
            pass
        return


class Consumer(Thread):

    def __init__(self, itemq):
        """
        Initialize a new item.

        Args:
            self: (todo): write your description
            itemq: (todo): write your description
        """
        Thread.__init__(self)
        self.itemq=itemq
        return

    def run(self):
        """
        Run all items in the queue.

        Args:
            self: (todo): write your description
        """
        itemq=self.itemq

        for j in range(4):
            time.sleep(2)
            it=itemq.get(1)
            print(currentThread(), "Consumed One Item:", it)
            pass
        return

if __name__=="__main__":

    q=Queue.Queue(10)

    pro=Producer(q)
    cons1=Consumer(q)
    cons2=Consumer(q)

    pro.start()
    cons1.start()
    cons2.start()
    pro.join()
    cons1.join()
    cons2.join()
    pass
