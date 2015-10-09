#dbconnector settings
databaseAddress = 'localhost'
databaseUser = 'DATABASEUSERNAME'
databaseUserPass = 'DATABASEUSERPASS'
databaseName = 'DATABASENAME'
#twitchconnector settings
twitchServer = 'irc.twitch.tv'
twitchPort = 6667
twitchChannel = '#CHANNELNAME' #Make sure to include the #
twitchBotUsername = 'BOTNAME'
twitchBotPassword = 'use twitch kraken open authentication'
#misc settings
logSite = ''
subMessage = ""
resubMessage = "" #use %s for months TODO: will use try: if %s isn't there

#things that'd break the bot if you changed them
currentInternalVersion = '1' #different from release numbers, this is used when I change mysql or core functionality and require a system update