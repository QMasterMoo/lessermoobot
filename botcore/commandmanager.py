import datetime
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
        self.quoteTime = datetime.datetime.now() - datetime.timedelta(seconds=10)
        self.modList = ['moomasterq']#as long as this isn't empty the bot will work


    def manage(self, userName, data, db, serv):
        """
        Invokes the various hardcoded managers
        Support for other commands will come in the future
        """
        self.db = db
        self.data = data.split(' ')
        self.serv = serv
        #time things
        self.currentTime = datetime.datetime.now()
        self.currentMinute = self.currentTime.minute
        self.utcTime = datetime.datetime.utcnow()
        #managers
        self._subManager(userName)
        self._quoteManager(userName)
        self._highlightManager(userName)
        #mod managers
        if userName in self.getModList():
            self._historyManager()
            self._logManager()
            self._nextGame()


    def getModList(self):
        """
        Returns the mod list in a list
        See issue #15
        """
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


    def _historyManager(self):
        """
        Manages the finding and executing of the !history userName command
        """
        if self.data[0] == '!history':
            try:
                self.logger.logToFileHistory(self.data[1] , 
                    self._historyUser(self.data[1], int(self.data[2])) )
                self.serv.msg("%s/history/%s.txt" % (logSite, self.data[1]))
            except:
                self.logger.logToFileHistory(self.data[1] , 
                    self._historyUser(self.data[1], 200) ) #200 is default messages logged
                self.serv.msg("%s/history/%s.txt" % (logSite, self.data[1]))


    def _logManager(self):
        """
        Manages the finding and executing of the !log command
        """
        if self.data[0] == '!log':
            try: #The database object allow retrieving the usernames from the list
                self.logger.logToFile(self._log(int(self.data[1])), self.db)
                self.serv.msg("%s/log.txt" % logSite)
            except:
                self.logger.logToFile(self._log(1000), self.db) #1000 is default messages logged
                self.serv.msg("%s/log.txt" % logSite)


    def _quoteManager(self, userName):
        """
        does everything with quotes
        """
        #Makes sure the command wasn't used too recently
        if self.data[0] == '!quote':
            #Checks if the time is 20 seconds greater than the last time the command was used
            offCooldown = self.currentTime - datetime.timedelta(seconds=20) > self.quoteTime
            if offCooldown:
                #If the above is true, it resets the quote time
                self.quoteTime = self.currentTime
        if self.data[0] == '!quote' and (offCooldown or userName in self.getModList()):
            """
            Abusing a try/except in order to manage the quotes
            So in case it's an invalid quote id when deleting nothing actually happens
            """
            try:
                #Manages the adding of quotes
                if self.data[1].lower() == 'add' and userName in self.getModList():
                    out = ""
                    #Rebuilds the output
                    for line in self.data[2:]:
                        out += line + ' '
                    #If there was no quote give a sassy response
                    if out == "":
                        self.serv.msg("Actually write something!")
                    else:
                        #remove trailing whitespace
                        out = out[:-1]
                        #Insert into quote table
                        qid = self.db.insertQuote(userName, str(out))
                        #Output quote id
                        self.serv.msg("Quote Added! (#%s)" % str(qid))
                #Manages the retrieving of quotes with the keyword 'get' 'getquote' or 'id'
                elif self.data[1].lower() == 'get' or self.data[1].lower() == 'getquote' or self.data[1].lower() == 'id':
                    #Casts the quote number as an integer and retrieves it
                    quote = self.db.queryQuote(int(self.data[2]))
                    self.serv.msg(quote)
                #Manages deleting a quote
                elif self.data[1] == 'delete' and userName in self.getModList():
                    #This is the quote deletion key that makes sure 
                    if self.data[2] == 'yes_im_sure':
                        #Casts the quote deletion id
                        qid = int(self.data[3])
                        #Deletes it
                        self.db.deleteQuote(qid)
                        self.serv.msg("Quote #%s deleted :'(" % str(qid))
                    else:
                        #Specifies that a user needs to say the deletion key to delete it
                        self.serv.msg("please specify if you are sure you want to delete it")
                #Another way to retrieve a quote
                else:
                    #Creates the quote id
                    qid = int(self.data[1])
                    quote = self.db.queryQuote(qid)
                    self.serv.msg(quote) 
            #If it's not an extra command it just goes and queries
            except:
                quote = self.db.queryQuote(0)
                self.serv.msg(quote)


    def _highlightManager(self, userName):
        if self.data[0].lower() == '!highlight':
            try:
                krakenJSON = urllib2.urlopen("https://api.twitch.tv/kraken/streams/%s" % twitchChannel[1:])
                krakenJSON = json.loads(krakenJSON.read().decode('utf-8'))
                createdAt = krakenJSON["stream"]["created_at"]
                #2015-11-19T23:44:58Z --> 23:44:58
                createdAt = createdAt[-9:-1].split(':')
                #creates datetime obj for vod timestamp
                vodtime = datetime.datetime(self.currentTime.year, self.currentTime.month, self.currentTime.day,
                             int(createdAt[0]), int(createdAt[1]), int(createdAt[2]))
                #converts from utc to localtimezone
                timeZoneConversion = self.utcTime - self.currentTime
                vodtime -= timeZoneConversion
                #calculates uptime, subtracts some time since highlights happen late
                timeDiff = self.currentTime - vodtime
                timeDiff -= datetime.timedelta(seconds=75)
                #creates the variables for timestamping the vod
                uptimeHours, remainder = divmod(timeDiff.seconds, 3600)
                uptimeMinutes, uptimeSeconds = divmod(remainder, 60)
                #gets vod url
                vodJSON = urllib2.urlopen("https://api.twitch.tv/kraken/channels/%s/videos?broadcasts=true" % twitchChannel[1:])
                vodJSON = json.loads(vodJSON.read().decode('utf-8'))
                latestVod = vodJSON["videos"][0]["_id"]
                latestVod = latestVod[1:]#removes the v
                vodLink = "%s requests: http://twitch.tv/%s/v/%s?t=%ih%im%is" % \
                            (userName, twitchChannel[1:], latestVod, uptimeHours, uptimeMinutes, uptimeSeconds)
                #inserts into vodurl as channel_highlights
                self.db.insertMessageIntoLog((twitchChannel[1:] + "_highlights"), str(self.currentTime)[:19], 
                                            'HIGHLIGHT', vodLink)

            except Exception as e:
                print(e)
            



    def _subManager(self, userName):
        """
        This method takes in the serv object (connection to twitch server)
        which is used to send message to the twitch server thanking people for subbing
        """
        if userName == "twitchnotify":
            subName = self.data[0]
            if self.data[1] == 'subscribed':
                subMonth = self.data[3]
                self.serv.msg(resubMessage % (subName, subMonth))
            else:
                self.serv.msg(subMessage % subName)


    def _nextGame(self):
        """
        !nextGame implementation
        """
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


    def _readListOfString(self, inList):
        """
        Helper command for _nextGame() that reads the list of strings and splits them up into real input
        """
        if inList != None:
            return inList[2:-2].split('\', \'')


    def _historyUser(self, userName, length):
        """
        Queries database for last x messages for the user
        """
        return self.db.queryHistory(userName, length)


    def _log(self, length):
        """
        Queries database for last x messages
        """
        return self.db.queryLog(length)

