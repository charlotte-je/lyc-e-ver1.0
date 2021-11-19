import calendar
from datetime import datetime
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pyautogui as pag

opt=Options()
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", { \
"profile.default_content_setting_values.media_stream_mic": 1,
"profile.default_content_setting_values.media_stream_camera": 1,
"profile.default_content_setting_values.geolocation": 1,
"profile.default_content_setting_values.notifications": 1
})

# WHEN THESE WORDS ARE TRIGGERED A MESSAGE WILL BE SENT
alertWords = [ "승아", "출석", "마이크", "말해봐", "들리나요","듣고있니","보고있나요","대답","결과"]

# TIME TABLE HERE
subjects = {'monday' : ['과탐실', '미술', '기가', '통사', '수학'],
                'tuesday':['진로','영어','한국사','통과','국어','영어','수학'],
                'wednesday' : ['영어', '통과', '체육','국어', '창체'],
                'thursday' : ['미술','국어','수학','한국사','통과','한국사','기가'],
                'friday' : ['국어', '기가', '통사',  '수학', '체육','영어','통사'],
              }

# GOOGLE MEET LINKS TO RESPECTIVE SUBJECTS
classes = { '과탐실':	'https://meet.google.com/ebb-wehv-uda?authuser=1',
                '미술':'https://meet.google.com/lookup/h4ee3r4rze?authuser=1&hs=179',
                '기가':'https://meet.google.com/zvq-aeuk-mve?authuser=1',
                '통사':'https://meet.google.com/scn-pgmo-rnv?authuser=1',
                '수학':'https://meet.google.com/lookup/frd5beeqbr?authuser=1&hs=179',
                '영어':'https://meet.google.com/wwf-wekg-nfq?authuser=1',
                '진로':'https://meet.google.com/lookup/hhq2x2awnb?authuser=1&hs=179',
                '체육':'https://meet.google.com/lookup/a2hmmahfsg?authuser=1&hs=179',
                '통과':'https://meet.google.com/lookup/cz4m3fmmmt?authuser=1&hs=179',
                '한국사':'https://meet.google.com/qfs-utai-szs?authuser=1',
                '국어' :'https://meet.google.com/sbk-aedi-pjn?authuser=1',
                  
          }

# RETURNS CURRENT DAY
def find_day():
    date_and_time = datetime.now()
    date = str(date_and_time.day) + ' ' + str(date_and_time.month) + ' ' + str(date_and_time.year)
    date = datetime.strptime(date, '%d %m %Y').weekday()
    day = calendar.day_name[date]
    return day.lower()

# RETURNS CURRENT DATE CLASSES
def find_classes():
    subs = []
    day = find_day()
    classes = subjects[day]
    # CHANGE ACCORDING TO YOUR TIME TABLE, I DONT HAVE CLASSES ON Tues, Thurs, Sat. SO MY CODE 
    if day != 'saturday' and day != 'sunday'  :
        # CHANGE ACCORDING TO YOUR CLASS TIMINGS
        timings = ['8:40 am - 9:30 am','9:40 am - 10:30 am', '10:40 am - 11:30 am', '11:40 am - 12:30 pm', '1:30 pm - 2:20 pm','2:30-pm - 3:20pm', '3:30pm - 4:20pm']
        for i in range(len(timings)):
            formatted = '{} {}'.format(timings[i],classes[i])
            subs.append(formatted)
    return subs

def classes_today():
    subs = find_classes()
    for i in subs:
        time = datetime.now().time()
        time = str(time).split(":")
        if time[0] == i[0:2] and time[1] >= i[3:5]:
            print('\n' + '\t' + i,' <-- Present Session')
        elif time[0] == i[11:13] and time[1] < i[14:16]:
            print('\n' + '\t' + i,' <-- Present Session')
        else:
            print('\n' + '\t' + i)


def open_link(url):
    try:
        driver=webdriver.Chrome(options=opt, executable_path='C:\Program Files (x86)\chromedriver.exe')
        driver.get('https://accounts.google.com/ServiceLogin/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F&followup=https%3A%2F%2Fclassroom.google.com%2F&emr=1&flowName=GlifWebSignIn&flowEntry=AddSession')

        #Logs in the classroom
        username=driver.find_element_by_id('identifierId')
        username.click()
        username.send_keys('gmail ici')

        next=driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]')
        next.click()
        time.sleep(2)
        password=driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password.click()
        password.send_keys('password ici')
        next=driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]')
        next.click()
        time.sleep(15)
        driver.get(url)
        time.sleep(7)

        # turns off camera
        camera=driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div')
        camera.click()

        # turns off mic
        mic=driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        mic.click()
        
        # clicks join button
        join=driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]')
        join.click() 
        time.sleep(3)

        # closes the popup
        driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[2]/div[3]/div').click()
        time.sleep(3)

        # turn on captions
        driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[9]/div[3]/div[2]/div/span/span/div').click()
        time.sleep(5)
        
        # Reads the text from captions
        while True:
            try:
                elems = driver.find_element_by_class_name("VbkSUe")
                captioTextLower = str(elems.text).lower()
                for word in alertWords:
                    if word in captioTextLower:
                        driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[3]').click()
                        time.sleep(2)
                        # Type whatever message you want to send when triggered
                        pag.write("네 선생님 저 마이크가 안돼서요ㅠㅠ ", interval=0.1)
                        time.sleep(0.5)
                        pag.press('enter')
                        time.sleep(2)
                time.sleep(0.5)
            except (NoSuchElementException, StaleElementReferenceException):
                time.sleep(1)
    except:
        time.sleep(3)
