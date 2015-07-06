#!/usr/bin/env python

import subprocess
import threading
import sys,os,shlex
import argparse

basecommand = "ssh -o StrictHostKeyChecking=no "
header = "echo -n  \"%s: \";  "


class Ssher(object):
    #output = {'alive': [], 'dead': []} # Populated while we are running
    hosts = [] # List of all hosts/servers in our input queue
    cmd = ""
    user = ""

    # How many ping process at the time.
    thread_count = 4

    # Lock object to keep track the threads in loops, where it can potentially be race conditions.
    lock = threading.Lock()

    def Runner(self, server):
        # Use the system ping command with count of 1 and wait time of 1.
        command = shlex.split(basecommand )
        command += [ self.user + "@" + server]
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

    parser = argparse.ArgumentParser(description='Multithreading ssh')
    parser.add_argument('command', action="store", type=str,
                        help="Command to execute")
    parser.add_argument('-t', action="store", dest="threads_no", type=int, default=6,
                        help="Number of threads")
    parser.add_argument('-u', action="store", dest="user", type=str, default="root",
                        help="user name")
    parser.add_argument('-k', action="store", dest="keyfile", type=str,
                        help="key file")
    
    args = parser.parse_args()

    servers = []
    while True:
        try:
            server = raw_input()
            servers.append( server )
        except EOFError:
            break

    tssh = Ssher()
    tssh.thread_count = args.threads_no 
    
    tssh.hosts =  servers 
    tssh.cmd = args.command
    tssh.user = args.user

    tssh.start()
