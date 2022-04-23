from requests import Session
from bs4 import BeautifulSoup
from web3.auto import w3
from loguru import logger
from sys import stderr
from pyuseragents import random as random_useragent
from multiprocessing.dummy import Pool
from urllib3 import disable_warnings
from platform import system as platform_system
from platform import platform
from os import system
from msvcrt import getch

class Wrong_Response(BaseException):
	def __init__(self, message):
		self.message = message

disable_warnings()
def clear(): return system('cls' if platform_system() == "Windows" else 'clear')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
print('Telegram channel - https://t.me/n4z4v0d\n')

if 'Windows' in platform():
	from ctypes import windll
	windll.kernel32.SetConsoleTitleW('Hyundai Auto Reger | by NAZAVOD')

threads = int(input('Threads: '))
data_folder = str(input('Drop .txt (format: discord:twitter): '))

with open(data_folder, 'r') as file:
	data_original = [row.strip() for row in file]

def create_wallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)

googleformurl = 'https://docs.google.com/forms/d/e/1FAIpQLSe98x8_opY5TWmld_G4CyM_8Msm2Pe4pdj7_eJpNn8ixbce-w/viewform'
formResponse = 'https://docs.google.com/forms/d/e/1FAIpQLSe98x8_opY5TWmld_G4CyM_8Msm2Pe4pdj7_eJpNn8ixbce-w/formResponse'


def mainth(data):
	for _ in range(100):
		try:
			discord_id = data.split(':')[0]
			twitter_username = data.split(':')[1]

			session = Session()
			session.headers.update({'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'cache-control': 'max-age=0', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://docs.google.com', 'referer': googleformurl, 'user-agent': random_useragent()})

			wallet_data = create_wallet()
			r = session.get(googleformurl)
			fbzx = BeautifulSoup(r.text, 'lxml').find('input', {'name':'fbzx'})['value']

			fulldata = f'entry.1213834476={discord_id}&entry.127126464={twitter_username}&entry.1996607665={wallet_data[0]}&entry.790332630=Wow!+It+feels+like+ice!&entry.790332630_sentinel=&fvv=1&partialResponse=[null,null,"{fbzx}"]&pageHistory=0&fbzx={fbzx}'.encode('utf-8')

			r = session.post(formResponse, data=fulldata)

			if not 'Ответ записан.' in r.text:
				raise Wrong_Response(r)

		except Wrong_Response as error:
			error_text = error.text.replace('\n', '')
			logger.error(f'{twitter_username} | Wrong Response, status code: {error.status_code}, response text: {error_text}')

		except Exception as error:
			logger.error(f'{twitter_username} | Unexpected error: {error}')

		else:
			with open('registered.txt', 'a') as file:
				file.write(f'{discord_id}:{twitter_username}:{wallet_data[0]}:{wallet_data[1]}\n')

			logger.success(f'{twitter_username} | The form has been completed successfully')

			return

	with open('unregisterd.txt', 'a') as file:
		file.write(f'{discord_id}:{twitter_username}\n')

if __name__ == '__main__':
	clear()
	pool = Pool(threads)
	pool.map(mainth, data_original)

	logger.success('Работа успешно завершена')
	print('\nPress Any Key To Exit..')
	getch()
	exit()