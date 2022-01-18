from asyncio.windows_events import NULL
from distutils.log import error
from multiprocessing.sharedctypes import Value
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Key, Controller
import time, yaml

conf = yaml.load(open('locationDetails.yml')) # hide user location data
location = conf['user_location']['location']

upperBoundPrice = 300.00 # max price willing to pay
lowerBoundPrice = 150.00 # used to filter out junk postins 
keywords = ["bnib", "unopened", "sealed"]

try: 
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    print("had to install new chrome driver")

keyboard = Controller()


# open facebook
# driver.get("https://www.facebook.com/marketplace/?ref=bookmark")
# try:
#     print("testing")
#     searchFacebook = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div/span/div/div/div/div/label/input")
#     print("found search bar")
#     searchFacebook.send_keys("galaxy watch 4")
#     print("entered search content")
#     # driver.find_element_by_css_selector("#MainContainer > div.fes-pagelet > div > div > div > header > div.headerContainer-471773205.headerContainer__on-2833799052 > div > div.searchBarWrapper-3397949630 > form > button.searchSubmit-4090601312.searchSubmit__on-136443452").click()
#     press('enter')
#     print("pressed enter")
# except:
#     print('----error! unable to search !error----')

# open kijiji and enter search parameters
driver.get("https://www.kijiji.ca")
driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/div/header/div[3]/div/div[2]/form/div[1]/div/div/div/input").send_keys("Galaxy Watch 4 Classic")
driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/div/header/div[3]/div/div[2]/form/button[1]/span").click()
time.sleep(3)
driver.find_element_by_xpath("/html/body/div[11]/div/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div/input").send_keys(location)
time.sleep(3)
keyboard.press(Key.enter)
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[11]/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/button").click()

# put together list of viable posts
posts = driver.find_elements_by_class_name("search-item")
for item in posts:
    try:
        listedPrice = item.find_element_by_class_name("price").get_attribute("innerHTML").strip().lower()
        if("please contact" in listedPrice):
            pass
        # elif("$" in listedPrice): #img in some prices mess this up
        else:
            listedPriceVal = float(listedPrice.replace("$","").replace(",",""))
            if(lowerBoundPrice <= listedPriceVal <= upperBoundPrice):
                print("list price:   ", listedPriceVal)

                # add post to list of posts

    except ValueError as verr: # error occurs when there is a picture next to price
        print("error: ", verr)

# send email of list of posts

print("finished")