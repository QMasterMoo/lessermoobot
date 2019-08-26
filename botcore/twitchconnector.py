#from .config import twitchServer, twitchPort, twitchChannel, twitchBotUsername, twitchBotPassword
import socket
import ssl

class Message:
	def __init__(self, rawMessage):
		self.rawMessage = rawMessage

	def getRawMessage(self):
		return self.rawMessage

class twitchconnector:
	#RME: creates connection to server
	def __init__(self, config):
		self.hostname = 'irc.chat.twitch.tv'
		context = ssl.create_default_context()
		self._rawSocket = socket.create_connection((self.hostname, 6697))
		self.irc = context.wrap_socket(self._rawSocket, server_hostname=self.hostname)
		
		OAuthKey = config["OAuthKey"]
		BotUsername = config["BotUsername"]
		TwitchChannel = config["ChannelName"]
		self.irc.send("CAP REQ :twitch.tv/membership \n".encode())
		self.irc.send("CAP REQ :twitch.tv/commands \n".encode())
		self.irc.send(f"PASS {OAuthKey}\n".encode())
		self.irc.send(f"NICK {BotUsername}\n".encode())
		self.irc.send(f"USER {BotUsername}\n".encode())
		self.irc.send(f"JOIN {TwitchChannel}\n".encode())

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
		return self.irc.recv(4096)

	def getMessage(self):
		
		return Message(self.getData());

	def IsConnectionAlive(self):
		return True