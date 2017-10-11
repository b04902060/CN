import socket # Include library
import string
import ConfigParser


class ChatBot:
	def __init__(self, channel, nickname, site, port):
		self.channel = channel
		self.nickname = nickname
		self.irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.irc.connect((site,port))
		self.irc.send("USER "+ self.nickname +" "+ self.nickname +" "+ self.nickname +" :Goodhat's bot\n")
		self.irc.send("NICK "+ self.nickname + '\n')
		self.irc.send("PRIVMSG nickserv :iNOOPE\r\n")
		self.irc.send("JOIN " + self.channel + '\n')
		self.n = 9

	def talk(msg):
		self.irc.send('PRIVMSG '+ self.channel +' :'+ msg +'\r\n')

	def run(self):

		while self.n > 0:  #ignore the initial messages
			self.text = self.irc.recv(2040)
			self.n = self.n-1

		self.text = self.irc.recv(2040)
		print self.text
		
		if self.text.find('PING') != -1: 
			self.irc.send('PONG ' + self.text.split() [1] + '\r\n')
		if len(self.text.split()) > 3:
			if self.text.split()[3] == ':@repeat':
				if len(self.text.split()) > 4:
					self.talk(self.text.split(" ", 4)[-1])

			if self.text.split()[3] == ':@convert':
				if len(self.text.split()) > 4:
					number = self.text.split()[4]
					if number[0] == '0' and number[1] == 'x' and all(c in '0123456789abcdef' for c in number[2:]):
						i = int(number,0)
						self.talk(str(i))
					elif number.isdigit():
						i = hex(int(number))	
						self.talk(str(i))

			if self.text.split()[3] == ':@help':
				self.talk('@repeat <Message>')
				self.talk('@convert <Number>')
				self.talk('@ip <String>')

			if self.text.split()[3] == ':@ip':
				if len(self.text.split()) > 4:
					self.ip = self.text.split()[4]
					if self.ip.isdigit() and len(self.ip)>3 and len(self.ip)<13:
						for i in range(1,len(self.ip),1):
							for j in range(i+1,len(self.ip),1):
								for k in range(j+1,len(self.ip),1):
										self.valid(i,j,k)
		

	def talk(self, msg):
		self.irc.send('PRIVMSG '+ self.channel +' :'+ msg +'\r\n')

	def valid(self, i, j, k):
		p1 = self.ip[0:i]
		p2 = self.ip[i:j]
		p3 = self.ip[j:k]
		p4 = self.ip[k:]
		#self.talk(self.ip[0:i]+'.'+self.ip[i:j]+'.'+self.ip[j:k]+'.'+self.ip[k:])
		
		if ((len(self.ip[0:i]) == 1 and self.ip[0:i][0] == '0') or ((self.ip[0:i][0] != '0') and int(self.ip[0:i])<256)):
			if ((len(self.ip[i:j]) == 1 and self.ip[i:j][0] == '0') or ((self.ip[i:j][0] != '0') and int(self.ip[i:j])<256)):
				if ((len(self.ip[j:k]) == 1 and self.ip[j:k][0] == '0') or ((self.ip[j:k][0] != '0') and int(self.ip[j:k])<256)):
					if ((len(self.ip[k:]) == 1 and self.ip[k:][0] == '0') or ((self.ip[k:][0] != '0') and int(self.ip[k:])<256)):
						self.talk(self.ip[0:i]+'.'+self.ip[i:j]+'.'+self.ip[j:k]+'.'+self.ip[k:])
		

def main():

	nickname = 'b04902060'
	site = 'irc.freenode.net'
	port = 6667
	
	
	f = open('config','r')
	channel = f.read(2048)[6:-2]
	
	mybot = ChatBot(channel, nickname, site, port)

	mybot.talk("Hello, I am robot.")
	while True:	
		mybot.run()

if __name__ == "__main__":
    main()







