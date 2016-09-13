from socketclient import mysocket


s = mysocket()
s.connect('localhost',80)
print s.myreceive()
cmd = ''
while cmd != "EXIT;":
    cmd = raw_input(">")
    s.mysend(cmd)
    print 'Received: '+s.myreceive()
s.close()
