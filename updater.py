
import logger
import traceback

global username, reponame
username, reponame = 'gamingwithevets', 'sneky'

def check_updates(currver, prerelease = False, showupdate = False):
	try:
		import requests
	except:
		logger.log('[UPDATER] Cannot check for Sneky updates because the \'requests\'\nmodule was not installed.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': True
		}
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
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
				return {
				'newupdate': False,
				'error': False,
				'unofficial': True
				}
		response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/v' + currver)
		try:
			if response.json()['message'] == 'API rate limit exceeded for ' + requests.get('https://api.ipify.org').content.decode('utf8') + '. (But here\'s the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)':
				logger.log('[UPDATER] GitHub API rate limit exceeded!\nSkipping update process.')
				return {
				'newupdate': False,
				'error': True,
				'exceeded': True
				}
			else:
				logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
				return {
				'newupdate': False,
				'error': False,
				'unofficial': True
				}
		except:
			pass
		currvertime = response.json()['published_at']
		if not prerelease:
			response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/latest')
			try:
				if response.json()['message'] == 'API rate limit exceeded for ' + requests.get('https://api.ipify.org').content.decode('utf8') + '. (But here\'s the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)':
					logger.log('[UPDATER] GitHub API rate limit exceeded!\nSkipping update process.')
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				pass
			if response.json()['tag_name'] != 'v' + currver and response.json()['published_at'] > currvertime:
				logger.log('[UPDATER] Updates available. User has been asked to update.', allowprint = False)
				return {
				'newupdate': True,
				'error': False,
				'tag_name': response.json()['tag_name'][1:],
				'title': response.json()['name']
				}
			else:
				logger.log('[UPDATER] Sneky is up to date.')
				return {
				'newupdate': False,
				'error': False
				}
		else:
			for version in versions:
				response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/' + version)
				try:
					if response.json()['message'] == 'API rate limit exceeded for ' + requests.get('https://api.ipify.org').content.decode('utf8') + '. (But here\'s the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)':
						logger.log('[UPDATER] GitHub API rate limit exceeded!\nSkipping update process.')
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else:
						logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
						return {
						'newupdate': False,
						'error': False,
						'unofficial': True
						}
				except:
					pass
				if currvertime < response.json()['published_at']:
					logger.log('[UPDATER] Updates available. User has been asked to update.', allowprint = False)
					return {
					'newupdate': True,
					'error': False,
					'tag_name': response.json()['tag_name'][1:],
					'title': response.json()['name']
					}
				else:
					logger.log('[UPDATER] Sneky is up to date.')
					return {
					'newupdate': False,
					'error': False
					}
	except:
		logger.log('[UPDATER] An error occurred while checking for updates!\n' + traceback.format_exc() + '\nSkipping update process.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': False
		}