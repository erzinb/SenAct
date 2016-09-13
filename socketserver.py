import socket
import threading
import time
from socketclient import mysocket

class myThread (threading.Thread):
    id = 0
    def __init__(self, mysocket):
        threading.Thread.__init__(self)
        self.id = myThread.id
        myThread.id += 1
        self.socket = mysocket
    def run(self):
        print "Starting %d" % self.id
        # Get lock to synchronize threads
        #threadLock.acquire()
        receiveSend(self.socket, "USER:;", self.id)
        # Free lock to release next thread
        #threadLock.release()

def receiveSend(s, firstmsg, id):
    global runserver
#    s.mysend(firstmsg)
    cmd = ''
    while cmd != 'EXIT;':
        cmd = s.myreceive()
        print "%d: %s: RECEIVED(%s)" % (id, time.ctime(time.time()), cmd)
#        time.sleep(2)
        s.mysend(cmd)
        print "%d: %s: SENT(%s)" % (id, time.ctime(time.time()), cmd)
        if cmd == 'STOPSERVER;':
            runserver = False
        break;
    s.close()
    s = None

threadLock = threading.Lock()
threads = []
runserver = True

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(('localhost', 80))
#become a server socket
serversocket.listen(5)

while runserver:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    #now do something with the clientsocket
    #in this case, we'll pretend this is a threaded server
#    ct = client_thread(clientsocket)
#    ct.run()
    s = mysocket(clientsocket)
# Create new threads
    t = myThread(s)
    t.start()
    threads.append(t)
#testVar = raw_input("Ask user for something.")
    #break

# Wait for all threads to complete
for t in threads:
    print t.socket
    if t.socket != None:
        t.socket.close()

print "Exiting Main Thread"
