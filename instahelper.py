#selenium
from selenium import webdriver
#keyboard manipulation
from selenium.webdriver.common.keys import Keys
#folder manipulation
import os
#keep track of time
import time
#sound notifications (beeps)
import winsound

#to read and edit excel files
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


#class to hold bot functions
class Instahelp:

    def __init__(self, username, password):
        #set class attributes
        self.username = username
        self.password = password

        #open webdriver chrome browser
        self.driver = webdriver.Chrome('./chromedriver.exe')


    #define logging in
    def login(self):
        #get instagram login page
        self.driver.get('https://www.instagram.com/accounts/login/')
        #wait to load
        time.sleep(2)
        #find username box and password box by name attribute (from inspect element)
        #then send keys from self.username, self.password
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        #find and click login button as first element with text "Log In" in div (insepct element)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        #time to load
        time.sleep(2)
        print('logged in')
        self.driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()

    def closedriver(self):
        self.driver.close()
        print('closed out')

    def likeuserpic(self, user, npics):
        #max 24 unless u wanna code another scroll lol
        #go to user's page
        self.driver.get('https://www.instagram.com/' + user)
        time.sleep(2)
        #find user's pics
        pics = self.driver.find_elements_by_class_name('_9AhH0')
        print(len(pics))
        #try to like pic
        for pic in pics[0:npics]: #first n pics
            try:
                pic.click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format('Like')).click()
                print('liked')
                time.sleep(0.5)
            except Exception as e:
                print(e)
                time.sleep(1)
            #exit pic
            self.driver.find_elements_by_class_name('ckWGn')[0].click()            
            
    def readuserlist(self):
        #get list of users from usersheet excel
        usersheet = pd.read_excel('usersheet.xlsx', sheet_name='Sheet1')
        self.userlist = usersheet['user list']
        
    def writeuserlist(self, userlist):
        #extend for column name of user list
        userlist = ['user list'] + userlist
        #write list into usersheet excel
        df = pd.DataFrame(userlist)
#        writer = pd.ExcelWriter('usersheet.xlsx', engine='xlsxwriter')
        df.to_excel('usersheet.xlsx', sheet_name="Sheet1", startcol = -1, startrow = -1)

    #liking function
    def likepic(self,npics):
        #remember cap 300 per hour
        #~100 covers a day?
        #start timer
        start = time.time()
        #go to feed url and load
        self.driver.get('https://www.instagram.com/')
        height = int(2000)
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(self.driver.window_handles[0])
        for i in range(1,npics):
            print(i)
            time.sleep(3)
            height=int(height + (1000)) #scroll down height of about 1 pic
            self.driver.execute_script("window.scrollTo(0," + str(height) + ");")
            time.sleep(3)
            #get pics hrefs
            pics = self.driver.find_elements_by_class_name('c-Yi7')
            #find href links for all pics
            pic_hrefs = [elem.get_attribute('href') for elem in pics]
            #switch new tab
            self.driver.switch_to.window(self.driver.window_handles[1])
            #go href pic link
            self.driver.get(pic_hrefs[0])
            time.sleep(2)
            #try to click like button
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format('Like')).click()
                print('liked')
                time.sleep(3)
            except Exception as e:
                print(e)
                time.sleep(1)
            #back to original feed tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        end = time.time()
        print(end - start)
        freq = 2500  #2500 Hz
        duration = 1000  #1000 ms == 1 s
        winsound.Beep(freq, duration)
        time.sleep(0.5)
        winsound.Beep(freq, duration)
        time.sleep(0.5)
        winsound.Beep(freq, duration)

    def seefollowrequests(self):
        #go to follow requests page
        self.driver.get('https://www.instagram.com/accounts/activity/?followRequests=1')
        time.sleep(2)
        #get all users requesting _7WumH works but no href
        requestusers = self.driver.find_elements_by_class_name('FPmhX')
        #print number of requests
        print(len(requestusers))
        #get hrefs
        fulls = [elem.get_attribute('href') for elem in requestusers]
        
        #isolate all individual names
        allnames = []
        for elem in fulls:
            #split hrefs to try to isolate usernames
            splits = elem.split('/')
            #isolate only 4th elem (the username by itself)
            isouser = splits[3]
            allnames.append(isouser)
        print(allnames)
        #save request users' names
        self.requests = allnames
        


if __name__ == '__main__':
    #class instance for setting username, password
    igpy = Instahelp('username','password')

    #actual actions
    
    #login
    igpy.login()

    #like some pics    
    #igpy.readuserlist()
    #for user in igpy.userlist:
    #    igpy.likeuserpic(user, 2)
    #igpy.likepic(50)
    
    #confirm follow requests
    #igpy.seefollowrequests()
    #print(igpy.requests[:])
    #igpy.writeuserlist(igpy.requests[:])
    
    
    