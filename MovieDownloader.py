from pydoc import cli
import time, os, random, itertools, threading
from grpc import ClientCallDetails
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service



CBlack = "\033[90m"
CRed = "\033[91m"
CGreen = "\033[92m"
CYellow = "\033[93m"
CYellow2 = "\033[33m"
CBlue = "\033[94m"
CPurple = "\033[95m"
CBeige = "\033[96m"
CWhite = "\033[97m"
CClear = "\033[30m"
CEnd = "\033[0m"

ColorList = [CRed, CGreen, CYellow, CYellow2, CBlue, CBeige]
color = random.choice(ColorList)

cmdline = f"{CBlue}MovieDownloader(~)$ {CEnd}"

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def loadingPrint(phrase,latence):
    for line in phrase:
        for letter in line:
            print(letter, end="",  flush=True)
            time.sleep(latence)

logo = f"""{color}
███    ███  ██████  ██    ██ ██ ███████ ██████   ██████  ██     ██ ███    ██ ██       ██████   █████  ██████  ███████ ██████  
████  ████ ██    ██ ██    ██ ██ ██      ██   ██ ██    ██ ██     ██ ████   ██ ██      ██    ██ ██   ██ ██   ██ ██      ██   ██ 
██ ████ ██ ██    ██ ██    ██ ██ █████   ██   ██ ██    ██ ██  █  ██ ██ ██  ██ ██      ██    ██ ███████ ██   ██ █████   ██████  
██  ██  ██ ██    ██  ██  ██  ██ ██      ██   ██ ██    ██ ██ ███ ██ ██  ██ ██ ██      ██    ██ ██   ██ ██   ██ ██      ██   ██ 
██      ██  ██████    ████   ██ ███████ ██████   ██████   ███ ███  ██   ████ ███████  ██████  ██   ██ ██████  ███████ ██   ██     
{CEnd}"""

def base():
    loadingPrint(logo,0.000001)
    print("\n")

options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--log-level=3") 
options.add_argument("--headless") 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service("C:\chromedriver\chromedriver.exe")

browser = webdriver.Chrome(options=options, service=service)
programType = ""
done = False

def animate():
    base()
    for c in itertools.cycle(['   ', '.  ', '.. ', '...']):
        if done:
            break
        print(f"\r{CGreen}Starting" + c, end=f"{CEnd}")
        time.sleep(0.5)

t = threading.Thread(target=animate)
t.start()

browser.get('http://www.papaflix.com/')
delay = 3 # seconds

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'main-body')))
except TimeoutException:
    print("Loading took too much time!")
done = True

def seeTheLink():
    try:
        continueToSeeTheLink = browser.find_element(By.XPATH, "/html/body/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div/input")
        continueToSeeTheLink.click()
    except:
        seeTheLink()

inputPlace = browser.find_element(By.XPATH, "/html/body/div[3]/header/ul[1]/li/form/div/input[4]")
def search():
    titles= []
    movieName = input("Program name : ")
    inputPlace.send_keys(movieName)
    inputPlace.submit()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[4]/div/div[2]/div[1]/p/a[2]")))
    except TimeoutException:
        print("Loading took too much time!")
    elementsPath = "//*[@id='dle-content']/div"
    elements = browser.find_elements(By.XPATH, elementsPath)
    for element in elements:
        items = []
        values = element.text.split("\n")
        items.append(values)
        
        try:
            titles.append(f"{values[1]} ({values[2]})")
        except:
            print(f"An error occured while trying to get the title of {values[1]}")
    
    print(f"We found {len(titles)} programs.\n")
    for i in range(len(titles)):
        print(f"{i+1} - {titles[i]}")
    selectedMovieId = int(input("\nSelect a program : "))
    selectedMovie = f"{elementsPath}[{selectedMovieId}]"
    movie = browser.find_element(By.XPATH, selectedMovie)
    movie.click()
    dropdown = browser.find_element(By.XPATH, "/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/div/button")
    dropdown.click()
    qualityPath="/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/ul"
    qualitys = browser.find_elements(By.XPATH, qualityPath)
    selectedQualitys=[]
    for quality in qualitys:
        items = []
        values = quality.text.split("\n")
        items.append(values)
        selectedQuality = items[0]
    
    print(f"We found {len(selectedQuality)} qualities.\n")
    for i in range(len(selectedQuality)):
        print(f"{i+1} - {selectedQuality[i]}")
    selectedQualitysId = int(input("\nSelect a quality : "))
    selectedQuality = f"{qualityPath}/li[{selectedQualitysId}]"
    quality = browser.find_element(By.XPATH, selectedQuality)
    quality.click()

    allHebergeurs = "//*[@id='show_links']/div/div"
    hebergeurs = browser.find_elements(By.XPATH, allHebergeurs)
    i=1
    hosters = []
    for hebergeur in hebergeurs:
        namePath = f"/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div/div/div[3]/div/div[{i}]/table/thead/tr/th[1]"
        name = browser.find_element(By.XPATH, namePath).text.capitalize()
        hosters.append(name)
        sizePath = f""
        i+=1

    print(f"We found {len(hosters)} hosts.\n")
    for i in range(len(hosters)):
        print(f"{i+1} - {hosters[i]}")
    selectedHosterId = int(input("\nSelect a host : "))

    linksPath = f"/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div/div/div[3]/div/div[{selectedHosterId}]/table/tbody/tr"
    links = browser.find_elements(By.XPATH, linksPath)
    i=1
    sizes = []
    for link in links:
        sizePath = f"/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div/div/div[3]/div/div[{selectedHosterId}]/table/tbody/tr[{i}]/td[3]"
        size = browser.find_element(By.XPATH, sizePath).text
        sizes.append(size)
        i+=1

    print(f"We found {len(sizes)} links.\n")
    for i in range(len(sizes)):
        print(f"{i+1} - {sizes[i]}")
    selectedLinkId = int(input("\nSelect a link : "))

    linkPath = f"/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div/div/div[3]/div/div[1]/table/tbody/tr[{selectedLinkId}]/td[1]/a[1]"
    link = browser.find_element(By.XPATH, linkPath)
    link.click()
    
    browser.switch_to.window(browser.window_handles[-1])

    clickToPass = browser.find_element(By.XPATH, "//*[@id='captcha']/div/div[2]/div[1]/div[3]")
    clickToPass.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div/input")))
    except TimeoutException:
        print("Loading took too much time!")
    seeTheLink()
    finalLink = browser.find_element(By.XPATH, "/html/body/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/h3/a")
    print(f"\nThere's your link: {finalLink.text}\nEnjoy!")
    response = input("\nPress a button to exit : ")

def baseQuestion():
    print(f"{CRed}What do you want to search ?{CEnd}")
    print("\n"+f"""\
        {CBlue}[1]{CEnd} {CBeige}Movie/Games/Music/...{CEnd}

        {CBlue}[e]{CEnd} {CBeige}Exit{CEnd}
        """)
    reponse = input(cmdline)
    if reponse == "1":
        search()
    elif reponse == "e":
        cls()
        exit()
    else:
        print("Invalid response, try again.")
        time.sleep(1)
        start()

def start():
    cls()
    baseQuestion()

start()