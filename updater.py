import logger
logger.log('[UPDATER] Initializing Sneky updater...', allowlog = False)
import traceback

global username, reponame, nomodule
username, reponame = 'gamingwithevets', 'sneky'

def check_internet():
	try:
		requests.get('https://google.com')
		return True
	except:
		logger.log('Cannot continue checking for Sneky updates because there is no Internet connection.')
		return False

def check_updates(currver, prerelease = False, showupdate = False):
	if nomodule:
		logger.log('[UPDATER] Cannot check for Sneky updates because the \'requests\'\nmodule was not installed.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': True
		}
	if not check_internet():
		logger.log('Cannot check for Sneky updates because there is no Internet connection.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': False,
		'nowifi': True
		}
	try:
		logger.log('[UPDATER] Begin checking for Sneky updates.')
		versions = []
		try:
			i = 0
			while True:
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
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
		if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
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
			if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
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
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
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
		'nomodule': False,
		'nowifi': False
		}

try:
	import requests
	nomodule = False
	logger.log('[UPDATER] Now ready to check for updates!', allowlog = False)
except:
	nomodule = True
	logger.log('[UPDATER] The \'requests\' module is not installed.\nAny attempt to check for updates will fail.', allowlog = False)