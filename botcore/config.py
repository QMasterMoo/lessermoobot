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
logSite = 'log.website.com'
subMessage = "Thanks for subscribing %s"#The %s will become their name
resubMessage = "Thank you for subscribing %s for %s months!" #Make sure to include 2 %s. First is userName, second is Months
screenName = 'lmb'

#things that'd break the bot if you changed them
currentInternalVersion = '1' #different from release numbers, this is used when I change mysql or core functionality and require a system update
