import json, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from classes import Bet, Lot

options = webdriver.ChromeOptions()
options.add_argument('headless')
#options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_experimental_option("excludeSwitches", ['enable-automation'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=options)




def getBets(betsDictsList):

    bets = []

    for betDict in betsDictsList:

        user_gave = float(betDict.get('itemsTotal'))
        site_gave = betDict.get('winItemPrice')
        site_gave = float(site_gave) if site_gave else 0
        ratio = float()
        
        bet = Bet(user_gave = user_gave, site_gave = site_gave)
        bets.append(bet)
        
    return bets


def getLot(data):
    game = data.get('game')

    bets = getBets(data.get('bets'))
    lotId = game.get('id')
    ratio = float(game.get('crashedAt'))

    lot = Lot(id = lotId, bets = bets, ratio = ratio)

    return lot


def starter(start_id, stop_id = 0):
    if stop_id:
        for id in range(start_id, stop_id+1):
            url = f'https://csfail.org/api/crash/games/{id}'
            driver.get(url)

            jsonStr = driver.find_element(By.TAG_NAME, 'pre').text
            jsonDict = json.loads(jsonStr)

            if not jsonDict.get('success'):
                print(f'No game with id {id}')
                break
            data = jsonDict.get('data')

            lot = getLot(data)
            print(lot.id)
    else:
        id = start_id
        while True:
            url = f'https://csfail.org/api/crash/games/{id}'
            driver.get(url)

            jsonStr = driver.find_element(By.TAG_NAME, 'pre').text
            jsonDict = json.loads(jsonStr)

            if not jsonDict.get('success'):
                print('Waiting for a new Lot...')
                time.sleep(10)
                continue

            data = jsonDict.get('data')

            lot = getLot(data)
            print(lot.ratio)

            id += 1

#starter(3320000)