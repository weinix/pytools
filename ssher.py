#!/usr/bin/env python

import subprocess
import threading
import sys,os,shlex

basecommand = "ssh -o StrictHostKeyChecking=no"
header = "echo -n  \"%s: \";  "


class Ssher(object):
    #output = {'alive': [], 'dead': []} # Populated while we are running
    hosts = [] # List of all hosts/servers in our input queue
    cmd = ""

    # How many ping process at the time.
    thread_count = 4

    # Lock object to keep track the threads in loops, where it can potentially be race conditions.
    lock = threading.Lock()

    def Runner(self, server):
        # Use the system ping command with count of 1 and wait time of 1.
        command = shlex.split(basecommand)
        command += [server]
        command += [ header % server  + str(self.cmd) +";"]
        output = subprocess.Popen(command, stdout=subprocess.PIPE).stdout
        for i in output:
            print i.strip()

    def pop_queue(self):
        server = None

        self.lock.acquire() # Grab or wait+grab the lock.

        if self.hosts:
            server = self.hosts.pop()

        self.lock.release() # Release the lock, so another thread could grab it.

        return server

    def dequeue(self):
        while True:
            server = self.pop_queue()

            if not server:
                return None

            #result = 'alive' if self.ping(server) else 'dead'
            self.Runner(server)
            #self.status[result].append(server)

    def start(self):
        threads = []

        for i in range(self.thread_count):
            # Create self.thread_count number of threads that together will
            # cooperate removing every server in the list. Each thread will do the
            # job as fast as it can.
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        # Wait until all the threads are done. .join() is blocking.
        [ t.join() for t in threads ]


if __name__ == '__main__':
    tssh = Ssher()
    tssh.thread_count = 5
    tssh.hosts = [
        'root@grunt2', 'root@grunt115', 'root@grunt32', 'root@grunt117'
        ]
    tssh.cmd = "uptime"

    tssh.start()
