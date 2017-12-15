import socket
import time, sys
import random

BUF_SIZE = 1024

SENDER = 8000
RECEIVER = 8001
AGENT = 8002
L_RATE = 0.2

class Agent:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', AGENT))

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender_address = ('127.0.0.1', SENDER)
        self.receiver_address = ('127.0.0.1', RECEIVER) 

    def send_to_receiver(self, msg):
        self.s.sendto(msg, self.receiver_address)

    def send_to_sender(self, msg):
        self.s.sendto(msg, self.sender_address)

    def receive_data(self, buf_size):
        return self.sock.recvfrom(buf_size)

def deal_with_packet(msg):
    num = int(msg.split('#')[1])
    message = msg.split('#')[2]
    return num, message

def ack_num(msg):
    if msg.split('#')[1] == 'ACK':
        return int(msg.split('#')[2])



if __name__ == '__main__':
    agent = Agent()

    total = 0.0
    loss = 0.0
    while True:
        buf, addr = agent.receive_data(BUF_SIZE)
        if 'receiver' in buf:
            print "get\tack\t#"+str(ack_num(buf))
            agent.send_to_sender(buf)
            print "fwd\tack\t#"+str(ack_num(buf))

        if 'sender' in buf:
            num, tmp = deal_with_packet(buf)
            print "get\tdata\t#"+str(num)
            total = total+1

            if random.uniform(0, 1) > L_RATE:
                agent.send_to_receiver(buf)
                print "fwd\tdata\t#"+str(num)+",\tloss rate = "+str(loss/total)
            else:
                loss = loss+1
                print "drop\tdata\t#"+str(num)+",\tloss rate = "+str(loss/total)





