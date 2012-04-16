# coding: utf-8
#!/usr/bin/python

import time
import bisect


class Scheduler:

    """
        修改自 schedule.py
        1、 增加 event的  repeat 功能
        2、 修改id方式，使得可以删除掉 repeat的 event
        3、 简化，直接将time作为时间函数
    """

    def __init__(self):
        self.queue = []
        self.event_map = {}
        self.max_id = 0

    def enterabs(self, initial_offset, id, action, repeat_offset, argument):
        event = initial_offset, id, action, repeat_offset, argument
        self.event_map[id] = event
        bisect.insort(self.queue, event)
        return id

    def enter(self, delay, id, action, repeat_offset, argument):
        return self.enterabs(time.time() + delay, id, action, repeat_offset, argument)

    def getID(self):
        self.max_id += 1
        return self.max_id

    def cancel(self, id):
        event = self.event_map.get(id, None)
        if event:
            del self.event_map[id]
            self.queue.remove(event)

    def empty(self):
        return len(self.queue) == 0

    def run(self):
        q = self.queue
        while q:
            initial_offset, id, action, repeat_offset, argument = q[0]
            now = time.time()
            if now < initial_offset:
                #time.sleep(time - now)
                return
            else:
                del q[0]
                del self.event_map[id]
                if repeat_offset > 0:
                    self.enter(repeat_offset, id, action, repeat_offset, argument)
                void = action(id, argument)
                time.sleep(0)   # Let other threads run


import threading

class GlobalTimer(threading.Thread):

    def __init__(self, interval = 0.1):
        threading.Thread.__init__(self)
        self.start_time = 0
        self.interval = interval
        self.sched = Scheduler()

    def addTimer(self, initial_offset, callback, repeat_offset=0, user_arg=None):
        return self.sched.enter(initial_offset, self.sched.getID(), callback, repeat_offset, user_arg)

    def delTimer(self, timer_id):
        self.sched.cancel(timer_id)

    def uptime(self):
        if self.start_time > 0:
            return time.time() - self.start_time
        return 0

    def run(self):
        self.start_time = time.time()
        while self.start_time > 0:
            self.sched.run()
            time.sleep(self.interval)

    def stop(self):
        self.start_time = 0

global_timer = GlobalTimer()
global_timer.start()

