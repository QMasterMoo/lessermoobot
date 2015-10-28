import datetime #will be used for command cooldowns
import json
import urllib2
from writer import writer
from config import logSite, subMessage, resubMessage, twitchChannel

class commandmanager:

    def __init__(self):
        #Eventually will init commands from file x
        self.logger = writer()
        self.currentMinute = 0
        self.lastMinute = -1
        self.modList = ['moomasterq']#as long as this isn't empty the bot will work

    """
    Invokes the various hardcoded managers
    Support for other commands will come in the future
    """
    def manage(self, userName, data, db, serv):
        self.db = db
        self.data = data.split(' ')
        self.serv = serv
        self.currentMinute = datetime.datetime.now().minute
        self._subManager(userName)#passing serv allows sending multiple messages
        #Not sure how to do without variables since I don't want to call it twice
        if userName in self.getModList():
            self._historyManager()
            self._logManager()
            self._nextGame()

    """
    Returns the mod list in a list
    See issue #15
    """
    def getModList(self):
        if self.currentMinute != self.lastMinute: #Anti flood measure for tmi
            self.lastMinute = self.currentMinute
            self.modList = ['moomasterq']#resets mod list
            modJSON= urllib2.urlopen("https://tmi.twitch.tv/group/user/%s/chatters" % twitchChannel[1:])
            modJSON = json.loads(modJSON.read().decode("utf-8"))
            for userLevel in ['staff','admins','global_mods','moderators']:
                if modJSON["chatters"][userLevel]:
                    for user in modJSON["chatters"][userLevel]:
                        self.modList.append(user)
        return self.modList

    """
    Manages the finding and executing of the !history userName command
    """
    def _historyManager(self):
        if self.data[0] == '!history':
            try:
                self.logger.logToFileHistory(self.data[1] , 
                    self._historyUser(self.data[1], int(self.data[2])) )
                self.serv.msg("%s/history/%s.txt" % (logSite, self.data[1]))
            except:
                self.logger.logToFileHistory(self.data[1] , 
                    self._historyUser(self.data[1], 200) ) #200 is default messages logged
                self.serv.msg("%s/history/%s.txt" % (logSite, self.data[1]))

    """
    Manages the finding and executing of the !log command
    """
    def _logManager(self):
        if self.data[0] == '!log':
            try: #The database object allow retrieving the usernames from the list
                self.logger.logToFile(self._log(int(self.data[1])), self.db)
                self.serv.msg("%s/log.txt" % logSite)
            except:
                self.logger.logToFile(self._log(1000), self.db) #1000 is default messages logged
                self.serv.msg("%s/log.txt" % logSite)

    """
    TODO: Write !quote methods
        adds quote and such to a seperate table on mysql, not planned for 
        initial release, see #12
    """

    """
    This method takes in the serv object (connection to twitch server)
    which is used to send message to the twitch server thanking people for subbing
    """
    def _subManager(self, userName):
        if userName == "twitchnotify":
            subName = self.data[0]
            if self.data[1] == 'subscribed':
                subMonth = self.data[3]
                self.serv.msg(resubMessage % (subName, subMonth))
            else:
                self.serv.msg(subMessage % subName)

    """
    !nextGame implementation
    """
    def _nextGame(self):
        if self.data[0].lower() == '!nextgame':
            gameList = self._readListOfString(self.logger.readCustomFile('nextgame'))
            try:
                if self.data[1].lower() == 'clearlist' or self.data[1].lower() == 'clear':
                    gameList = ['EMPTY']
                    self.logger.writeCustomFile('nextgame', gameList)
                    self.serv.msg("Cleared the list!")
                elif self.data[1].lower() == 'add':
                    self.serv.msg("To add a user you don't need the word 'add', just put the username after !nextgame")
                elif self.data[1].lower() == 'remove':
                    try:
                        gameList.remove(self.data[2])
                        self.logger.writeCustomFile('nextgame', gameList)
                    except:
                        self.serv.msg("User: \'%s\' isn't in the list, please check spelling" % self.data[2])
                #if it's not a command it appends the next chunk after the split (userame)
                #to the list and rewrites the file
                else:
                    #Removes the empty from the list
                    try:
                        gameList.remove('EMPTY')
                    except:
                        pass
                    gameList.append(self.data[1])
                    self.logger.writeCustomFile('nextgame', gameList)
            #I abuse except to just print the list otherwise
            except:
                out = "Current list: "
                if gameList != None:
                    for line in gameList:
                        out += line + ', ' 
                self.serv.msg(out[:-2])

    """
    Helper command for _nextGame() that reads the list of strings and splits them up into real input
    """
    def _readListOfString(self, inList):
        if inList != None:
            return inList[2:-2].split('\', \'')

    """
    Queries database for last x messages for the user
    """
    def _historyUser(self, userName, length):
        return self.db.queryHistory(userName, length)

    """
    Queries database for last x messages
    """
    def _log(self, length):
        return self.db.queryLog(length)


