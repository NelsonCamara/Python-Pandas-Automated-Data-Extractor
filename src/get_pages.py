import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
import os.path
import requests
import time
from PIL import Image
from io import BytesIO
import undetected_chromedriver as uc
from random import randint
from bs4 import BeautifulSoup
import urllib.request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}  

url = "https://www.leboncoin.fr/recherche?category=20&item_condition=1%2C6%2C2%2C3&home_appliance_product=appareildemassage%2Cbrosseadentelectrique%2Cbrossecoiffante%2Cepilateur%2Cferaboucler%2Clisseur%2Cpesepersonne%2Crasoirelectrique%2Csechecheveux%2Ctondeuse%2Cautres%2Cappareildecuisson%2Cbalancedecuisine%2Cbarbecueetplanchaelectrique%2Cbouilloire%2Ccaveavin%2Cextracteurdejus%2Cfouramicroondes%2Cgaziniere%2Cgrillepain%2Cmachineacafe%2Cmachineapain%2Cmachineasoda%2Cmachineathe%2Cpianodecuisson%2Cplaquedecuisson%2Crobotcuiseur%2Crobotmultifonction%2Crobotpatissier%2Cautresrobots%2Csorbetiere%2Ctireuseabiere%2Cyaourtiere%2Caspirateur%2Ccentralevapeur%2Ccentrederepassage%2Cchauffagedappoint%2Cclimatiseur%2Cdefroisseur%2Cferarepasser%2Cmachineacoudre%2Cnettoyeurvapeur%2Cventilateur&price=40-300"

def save_webpage_source_to_file(url,browser):
    # Initialisez le navigateur
    
    
    # Accédez à la page
    browser.get(url)
    time.sleep(20)  
    # Appuyez sur Ctrl + U pour voir le code source
    browser.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL, 'U')
   
    time.sleep(2)  # Attendre que le nouvel onglet soit ouvert
    
    # Passez au nouvel onglet contenant le code source
    browser.switch_to.window(browser.window_handles[1])
    
    # Sauvegardez le code source
    browser.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL, 'S')
    time.sleep(2)  # Laissez le dialogue de sauvegarde s'ouvrir

    browser.find_element(By.TAG_NAME,'body').send_keys(Keys.ENTER)

    time.sleep(2)  # Attendre que la sauvegarde soit terminée

    
    # NOTE: Cette partie est compliquée car le dialogue de sauvegarde dépend du système
    # Vous devrez peut-être utiliser une autre méthode pour automatiser le dialogue de sauvegarde
    # ou sauvegarder manuellement la première fois.

    # Fermez le navigateur une fois terminé
    browser.quit()

options = Options()
options.page_load_strategy = 'none'
#options.add_argument('--start-maximized')

options.add_argument("--window-size=1920,1080")
#options.add_argument("--headless")
#options.add_argument("--user-data-dir= C:\\Users\\Nelson\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
options.set_capability('acceptInsecureCerts',True)
browser = webdriver.Chrome(options=options) 

save_webpage_source_to_file(url,browser)

