from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from random import randint
from time import sleep

#Login Info
my_username = "REPLACE"
my_password = "REPLACE"

#Initial Bet
bet = "0.01"

# Initiate the browser
driver  = webdriver.Chrome(ChromeDriverManager().install())
#Maximizes window
driver.maximize_window()
#Small elay to allow window to resize
time.sleep(1)
# Open the Website
driver.get('https://www.bananobet.com/')

# Allows Captcha to be completed manually
def login_process():
    #Clicks Login button in top right
    login_button = driver.find_element_by_xpath("//*[@id='navbarSupportedContent']/div/button").click();
    time.sleep(2)
    #Locates and sends username to username box
    id_box = driver.find_element_by_xpath("/html/body/div[3]/div/div/form/div[1]/div[1]/input")
    id_box.click();
    id_box.send_keys(my_username)
    #Locates and sends password to password box
    pw_box = driver.find_element_by_xpath("/html/body/div[3]/div/div/form/div[1]/div[2]/input")
    pw_box.send_keys(my_password)
    #Time to complete ReCAPTCHA, waits for My Bets page to become visible
    wait = WebDriverWait(driver, 300)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[5]/div/ul/li[2]/a")))
    #Find table on My bets page
    table = driver.find_element_by_id("myBetLog")
    #Define double bet button
    doubler_button = driver.find_element_by_id("doubleBetBtn")
    #Define Roll Dice button
    roll_dice = driver.find_element_by_id('betSubmit')
    #Bid Amount box
    bet_box = driver.find_element_by_id('bet_amount')

login_process()

#Open My Bets page
my_bets = driver.find_element_by_id("pills-my-bets-tab")
my_bets.click()
#Find table on page
table = driver.find_element_by_id("myBetLog")
#Define double bet button
doubler_button = driver.find_element_by_id("doubleBetBtn")
#Define Roll Dice button
roll_dice = driver.find_element_by_id('betSubmit')
#Bid Amount box
bet_box = driver.find_element_by_id('bet_amount')

#Define initial bet
def initial_bet():
    time.sleep(5)
    #Sends initial bet
    bet_box.send_keys(bet)
    #Clicks to submit bet
    roll_dice.click();
    #Pauses to allow table to update with result
    time.sleep(5)

#Define betting strategy
def win():
    #Clears bet amount
    bet_box.clear()
    #Sends initial bet
    bet_box.send_keys(bet)
    #Clicks to submit bet
    roll_dice.click();
    #Pauses to allow table to update with result
    time.sleep(randint(1,2))
    #Returns and bets initial amount again
    bet_loop()

def lose():
    result = table.find_element_by_xpath("//*[@id='myBetLog']/tr[1]/td[9]").text
    #Checks cell for maximum acceptable loss and restarts process if found
    if ("-1.28") in result:
        win()
    else:
        #Clicks doubler button to double bet in bet_box
        doubler_button.click();
        #Submits bet
        roll_dice.click();
        #Pauses to allow table to update after result
        time.sleep(randint(2,3))
        #Returns and bets initial amount again
        bet_loop()

def bet_loop():
    #Returns prtofit/loss value from table
    result = table.find_element_by_xpath("//*[@id='myBetLog']/tr[1]/td[9]").text
    #Checks cell value
    if ("+") in result:
        #Runs Win condition
        win()
    else:
        #Runs lose condtions
        lose()

initial_bet()

bet_loop()
