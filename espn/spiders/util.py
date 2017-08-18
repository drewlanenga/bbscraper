
def mmss2ss( mmss ):
	parts = mmss.split(':')
	return ( int(parts[0]) * 60 ) + int(parts[1])


team_template = { 'id': '', 'points': 0 }
teams = { 'home': team_template, 'visitor': team_template }

teams['home']['id'] = ''
teams['visitor']['id'] = ''

