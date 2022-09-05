import sys
if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

import logger
tag = 'UPDATER'

logger.log('Initializing Sneky updater...', tag = tag)
import traceback
from datetime import datetime

global username, reponame, nomodule
username, reponame = 'gamingwithevets', 'sneky'


def check_internet(log = True):
	url = 'https://google.com'
	print_tag('Attempting Internet connection test.')
	try:
		print_tag(f'Connecting to URL: {url}')
		requests.get(url)
		print_tag(f'Successfully connected to URL: {url}')
		print_tag('Connection test succeeded!')
		return True
	except:
		if log:
			print_tag(f'Cannot connect to URL: {url}')
			print_tag('Either the Internet connection is slow, or there is no Internet connection. Aborting update process.')
		return False

def print_tag(text):
	logger.log(text, tag = tag)

def print_rate_limit(totalrequests):
	try:
		response = requests.get('https://api.github.com/rate_limit')
		remaining = response.json()['rate']['remaining']
		limit = response.json()['rate']['limit']
		reset = datetime.fromtimestamp(response.json()['rate']['reset']).strftime('%d/%m/%Y %H:%M:%S')
		print_tag(f'Made {totalrequests} request(s), {remaining}/{limit} request(s) left\nRate limit reset: {reset}')
	except: print_tag(f'Made {totalrequests} request(s), ????/???? request(s) left\nRate limit reset: ??/??/???? ??:??:??')

def check_updates(currver, prerelease):
	if prerelease: prerelease_str = 'on'
	else: prerelease_str = 'off'
	print_tag(f'Received call to check updates.\nSetting "Check Prerelease Versions" is {prerelease_str}.')
	if nomodule:
		print_tag('Cannot check for Sneky updates because the \'requests\'\nmodule was not installed. Aborting update process.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': True
		}
	if not check_internet(False):
		print_tag('Cannot check for Sneky updates because there is no Internet connection. Aborting update process.')
		return {
		'newupdate': False,
		'error': True,
		'exceeded': False,
		'nomodule': False,
		'nowifi': True
		}
	try:
		print_tag('Begin checking for Sneky updates.')
		totalrequests = 0
		versions = []
		if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		print_tag(f'Getting releases from repository: {username}/{reponame}')
		try:
			response = requests.get(f'https://api.github.com/repos/{username}/{reponame}/releases')
			totalrequests += 1
			print_tag('Successfully connected.')
		except:
			print_tag('Can\'t connect! Performing emergency Internet connection test.')
			if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}

		i = 0
		print_tag(f'Getting release tags from repository: {username}/{reponame}')
		try:
			while True:
				versions.append(response.json()[i]['tag_name'])
				i += 1
		except:
			print_tag('Finished getting release tags.')
			pass

		if 'v' + currver not in versions:
			print_tag(f'Tag v{currver} not in tag list! Checking more data.')
			try:
				testvar = response.json()['message']
				if 'API rate limit exceeded for' in testvar:
					print_tag('GitHub API rate limit exceeded! Aborting update process.')
					print_rate_limit(totalrequests)
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					print_tag(f'Unofficial/development version of Sneky (v{currver}) has been detected.')
					print_rate_limit(totalrequests)
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				print_tag(f'Unofficial/development version of Sneky (v{currver}) has been detected.')
				print_rate_limit(totalrequests)
				return {
				'newupdate': False,
				'error': False,
				'unofficial': True
				}
		if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		print_tag(f'Getting data for release v{currver} from repository: {username}/{reponame}')
		try:
			response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/v' + currver)
			totalrequests += 1
			print_tag('Successfully connected.')
		except:
			print_tag('Can\'t connect! Performing emergency Internet connection test.')
			if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
		try:
			testvar = response.json()['message']
			if 'API rate limit exceeded for' in testvar:
				print_tag('GitHub API rate limit exceeded! Aborting update process.')
				print_rate_limit(totalrequests)
				return {
				'newupdate': False,
				'error': True,
				'exceeded': True
				}
			else:
				print_tag('Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
				print_rate_limit(totalrequests)
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
			print_tag(f'Getting latest release from repository: {username}/{reponame}')
			try:
				response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/latest')
				totalrequests += 1
				print_tag('Successfully connected.')
			except:
				print_tag('Can\'t connect! Performing emergency Internet connection test.')
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
			try:
				testvar = response.json()['message']
				if 'API rate limit exceeded for' in testvar:
					print_tag('GitHub API rate limit exceeded! Aborting update process.')
					print_rate_limit(totalrequests)
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else:
					print_tag('Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
					print_rate_limit(totalrequests)
					return {
					'newupdate': False,
					'error': False,
					'unofficial': True
					}
			except:
				pass
			if response.json()['tag_name'] != 'v' + currver and response.json()['published_at'] > currvertime:
				print_tag('Updates available. Prompting to update.')
				tag_name, title = response.json()['tag_name'], response.json()['name']
				print_rate_limit(totalrequests)
				return {
				'newupdate': True,
				'error': False,
				'tag_name': tag_name,
				'title': title
				}
			else:
				print_tag('Sneky is up to date.')
				print_rate_limit(totalrequests)
				return {
				'newupdate': False,
				'unofficial': False,
				'error': False
				}
		else:
			for version in versions:
				if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
				print_tag(f'Getting data for release {version} from repository: {username}/{reponame}')
				try:
					response = requests.get('https://api.github.com/repos/' + username + '/' + reponame + '/releases/tags/' + version)
					totalrequests += 1
					print_tag('Successfully connected.')
				except:
					print_tag('Can\'t connect! Performing emergency Internet connection test.')
					if not check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nomodule': False, 'nowifi': True}
				try:
					testvar = response.json()['message']
					if 'API rate limit exceeded for' in testvar:
						print_tag('GitHub API rate limit exceeded! Aborting update process.')
						print_rate_limit(totalrequests)
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else:
						print_tag('Unofficial/development version of Sneky (v.' + currver + ') has been detected.')
						print_rate_limit(totalrequests)
						return {
						'newupdate': False,
						'error': False,
						'unofficial': True
						}
				except:
					pass
				if currvertime < response.json()['published_at']:
					print_tag('Updates available. Prompting to update.')
					tag_name, title = response.json()['tag_name'], response.json()['name']
					print_rate_limit(totalrequests)
					return {
					'newupdate': True,
					'error': False,
					'tag_name': tag_name,
					'title': title
					}
				else:
					print_tag('Sneky is up to date.')
					print_rate_limit(totalrequests)
					return {
					'newupdate': False,
					'unofficial': False,
					'error': False
					}
	except:
		print_tag('An error occurred while checking for updates!\n' + traceback.format_exc() + ' Aborting update process.')
		print_rate_limit(totalrequests)
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
	print_tag('Now ready to check for updates!')
except:
	nomodule = True
	print_tag('The \'requests\' module is not installed.\nAny attempt to check for updates will fail.')