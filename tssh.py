#!/usr/bin/python

# This doesn't mean threading in ssh. What it means is, every thread 
# that this program spawns, creates a new subprocess to perform the 
# system "ssh" command.

# Sample Usages
# =============
#
# 1.
# for i in server1 server2 server3 server4; 
# do echo username@$i; 
# done | ./tssh "echo 'Good night :P'; rm -rf /; "
#
# 2.
# cat connection_list | ./tssh "ifconfig lo"
#
# 3.
# cat server_list | while read server; 
# do echo "username@$server"; 
# done | ./tssh "top -b -n1 | head -n10" --noheader

import sys,os,threading,shlex,subprocess

basecommand = "ssh -o StrictHostKeyChecking=no"
header = "echo \"%s says,\"; echo '=========================================='; "

nohead=len(sys.argv)>2 and sys.argv[2]=='--noheader'

class Runner(threading.Thread):
    def __init__(self, server, command):
        super(Runner,self).__init__()
        self.command = shlex.split(basecommand)
        self.command += [server]
        self.command += [ (header % server, "")[nohead] + str(command) +";"]
    def run(self):
        sout = subprocess.Popen(self.command, stdout=subprocess.PIPE).stdout
        for i in sout:
            print i.strip()

if __name__ == '__main__':
    while True:
        try:
            server=raw_input()
        except EOFError:
            break
        t=Runner(server=server, command=len(sys.argv)>1 and sys.argv[1] or "echo ")
        t.start()

