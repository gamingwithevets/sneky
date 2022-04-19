import logger
logger.log('[UPDATER] Initializing Sneky updater...', allowlog = False)
import traceback
from datetime import datetime

global username, reponame, nomodule
username, reponame = 'gamingwithevets', 'sneky'

def check_internet(log = True):
	url = 'https://google.com'
	logger.log('[UPDATER] Attempting Internet connection test.')
	try:
		logger.log('[UPDATER] Connecting to URL: {0}'.format(url))
		requests.get(url)
		logger.log('[UPDATER] Successfully connected to URL: ' + url + '\nConnection test succeeded!')
		return True
	except:
		if log: logger.log('[UPDATER] Cannot connect to URL: ' + url + '\nEither the Internet connection is slow, or there is no Internet connection.\nAborting update process.')
		return False

def check_updates(currver, prerelease):
	if prerelease: prerelease_str = 'on'
	else: prerelease_str = 'off'
	logger.log('[UPDATER] Received call to check updates.\nSetting "Check Prerelease Versions" is {0}.'.format(prerelease_str))
	if nomodule:
		logger.log('[UPDATER] Cannot check for Sneky updates because the \'requests\'\nmodule was not installed.\nAborting update process.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': True
		}
	if not check_internet(False):
		logger.log('[UPDATER] Cannot check for Sneky updates because there is no Internet connection.\nAborting update process.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': False,
		'nowifi': True
		}
	try:
		logger.log('[UPDATER] Begin checking for Sneky updates.')
		totalrequests = 0
		versions = []
		if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		logger.log('[UPDATER] Getting releases from repository: {0}/{1}'.format(username, reponame))
		try:
			response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases')
			totalrequests += 1
			logger.log('[UPDATER] Successfully connected.')
		except:
			logger.log('[UPDATER] Can\'t connect! Performing emergency Internet connection test.')
			if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}

		i = 0
		logger.log('[UPDATER] Getting release tags from repository: {0}/{1}'.format(username, reponame))
		try:
			while True:
				versions.append(response.json()[i]['tag_name'])
				i += 1
		except:
			logger.log('[UPDATER] Finished getting release tags.')
			pass

		if 'v' + currver not in versions:
			logger.log('[UPDATER] Tag v{0} not in tag list! Checking more data.'.format(currver))
			try:
				testvar = response.json()['message']
				if 'API rate limit exceeded for' in testvar:
					logger.log('[UPDATER] GitHub API rate limit exceeded!\nAborting update process.')
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
				try:
					response = requests.get('https://api.github.com/rate_limit')
					logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
				except:
					logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
				return {
				'newupdate': False,
				'error': False,
				'unofficial': True
				}
		if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		logger.log('[UPDATER] Getting data for release v{0} from repository: {1}/{2}'.format(currver, username, reponame))
		try:
			response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/v' + currver)
			totalrequests += 1
			logger.log('[UPDATER] Successfully connected.')
		except:
			logger.log('[UPDATER] Can\'t connect! Performing emergency Internet connection test.')
			if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		try:
			testvar = response.json()['message']
			if 'API rate limit exceeded for' in testvar:
				logger.log('[UPDATER] GitHub API rate limit exceeded!\nAborting update process.')
				try:
					response = requests.get('https://api.github.com/rate_limit')
					logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
				except:
					logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
				return {
				'newupdate': False,
				'error': True,
				'exceeded': True
				}
			else:
				logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
				try:
					response = requests.get('https://api.github.com/rate_limit')
					logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
				except:
					logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
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
			logger.log('[UPDATER] Getting latest release from repository: {0}/{1}'.format(username, reponame))
			try:
				response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/latest')
				totalrequests += 1
				logger.log('[UPDATER] Successfully connected.')
			except:
				logger.log('[UPDATER] Can\'t connect! Performing emergency Internet connection test.')
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
			try:
				testvar = response.json()['message']
				if 'API rate limit exceeded for' in testvar:
					logger.log('[UPDATER] GitHub API rate limit exceeded!\nAborting update process.')
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				pass
			if response.json()['tag_name'] != 'v' + currver and response.json()['published_at'] > currvertime:
				logger.log('[UPDATER] Updates available. User has been asked to update.')
				tag_name, title = response.json()['tag_name'][1:], response.json()['name']
				try:
					response = requests.get('https://api.github.com/rate_limit')
					logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
				except:
					logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
				return {
				'newupdate': True,
				'error': False,
				'tag_name': tag_name,
				'title': title
				}
			else:
				logger.log('[UPDATER] Sneky is up to date.')
				try:
					response = requests.get('https://api.github.com/rate_limit')
					logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
				except:
					logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
				return {
				'newupdate': False,
				'unofficial': False,
				'error': False
				}
		else:
			for version in versions:
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
				logger.log('[UPDATER] Getting data for release {0} from repository: {1}/{2}'.format(version, username, reponame))
				try:
					response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/' + version)
					totalrequests += 1
					logger.log('[UPDATER] Successfully connected.')
				except:
					logger.log('[UPDATER] Can\'t connect! Performing emergency Internet connection test.')
					if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
				try:
					testvar = response.json()['message']
					if 'API rate limit exceeded for' in testvar:
						logger.log('[UPDATER] GitHub API rate limit exceeded!\nAborting update process.')
						try:
							response = requests.get('https://api.github.com/rate_limit')
							logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
						except:
							logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else:
						logger.log('[UPDATER] Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
						try:
							response = requests.get('https://api.github.com/rate_limit')
							logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
						except:
							logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
						return {
						'newupdate': False,
						'error': False,
						'unofficial': True
						}
				except:
					pass
				if currvertime < response.json()['published_at']:
					logger.log('[UPDATER] Updates available. User has been asked to update.', allowprint = False)
					tag_name, title = response.json()['tag_name'][1:], response.json()['name']
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': True,
					'error': False,
					'tag_name': tag_name,
					'title': title
					}
				else:
					logger.log('[UPDATER] Sneky is up to date.')
					try:
						response = requests.get('https://api.github.com/rate_limit')
						logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
					except:
						logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
					return {
					'newupdate': False,
					'unofficial': False,
					'error': False
					}
	except:
		logger.log('[UPDATER] An error occurred while checking for updates!\n' + traceback.format_exc() + '\nAborting update process.')
		try:
			response = requests.get('https://api.github.com/rate_limit')
			logger.log('[UPDATER] Made {0} request(s), {1}/{2} request(s) left\nRate limit reset: {3}'.format(totalrequests, response.json()['rate']['remaining'], response.json()['rate']['limit'], datetime.fromtimestamp(response.json()['rate']['reset']).strftime("%d/%m/%Y %H:%M:%S")))
		except:
			logger.log('[UPDATER] Made {0} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??'.format(totalrequests))
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