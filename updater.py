import requests
import logger
import traceback

global username, reponame
username, reponame = 'gamingwithevets', 'sneky'

def check_updates(currver, prerelease = False, showupdate = False):
	try:
		logger.log('[UPDATER] Begin checking for Sneky updates.')
		versions = []
		try:
			i = 0
			while True:
				response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases')
				versions.append(response.json()[i]['tag_name'])
				i += 1
		except:
			pass
		if 'v' + currver not in versions:
			try:
				if response.json()['message'] == 'API rate limit exceeded for ' + requests.get('https://api.ipify.org').content.decode('utf8') + '. (But here\'s the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)':
					logger.log('[UPDATER] GitHub API rate limit exceeded!\nSkipping update process.')
					return False, True, False, None, None, None
				else:
					logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					return False, True, None, None, None
			except:
				pass
		response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/v' + currver)
		currvertime = response.json()['published_at']
		if not prerelease:
			response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/latest')
			if response.json()['tag_name'] != 'v' + currver and response.json()['published_at'] > currvertime:
				logger.log('[UPDATER] Updates available. User has been asked to update.', allowprint = False)
				return True, False, False, 'v.' + response.json()['tag_name'][1:], response.json()['name'], response.json()['body']
			else:
				logger.log('[UPDATER] Sneky is up to date.')
				return False, False, False, None, None, None
		else:
			for version in versions:
				response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/' + version)
				if currvertime < response.json()['published_at']:
					logger.log('[UPDATER] Updates available. User has been asked to update.', allowprint = False)
					return True, False, False, 'v.' + response.json()['tag_name'][1:], response.json()['name'], response.json()['body']
				else:
					logger.log('[UPDATER] Sneky is up to date.')
					return False, False, False, None, None, None
	except:
		logger.log('[UPDATER] An error occurred while checking for updates!\n' + traceback.format_exc() + '\nSkipping update process.')
		return False, True, False, None, None, None