from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import time
import random
from pyotp import *
import threading
from threading import Thread, current_thread, local
from queue import Queue
from selenium import webdriver
import os


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return




chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

caps = chrome_options.to_capabilities()
caps['acceptInsecureCerts'] = True
s = Service(r"chromedriver.exe")

# user-agent
user_agents_list = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0']


# БРАУЗЕР ЗАКРЫТ И РАБОТЕТ
# headless mode
# chrome_options.add_argument("--headless")
# options.headless = True

thread_local = threading.local()

def create_driver():
    chrome_options.add_argument(f"user-agent={random.choice(user_agents_list)}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=s, options=chrome_options,
                              desired_capabilities=caps)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                              const newProto = navigator.__proto__
                              delete newProto.webdriver
                              navigator.__proto__ = newProto
                              """
    })
    thread_local.driver = driver
    return driver

def get_data(Login, Password, FA, Product, Count, results):
    # Данные
    totp = TOTP(f"{FA}")  # 2fa token
    email = f"{Login}"  # почта
    password = f"{Password}"  # пароль
    Product = Product
    ######
    try:

        # использование ThreadLocal для создания webdriver
        if not hasattr(thread_local, "driver"):
            create_driver()
        driver = thread_local.driver
        # ваш код для получения данных

        driver.get(url='https://gold.razer.com/globalzh/en/gold/catalog/pubg-mobile-uc-code')

        def login():
            wait = WebDriverWait(driver, 35)
            try:
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//preceding::button[@id='onetrust-accept-btn-handler']")))
                time.sleep(1)
                driver.find_element(By.XPATH, "//preceding::button[@id='onetrust-accept-btn-handler']").click()
            except:
                print('login 1st part')
            try:
                driver.get('https://razerid.razer.com/?client_id=63c74d17e027dc11f642146bfeeaee09c3ce23d8&redirect=https%3A%2F%2Fgold.razer.com%2Fglobalzh%2Fen%2Fgold%2Fcatalog%2Fpubg-mobile-uc-code')
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//preceding::button[@class='btn-agree']")))
                time.sleep(3)
                driver.find_element(By.XPATH, "//preceding::button[@class='btn-agree']").click()
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//preceding::input[@name='email']")))
                time.sleep(3)
                driver.find_element(By.XPATH, "//preceding::input[@name='email']").send_keys(email)
                driver.find_element(By.XPATH, "//preceding::input[@name='password']").send_keys(password)
                try:
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//preceding::button[@type='submit']")))
                    driver.find_element(By.XPATH, "//preceding::button[@type='submit']").click()
                    try:
                        wait = WebDriverWait(driver, 20)
                        element = wait.until(
                            EC.presence_of_element_located((By.XPATH, "//preceding::button[@id='btn-skip']")))
                        driver.find_element(By.XPATH, "//preceding::button[@id='btn-skip']").click()
                    except:
                        pass
                    return True
                except:
                    return '<b>Введен неправильный логин или пароль!</b>'
            except:
                return '<b>Произошла ошибка напишите-@foureason!</b>'


        def buy():
            # что покупаем
            wait = WebDriverWait(driver, 35)
            try:
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//preceding::div[@class='selection-tile__text d-flex flex-column justify-content-center text-center']")))
            except:
                print('\n ------------------------------- \n В наличии нет ни одного товара')

            try:
                nenal = driver.find_elements(By.XPATH, "//preceding::div[@class='selection-tile__text d-flex flex-column justify-content-center text-center disabled']")
                print('Не в наличии: \n ')
                masnet = []
                for i in range(len(nenal)):
                    print(nenal[i].text)
                    masnet.append(nenal[i])

            except:
                print('Все товары в наличии! \n ')

            try:
                nal = driver.find_elements(By.XPATH, "//preceding::div[@class='selection-tile__text d-flex flex-column justify-content-center text-center']")
                print('\n ------------------------------- \n В наличии: \n ')
                masyes = []
                for i in range(len(nal)):
                    print(nal[i].text)
                    masyes.append(nal[i].text)
                tovar = -1
                for i in range(len(masyes)):
                    if str(Product) in masyes[i]:
                        tovar = i
                        break
                if tovar == -1:
                    return "<b>Данного товара нет в наличии, или вам необходимо сменить регион с USA!</b>"
                else:
                    time.sleep(1)
                    driver.execute_script("window.scrollTo(0, 200)")
                    nal[tovar].click()
                # способ оплаты
                time.sleep(4)
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//preceding::div[@class='selection-tile__content rounded has-shadow selection-tile--image selectable selectable--outline hover-outline--brand']")))
                driver.find_element(By.XPATH, "//preceding::div[@class='selection-tile__content rounded has-shadow selection-tile--image selectable selectable--outline hover-outline--brand']").click()
                time.sleep(4)
                try:
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//preceding::button[@class='btn-loader btn-block-mobile btn btn-primary']")))
                    driver.find_element(By.XPATH, "//preceding::button[@class='btn-loader btn-block-mobile btn btn-primary']").click()
                except:
                    driver.refresh()
                    nal[tovar].click()
                    # способ оплаты
                    time.sleep(4)
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//preceding::div[@class='selection-tile__content rounded has-shadow selection-tile--image selectable selectable--outline hover-outline--brand']")))
                    driver.find_element(By.XPATH, "//preceding::div[@class='selection-tile__content rounded has-shadow selection-tile--image selectable selectable--outline hover-outline--brand']").click()
                    time.sleep(4)
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//preceding::button[@class='btn-loader btn-block-mobile btn btn-primary']")))
                    driver.find_element(By.XPATH, "//preceding::button[@class='btn-loader btn-block-mobile btn btn-primary']").click()
                try:
                    time.sleep(5)
                    WebDriverWait(driver, 240).until(
                        EC.presence_of_element_located((By.XPATH, "//preceding::button[@id='btn99']")))
                    time.sleep(10)
                    driver.find_element(By.XPATH, "//preceding::button[@id='btn99']").click()
                except:
                    return "<b>Недостаточно средств на аккаунте!</b>"
                WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id='razerOTP']")))
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='number']"))).send_keys(totp.now())
                time.sleep(1)
                if int(driver.execute_script("return document.getElementsByClassName('dialog').length"))==1:
                    return "<b>Неверный 2FA!</b>"
                return True

            except:
                return "<b>Произошла ошибка напишите-@foureason!</b>"

        def pars():
            global file_name
            wait = WebDriverWait(driver, 300)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//preceding::div[@class='pin-code']")))
            cods = driver.find_element(By.XPATH, "//preceding::div[@class='pin-code']")
            print(cods.text)

            with open("BuyUC.txt", "a") as tw:
                tw.write(f"{cods.text}""\n")
                tw.close()
            return True



            # element = wait.until(
            #     EC.presence_of_element_located((By.XPATH, "//preceding::ol[@class='pl-4']")))
            # cods = driver.find_element(By.XPATH, "//preceding::ol[@class='pl-4']")
            # print(cods.text)

        LOG=login()
        if LOG==True:
            BU=buy()
            if BU == True:
                parsing = pars()
                if parsing == True:
                    return parsing
            else:
                print(f"{BU} ебать ошибка")
                return BU
        else:
            return LOG



    except Exception as ex:
        print(f"Ошибка: !!!!!")
        if hasattr(thread_local, "driver"):
            thread_local.driver.close()
        return  # или что-то еще, если нужно отличать ошибочные


    finally:
        print(f"Finally блок")
        if hasattr(thread_local, "driver"):
            thread_local.driver.close()





    pass

    results.put(Queue)


def Start_Logic(Login, Password, FA, Count, Product):
    results = Queue()
    threads = []
    if Count > 4: Count = 4
    for i in range(Count):
        thread = CustomThread(target=get_data, args=(Login, Password, FA, Product, Count, results))
        thread.start()
        threads.append(thread)
    for thread in threads:
        final = thread.join()
        if hasattr(thread_local, "driver"):
            thread_local.driver.quit()
        if final == True:
            with open(f"BuyUC.txt") as f:
                text = f.read()
                lines = text.count('\n')
                f.close()
            print(f"Удача{final}")
            return [final, lines]
        else:
            print(f"Не удача{final}")
            return final