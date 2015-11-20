from config import twitchServer, twitchPort, twitchChannel, twitchBotUsername, twitchBotPassword
import socket

class twitchconnector:
	#RME: creates connection to server
	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((twitchServer, twitchPort))
		self.irc.send("CAP REQ :twitch.tv/membership \n")
		self.irc.send("CAP REQ :twitch.tv/commands \n")
		self.irc.send("PASS " + twitchBotPassword + "\n")
		self.irc.send("NICK "+ twitchBotUsername +"\n")
		self.irc.send("USER "+ twitchBotUsername + "\n")
		self.irc.send("JOIN " + twitchChannel + "\n")


	def ping(self):
		"""
		responds with ping
		"""
		self.irc.send("PONG :ping\n")


	def msg(self, message):
		"""
		sends a PRIVMSG, which just sends it to the chat
		"""
		self.irc.send("PRIVMSG " + twitchChannel + " :" + message + "\r\n")


	def msgRaw(self, message):
		"""
		sends a msg as is to the server, generally not a good idea
		unless you know exactly what you are doing
		"""
		self.irc.send(message)

	
	def getData(self):
		"""
		gets data from the server
		"""
		return self.irc.recv(2048)