import socket, sys
import time

BUF_SIZE = 1024

SENDER = 8000
RECEIVER = 8001
AGENT = 8002
THRESHOLD = 16


class Sender:
    def __init__(self, threshold):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket that is used to receive messages
        self.sock.bind(('127.0.0.1', SENDER))

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket that is used to send messages
        self.agent_address = ('127.0.0.1', AGENT) # agent address

        self.threshold = threshold
        self.window_size = 1 # winodw size
        self.latest_sent = 0 # how many windows are used
        self.latest_acked = 0
        self.all_ok = 0

    def send_to_agent(self, msg):
        self.s.sendto('sender#'+msg, self.agent_address)

    def receive_from_agent(self, buf_size):
        return self.sock.recvfrom(buf_size)

    def increase_window(self):
        if self.window_size < self.threshold:
            self.window_size = self.window_size*2
        else:
            self.window_size = self.window_size+1

    def penalty(self):
        self.threshold = max(self.threshold/2, 1)
        self.window_size = 1

def ack_num(msg):
    if msg.split('#')[1] == 'ACK':
        return int(msg.split('#')[2])


if __name__ == '__main__':

    f = open("data.txt", 'r')
    sender = Sender(THRESHOLD)

    terminate_flag1 = 0
    terminate_flag2 = 0
    buf_list = []
    sequence_num = 0
    while True:
        for i in range(sender.window_size): # send messages in the window
            if len(buf_list) - i > 0:
                num, buf = buf_list[i]
                sender.send_to_agent(str(num)+'#'+buf)
                print "resnd\tdata\t#"+str(num)+',\twinSize = '+str(sender.window_size) 
            else:
                buf = f.read(1000)
                if len(buf) < 1000:
                    terminate_flag1 = 1
                sequence_num = sequence_num + 1
                buf_list.append((sequence_num, buf))
                sender.send_to_agent(str(sequence_num)+'#'+buf)
                print "send\tdata\t#"+str(sequence_num)+',\twinSize = '+str(sender.window_size)  
            sender.latest_sent = sender.latest_sent + 1
            if terminate_flag1 == 1:
                break

        while True: # receive ack
            try:
                sender.sock.settimeout(1)
                buf, addr = sender.receive_from_agent(BUF_SIZE)
                order = ack_num(buf)
                print "recv\tack\t#"+str(order)
                if order == sender.latest_acked+1:
                    sender.latest_acked = sender.latest_acked+1
                    buf_list = buf_list[1:]
                else: # fail to receive all acks in the window.
                    sender.penalty()
                    sender.latest_sent = sender.latest_acked # restore latest sent
                    break
                if sender.latest_acked == sender.latest_sent:
                    terminate_flag2 = 1
                    sender.increase_window()
                    break
            except socket.timeout :
                sender.penalty()
                print "time\tout,\t\tthreshold = "+str(sender.threshold)
                sender.latest_sent = sender.latest_acked # restore latest sent
                break

        if terminate_flag1 == 1 and sender.latest_acked == sender.latest_sent and len(buf_list) == 0:
            break

    flag = 0
    while True:
        sender.send_to_agent("0#fin")
        print "send\tfin"
        while True:
            try:
                sender.sock.settimeout(1)
                buf, addr = sender.receive_from_agent(BUF_SIZE)
                if buf.split('#')[1] == 'ACK' and buf.split('#')[2] == '0':
                    print "recv\tfinack"
                    flag = 1
                    break
            except socket.timeout:
                break
        if flag == 1:
            break
    