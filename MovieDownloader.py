import time, os, random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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

def base():
    print(f"""\
        {color}
  __  __            _      ____                      _                 _           
 |  \/  | _____   _(_) ___|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 | |\/| |/ _ \ \ / / |/ _ \ | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |  | | (_) \ V /| |  __/ |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |_|  |_|\___/ \_/ |_|\___|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                                                   
{CEnd}""")
options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--log-level=3") 
options.add_argument("--headless") 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service("C:\chromedriver\chromedriver.exe")

browser = webdriver.Chrome(options=options, service=service)

print("Starting...\nDo not exit, it's normal.")
browser.get('https://www.wawacity.blue/')
delay = 3 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'main-body')))
    print("Opened website...")
except TimeoutException:
    print("Loading took too much time!")

select = Select(browser.find_element(By.XPATH, "/html/body/nav/div/div[2]/form/select"))
inputPlace = browser.find_element(By.XPATH, "/html/body/nav/div/div[2]/form/input")
searchButton = browser.find_element(By.XPATH, "/html/body/nav/div/div[2]/form/button")
def movieSearch():
    titles= []
    movieName = input("Movie name : ")
    inputPlace.send_keys(movieName)
    searchButton.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")))
    except TimeoutException:
        print("Loading took too much time!")
    elements = browser.find_elements(By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")
    for element in elements:
        items = []
        values = element.text.split("\n")
        items.append(values)
        title = items[0][0]
        title = title.split("[", 1)[0]
        titles.append(title)
    print(f"We found {len(titles)} movies.\n")
    for i in range(len(titles)):
        print(f"{i+1} - {titles[i]}")
    selectedMovieId = int(input("\nSelect a movie : "))-1
    selectedMovie = elements[selectedMovieId].text.split("\n")[0].split(" [", 1)[0]
    movie = browser.find_element(By.XPATH, f"//*[contains(text(), ' {selectedMovie}')]")
    movie.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-post-list-ofLinks row readable-post-list']")))
    except TimeoutException:
        print("Loading took too much time!")
    qualitys = browser.find_elements(By.XPATH, "//*[@id='detail-page']/div[1]/ul/li")
    selectedQualitys = []
    for qualitie in qualitys:
        items = []
        values = qualitie.text.split("\n")
        items.append(values)
        selectedQuality = items[0][0]
        selectedQualitys.append(selectedQuality)
    actualQuality = browser.find_element(By.XPATH, "//*[@id='detail-page']/div[2]/div[1]/i[2]").text
    actualQuality = actualQuality[1:].replace("]", "")
    selectedQualitys.append(actualQuality)
    print(f"We found {len(selectedQualitys)} qualities.\n")
    for i in range(len(selectedQualitys)):
        print(f"{i+1} - {selectedQualitys[i]}")
    selectedQualitysId = int(input("\nSelect a quality : "))-1
    if selectedQualitysId != len(selectedQualitys)-1:
        quality = browser.find_element(By.XPATH, f"//*[contains(text(), '{selectedQualitys[selectedQualitysId].split('(')[0]}')]")
        quality.click()
    tbody = browser.find_elements(By.XPATH, "//*[@id='DDLLinks']/tbody/tr/td[2]")
    allLinks = []
    for tr in tbody:
        texte = tr.text
        allLinks.append(texte)
    allLinks = allLinks[1:]
    print(f"\nWe found {len(allLinks)} hosts.\n")
    for i in range(len(allLinks)):
        print(f"{i+1} - {allLinks[i]}")
    selectedHostsId = int(input("\nSelect a host : "))-1
    selectedHost = browser.find_element(By.XPATH, f"//*[contains(text(), '{allLinks[selectedHostsId]}')]")
    parent = selectedHost.find_element(By.XPATH, "..")
    parent.click()
    # print the actual url
    # change the tab
    i=1
    browser.switch_to.window(browser.window_handles[i])
    if "dl-protect.info" in browser.current_url:
        i=i
    else:
        i+=+1
        browser.switch_to.window(browser.window_handles[i])
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]")))
    except TimeoutException:
        print("Loading took too much time!")
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/button")
    button.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")))
    except TimeoutException:
        print("Loading took too much time!")
    browser.get_screenshot_as_file("screenshot.png")
    link = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")
    url = link.text
    print(f"\nThe link is {url}")

""" todo : automaticaly gave all the links
def tvShowSearch():
    titles= []
    TVShowName = input("TV Show name : ")
    inputPlace.send_keys(TVShowName)
    searchButton.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")))
    except TimeoutException:
        print("Loading took too much time!")
    elements = browser.find_elements(By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")
    for element in elements:
        items = []
        values = element.text.split("\n")
        items.append(values)
        title = items[0][0]
        title = title.split("[", 1)[0]
        titles.append(title)
    print(f"We found {len(titles)} TV show.\n")
    for i in range(len(titles)):
        print(f"{i+1} - {titles[i]}")
    selectedTVShowId = int(input("\nSelect a TV show : "))-1
    print(f"You selected {titles[selectedTVShowId]}")
    selectedTVShow = titles[selectedTVShowId].split("\n")[0].split(" [", 1)[0]
    selectedTVShow2 = selectedTVShow.split(" - ")[2]
    firstValue = selectedTVShow.split(" - ")[0] + " - " + selectedTVShow.split(" - ")[1]
    firstValueSearch = browser.find_elements(By.XPATH, f"//*[contains(text(), ' {firstValue}')]")
    # for all results check if the TV show is the one we want
    for element in firstValueSearch:
        try:
            if element.text == titles[selectedTVShowId]:
                element.click()
        except:
            pass
    print(browser.current_url)

    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-post-list-ofLinks row readable-post-list']")))
    except TimeoutException:
        print("Loading took too much time!")

    tbody = browser.find_elements(By.XPATH, "//*[@id='DDLLinks']/tbody/tr/td[2]")
    allLinks = []
    for tr in tbody:
        parenttd = tr.find_element(By.XPATH, "..")
        texte = tr.text
        classTr = parenttd.get_attribute("class")
        styleTr = parenttd.get_attribute("style")
        print(styleTr+"\n"+classTr)
        if classTr == "title episode-title active":
            allLinks.append(texte)
    allLinks = allLinks[1:]
    print(f"\nWe found {len(allLinks)} hosts.\n")
    for i in range(len(allLinks)):
        print(f"{i+1} - {allLinks[i]}")
    selectedHostsId = int(input("\nSelect a host : "))-1

    selectedHost = browser.find_element(By.XPATH, f"//*[contains(text(), '{allLinks[selectedHostsId]}')]")
    parent = selectedHost.find_element(By.XPATH, "..")
    parent.click()
    # print the actual url
    # change the tab
    i=1
    browser.switch_to.window(browser.window_handles[i])
    if "dl-protect.info" in browser.current_url:
        i=i
    else:
        i+=+1
        browser.switch_to.window(browser.window_handles[i])
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]")))
    except TimeoutException:
        print("Loading took too much time!")
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/button")
    button.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")))
    except TimeoutException:
        print("Loading took too much time!")
    link = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")
    url = link.text
    print(f"\nThe link is {url}")
"""

def gameSearch():
    titles= []
    movieName = input("Game name : ")
    inputPlace.send_keys(movieName)
    searchButton.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")))
    except TimeoutException:
        print("Loading took too much time!")
    elements = browser.find_elements(By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")
    for element in elements:
        items = []
        values = element.text.split("\n")
        items.append(values)
        title = items[0][0]
        title = title.split("[", 1)[0]
        titles.append(title)
    print(f"We found {len(titles)} games.\n")
    for i in range(len(titles)):
        print(f"{i+1} - {titles[i]}")
    selectedMovieId = int(input("\nSelect a game : "))-1
    selectedMovie = elements[selectedMovieId].text.split("\n")[0].split(" [", 1)[0]
    movie = browser.find_element(By.XPATH, f"//*[contains(text(), ' {selectedMovie}')]")
    movie.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-post-list-ofLinks row readable-post-list']")))
    except TimeoutException:
        print("Loading took too much time!")
    tbody = browser.find_elements(By.XPATH, "//*[@id='DDLLinks']/tbody/tr/td[2]")
    allLinks = []
    for tr in tbody:
        texte = tr.text
        allLinks.append(texte)
    allLinks = allLinks[1:]
    print(f"\nWe found {len(allLinks)} hosts.\n")
    for i in range(len(allLinks)):
        print(f"{i+1} - {allLinks[i]}")
    selectedHostsId = int(input("\nSelect a host : "))-1
    selectedHost = browser.find_element(By.XPATH, f"//*[contains(text(), '{allLinks[selectedHostsId]}')]")
    parent = selectedHost.find_element(By.XPATH, "..")
    parent.click()
    # print the actual url
    # change the tab
    i=1
    browser.switch_to.window(browser.window_handles[i])
    if "dl-protect.info" in browser.current_url:
        i=i
    else:
        i+=+1
        browser.switch_to.window(browser.window_handles[i])
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]")))
    except TimeoutException:
        print("Loading took too much time!")
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/button")
    button.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")))
    except TimeoutException:
        pass
    link = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")
    url = link.text
    print(f"\nThe link is {url}")

def musicSearch():
    titles= []
    movieName = input("Music name : ")
    inputPlace.send_keys(movieName)
    searchButton.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")))
    except TimeoutException:
        print("Loading took too much time!")
    elements = browser.find_elements(By.XPATH, "//*[@class='wa-sub-block wa-post-detail-item']")
    for element in elements:
        items = []
        values = element.text.split("\n")
        items.append(values)
        title = items[0][0]
        title = title.split("[", 1)[0]
        titles.append(title)
    print(f"We found {len(titles)} games.\n")
    for i in range(len(titles)):
        print(f"{i+1} - {titles[i]}")
    selectedMovieId = int(input("\nSelect a game : "))-1
    selectedMovie = elements[selectedMovieId].text.split("\n")[0].split(" [", 1)[0]
    movie = browser.find_element(By.XPATH, f"//*[contains(text(), ' {selectedMovie}')]")
    movie.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wa-post-list-ofLinks row readable-post-list']")))
    except TimeoutException:
        print("Loading took too much time!")
    tbody = browser.find_elements(By.XPATH, "//*[@id='DDLLinks']/tbody/tr/td[2]")
    allLinks = []
    for tr in tbody:
        texte = tr.text
        allLinks.append(texte)
    allLinks = allLinks[1:]
    print(f"\nWe found {len(allLinks)} hosts.\n")
    for i in range(len(allLinks)):
        print(f"{i+1} - {allLinks[i]}")
    selectedHostsId = int(input("\nSelect a host : "))-1
    selectedHost = browser.find_element(By.XPATH, f"//*[contains(text(), '{allLinks[selectedHostsId]}')]")
    parent = selectedHost.find_element(By.XPATH, "..")
    parent.click()
    # print the actual url
    # change the tab
    i=1
    browser.switch_to.window(browser.window_handles[i])
    if "dl-protect.info" in browser.current_url:
        i=i
    else:
        i+=+1
        browser.switch_to.window(browser.window_handles[i])
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]")))
    except TimeoutException:
        pass
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/button")
    button.click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")))
    except TimeoutException:
        pass
    link = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/ul/li/a")
    url = link.text
    print(f"\nThe link is {url}")


def baseQuestion():
    print(f"{CRed}What do you want to search ?{CEnd}")
    print("\n"+f"""\
        {CBlue}[1]{CEnd} {CBeige}Movie{CEnd}
        {CRed}[2]{CEnd} {CRed}TVShow{CEnd} (Dont work)
        {CBlue}[3]{CEnd} {CBeige}Game{CEnd}
        {CBlue}[4]{CEnd} {CBeige}Music{CEnd}
        {CBlue}[e]{CEnd} {CBeige}Exit{CEnd}
        """)
    reponse = input(cmdline)
    if reponse == "1":
        select.select_by_value('films')
        movieSearch()
    elif reponse == "2":
        select.select_by_value('series')
        tvShowSearch()
    elif reponse == "3":
        select.select_by_value('jeux')
        gameSearch()
    elif reponse == "4":
        select.select_by_value('musiques')
        musicSearch()
    elif reponse == "e":
        cls()
        exit()
    else:
        print("Invalid response, try again.")
        time.sleep(1)
        start()

def start():
    cls()
    base()
    baseQuestion()

start()