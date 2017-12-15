import socket
import time, sys

BUF_SIZE = 1024

SENDER = 8000
RECEIVER = 8001
AGENT = 8002
CACHE_SIZE = 32


class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket that is used to receive messages
        self.sock.bind(('127.0.0.1', RECEIVER))

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket that is used to send messages
        self.agent_address = ('127.0.0.1', AGENT) # agent address

    def send_to_agent(self, msg):
        self.s.sendto(msg, self.agent_address)

    def receive_from_agent(self, buf_size):
        return self.sock.recvfrom(buf_size)

def deal_with_packet(msg):
    num = int(msg.split('#')[1])
    message = msg.split('#')[2]
    return num, message


if __name__ == '__main__':

    f = open('result.txt', 'w+')
    receiver = Receiver()

    sequence_num = 0
    cache = ''
    cache_num = 0
    while True:
        buf, addr = receiver.receive_from_agent(BUF_SIZE)
        packet_num, message = deal_with_packet(buf)
        if message == 'fin':
            f.write(cache)
            print "flush"
            print "send\tfinack"
            receiver.send_to_agent('receiver#ACK#0')
            break

        print "recv\tdata\t#"+str(packet_num)
        if packet_num == sequence_num +1:
            cache = cache+message
            cache_num = cache_num+1
            if cache_num >= CACHE_SIZE: # flush
                f.write(cache)
                cache = ''
                cache_num = 0
                print "flush"
            sequence_num = sequence_num+1
            receiver.send_to_agent('receiver#ACK#'+str(sequence_num))
            print "send\tack\t#"+str(sequence_num)
        else:
            receiver.send_to_agent('receiver#ACK#'+str(sequence_num))
            print "send\tack\t#"+str(sequence_num)
    f.close()