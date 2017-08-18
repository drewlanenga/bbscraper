from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.xpathor import Selector
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.item import Item, Field
from string import Template
from datetime import datetime
import _mysql
import time
import json

class AllItem(Item):
		team = Field()
		games = Field()

class TeamItem(Item):
		name = Field()
		id = Field()

class ScheduleItem(Item):
		id = Field()
		home = Field()
		visitor = Field()
		score = Field()

class PlayerItem(Item):
		player = Field()

class PlayByPlaySpider(CrawlSpider):
		name = "playbyplay"
		allowed_domains = [ "espn.go.com" ]
		start_urls = [ "http://espn.go.com/mens-college-basketball/teams" ]

		_conn = _mysql.connect( "localhost", "jackboot", "", "ncaa_bb" )
		_year = '2013'
		_seasontype = '2'

		## the base parser starts on the overall team list and grabs all applicable teams
		## it then loops through each team for the given year and seasontype
		def parse(self, response):
				## template string for the query insertion
				template = Template("insert ignore into `teams_pbp` (`teamid`,`teamname`) values ('$teamid','$teamname')")

				hxs = Selector(response)

				teams = []

				for h5 in hxs.xpath('//h5'):
						#time.sleep( 5 )
						splat = h5.xpath('.//a/@href').extract()[0].encode('ISO-8859-1').split('/')
						url = "http://espn.go.com/mens-college-basketball/team/schedule/_/id/" + splat[7] + "/year/" + self._year + "/" + splat[8]
						
						print "hello team: " + splat[8]

						teamDict = {}
						teamDict['teamid'] = splat[7]
						teamDict['teamname'] = splat[8].replace("'","")

						self._conn.query(template.substitute(teamDict))

						request = Request( url, callback = lambda r: self.parseSchedule(r) )

						yield request

		## this parser takes the team's schedule and finds all of the game ids to look for
		## it also checks to see if the game id has already been logged (i.e. from another team's schedule)
		def parseSchedule(self, response):

				## template string for the query insertion
				template = Template("insert ignore into `schedule_pbp` (`gameid`,`homeid`,`visitid`,`homescore`,`visitscore`,`year`,`seasontype`,`gamedate`) values ('$gameid','$homeid','$visitid','$homescore','$visitscore','$year','$seasontype','$gamedate')")

				hxs = Selector(response)
				gamediv = hxs.xpath('//div[@class="mod-content"]')

				items = []

				team = response.url.split('/')[8]

				for game in gamediv:
						#time.sleep( 5 )
						## sleep for a bit
##					  time.sleep(4)

						trs = game.xpath('.//tr')

						for tr in trs:
								## this may be useless, but i don't know if scrapy needs it
								scheduleItem = ScheduleItem()

								item = {'gameid':'', 'homeid':'', 'visitid':'', 'homescore':'', 'visitscore':'', 'year':self._year, 'seasontype':self._seasontype, 'gamedate':''}

								opp = ''
								
								tmp = tr.xpath('.//li[@class="team-name"]')
								tmpLink = tr.xpath('.//li[@class="team-name"]/a')

								## make sure the row is an actual game
								if len(tmp) == 1 and len(tmpLink) == 1:

										## apparently some postponed/cancelled games still get a row -- we don't want those
										score = tr.xpath('.//li[@class="score"]')
										if len(score) > 0:

												rawGameDate = tr.xpath('.//td/text()').extract()[0].encode('ISO-8859-1');
												gamedate = datetime.strptime(rawGameDate,'%a, %b %d')

												## see if the game was played in the current game year or not
												gameyear = int(self._year)
												if gamedate.month > 7:
														gameyear = gameyear - 1

												item['gamedate'] = str(gameyear) + '-' + str(gamedate.month) + '-' + str(gamedate.day)


												opp = tmp[0].xpath('.//a/@href').extract()[0].encode('ISO-8859-1').split('/')[7]
												where = tr.xpath('.//li[@class="game-status"]/text()').extract()[0].encode('ISO-8859-1')

												status = ''
												statusHolder = tr.xpath('.//li[@class="game-status loss"]/span/text()')
												if len(statusHolder) > 0:
														status = 'loss'
												else:
														statusHolder = tr.xpath('.//li[@class="game-status win"]/span/text()')
														if len(statusHolder) > 0:
																status = 'win'

												statusIndex = {'home':'','visit':''}

												if where == '@':
														item['homeid'] = opp
														item['visitid'] = team

														if status == 'win':
																statusIndex = {'home': 1, 'visit': 0}
														elif status == 'loss':
																statusIndex = {'home': 0, 'visit': 1}
												else:
														item['homeid'] = team
														item['visitid'] = opp

														if status == 'win':
																statusIndex = {'home': 0, 'visit': 1}
														elif status == 'loss':
																statusIndex = {'home': 1, 'visit': 0}

												#scoreurl = score.xpath('.//a/@href').extract()[0].encode('ISO-8859-1').split('=')

												# better handle postponed or cancelled games in the schedule
												scoreurl = score.xpath('.//a/@href').extract()

												if len(scoreurl) > 0:
													scoreurl = scoreurl[0].encode('ISO-8859-1').split('=')

													## apparently some of the older games don't have boxscores and playbyplay summaries
													if len(scoreurl) == 2:
															item['gameid'] = scoreurl[1]

															## check if the game id has already been logged
															self._conn.query("select `gameid` from `schedule_pbp` where `gameid` = '" + item['gameid'] + "'")
															rs = self._conn.store_result()
															row = rs.fetch_row(0,1)

															## the game id hasn't been logged
															if len(row) == 0:
																	scores = score.xpath('.//a/text()').extract()[0].encode('ISO-8859-1').split('-')

																	item['homescore'] = scores[statusIndex['home']]
																	item['visitscore'] = scores[statusIndex['visit']]

																	self._conn.query(template.substitute(item))

																	## get the player stuff for the game
																	gameurl = "http://espn.go.com/ncb/playbyplay?gameId=" + item['gameid']
																	print gameurl

																	request = Request(gameurl,callback= lambda r: self.parsePlayByPlay(r))
																	# request = Request(gameurl,callback= lambda r: self.parseGame(r))
																	yield request
															else:
																	yield scheduleItem


		def parsePlayByPlay( self, response ):
			print "---------- PLAY BY PLAY ---------"

			gameid = response.url.split('=')[1]

			hxs = Selector( response )

			#
			#  figure out who is playing whom
			#

			matchup = hxs.xpath('//div[contains(@class,"matchup")]')[0]

			links = matchup.xpath('./div[contains(@class,"team")]/div[contains(@class,"team-info")]/h3/a/@href').extract()

			teamids = []
			for link in links:
				spat = link.split('/')
				teamids.append( spat[7] )


			#
			#  just grab stuff
			#

			plays = []

			rows = hxs.xpath('//table[contains(@class,"mod-data")]/tr')

			for row in rows:
				rowclass = row.xpath('@class').extract()[0]
				# make sure the row has 
				if rowclass == u'odd' or rowclass == u'even':
					values = []
					tds = row.xpath('./td')
					for td in tds:
						children = td.xpath('./*/text()').extract()
						if len(children):
							content = children
						else:
							content = td.xpath('./text()').extract()
							if len(content) == 0:
								content.append('')
						value = content[0].encode('ISO-8859-1')
						# just get rid of quotes the ghetto way
						if value == '\xa0':
							value = ''
						values.append( value )
					plays.append( values )


			game = { 'teamids': teamids, 'plays': plays }

			f = open( "/Users/lanenga/Documents/kaggle/ncaa/data/espn/playbyplay/" + gameid + ".json", "w+")
			print f
			json.dump( game, f )

			f.close()



		## this parser actually goes through the box score and logs everything
		def parseGame(self, response):
				print "hello game"
				hxs = Selector(response)

				## get the thead to see which columns are displayed and where and create the template string
				ths = hxs.xpath('//thead')[0].xpath('.//tr')[1].xpath('.//th/text()').extract()
				goodColumns = {'MIN':'min','FGM':'fgm','FGA':'fga','3PM':'threem','3PA':'threea','FTM':'ftm','FTA':'fta','OREB':'oreb','REB':'dreb','AST':'ast','STL':'stl','BLK':'blk','TO':'to','PF':'pf','PTS':'pts'}

				i = -2
				thMap = {}
				templateParts = {'part1':'insert ignore into `boxscores` (`gameid`,`teamid`,`playerid`,', 'part2':[], 'part3':") values ('$gameid','$teamid','$playerid',", 'part4':[],'part5':')'}
				for th in ths:
						th = th.encode('ISO-8859-1')

						splat = th.split('-')

						for split in splat:
								if split == 'A':
										split = splat[0][:-1] + split

								i = i + 1
								if goodColumns.keys().count(split) > 0:

										thMap[goodColumns[split]] = i

										templateParts['part2'].append("`" + goodColumns[split] + "`")
										templateParts['part4'].append("'$" + goodColumns[split] + "'")

				templateParts['part2'] = ','.join(templateParts['part2'])
				templateParts['part4'] = ','.join(templateParts['part4'])
				## template string for the query insertion
				template = Template(''.join(templateParts.values()))
#			   template = {'pmSet': Template("insert into `boxscores` (`gameid`,`playerid`,`min`,`fgm`,`fga`,`threem`,`threea`,`ftm`,`fta`,`oreb`,`dreb`,`reb`,`ast`,`stl`,`blk`,`to`,`pf`,`pm`,`pts`) values ('$gameid','$playerid','$min','$fgm','$fga','$threem','$threea','$ftm','$fta','$oreb','$dreb','$reb','$ast','$stl','$blk','$to','$pf','$pm','$pts')"),'pmNotSet': Template("insert into `boxscores` (`gameid`,`playerid`,`min`,`fgm`,`fga`,`threem`,`threea`,`ftm`,`fta`,`oreb`,`dreb`,`reb`,`ast`,`stl`,`blk`,`to`,`pf`,`pts`) values ('$gameid','$playerid','$min','$fgm','$fga','$threem','$threea','$ftm','$fta','$oreb','$dreb','$reb','$ast','$stl','$blk','$to','$pf','$pts')")}

				gameid = response.url.split('=')[1]

#			   matchup = hxs.xpath('//h1[@class="matchup "]')[0].xpath('.//a/@href').extract()
				matchup = hxs.xpath('//div[@class="matchup "]')[0].xpath('.//a/@href').extract()

				## loop through start/bench for each team
				table = hxs.xpath('//table[@class="mod-data"]')

				## team headers have the class team-color-strip
				strip = hxs.xpath('.//tr[@class="team-color-strip"]')

				i = 0
				for teamStrip in strip:

						teamid = matchup[i].encode('ISO-8859-1').split('/')[7]
						i = i + 1

						## get the next two tbodies from the 
						siblings = teamStrip.xpath('../following-sibling::tbody')[0:2]

						for tbody in siblings:
								## get each player
								for tr in tbody.xpath('.//tr'):

										## boolean to mark if tr is a row for a player
										isPlayer = False

										tds = tr.xpath('.//td/text()')
										tmp = tr.xpath('.//a/@href').extract()

										## the pm column is set
										if len(tmp) > 0:
												isPlayer = True
												playerid = tmp[0].encode('ISO-8859-1').split('/')[7]


										## player name is not a link
										if len(tmp) == 0:
												tds = tr.xpath('.//td/text()')


										if isPlayer:
												print "playerid: " + playerid


												## only players have 15 tds in their row
												if len(tds) > 10:

														tdList = []
														## add pertinent td results to the player array
														for td in tds:
																text = td.extract().encode('ISO-8859-1')

																test = text.split(', ')
																if len(test) == 2:
																		continue
																else:
																		test = text.split('-')
																		for value in test:
																				tdList.append(value)

														## make a dict object for the Template string substitution
														playerDict = {'gameid':gameid,'teamid':teamid,'playerid':playerid}

														for th in thMap:
																playerDict[th] = tdList[thMap[th]]

														#print(playerDict)

												## create the query from the template string and execute it
														self._conn.query(template.substitute(playerDict))


														item = PlayerItem()

														yield item
