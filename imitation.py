from json_api import getLot, getBets
from pydantic import BaseModel 
from typing import Optional, List, Any, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from classes import Bet, Lot
import json
from algorithm import simpleAlg

options = webdriver.ChromeOptions()
options.add_argument('headless')
#options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_experimental_option("excludeSwitches", ['enable-automation'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=options)

class DefaulfImmitation(BaseModel):
    alg: Any
    bets: List[Bet] = []
    kredits: float = 100.0
    statistic: Dict = {'maxKredits': 0, 'wins': 0, 'losses': 0, 'underNull': 0, 'skipped': 0}

    def addBet(self, lot: Lot):
        print('--\nKredits')
        ratio, user_gave = self.algReturn()
        site_gave = 0
        if user_gave:
            if ratio > lot.ratio:
                self.kredits -= user_gave
                self.checkNull()
            else:
                site_gave += user_gave * ratio 
                self.kredits += user_gave * (ratio - 1)
        else: print('SKIPPED')

        bet = Bet(site_gave = site_gave, user_gave = user_gave)
        print(self.kredits, '\n', bet.__dict__)

        self.bets.append(bet)
        self.collectStatic()
        
    def algReturn(self):
        algBet = self.alg(self.kredits, self.bets)
        user_gave = algBet.get('user_gave')
        ratio = algBet.get('ratio')

        return ratio, user_gave

    def checkNull(self):
        if self.kredits <= 0:
            self.statistic['underNull'] += 1
            self.kredits = 100
    
    def collectStatic(self):
        if not self.bets: return
        if self.bets[-1].user_gave:
            self.statistic['maxKredits'] = max(self.statistic['maxKredits'], self.kredits)
            if self.bets[-1].is_won: self.statistic['wins'] += 1
            else: self.statistic['losses'] += 1
        else:
            self.statistic['skipped'] += 1

    def stop(self):
        del self.bets
        print(self.__dict__)
        del self

def startImmitation(model, range:List):

    for id in range:
        url = f'https://csfail.org/api/crash/games/{id}'
        driver.get(url)

        jsonStr = driver.find_element(By.TAG_NAME, 'pre').text
        jsonDict = json.loads(jsonStr)

        if not jsonDict.get('success'):
            print(f'No game with id {id}')
            break
        data = jsonDict.get('data')

        lot = getLot(data)
        
        model.addBet(lot)

    model.stop()

model = DefaulfImmitation(alg = simpleAlg)

startImmitation(model, range(3320100, 3320201))