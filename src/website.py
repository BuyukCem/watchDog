#!/usr/bin/env python3
import requests

import os
import time
from utils import util
from src import image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request
import urllib.parse

class WebSite:
    def __init__(self, webSiteUrl):
        self.url = webSiteUrl
        self.FolderName = self.url.replace('/', '-')
        self.statusCode = 0
        self.listScrennshotReference = []
        # self.WebImageReference = imgName.replace('/', '-')

    def webBrowsingOption(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(chrome_options=chrome_options)

    def getResponseCode(self):
        status = requests.get("http://" + self.url)
        self.statusCode = status
        return status.status_code

    def timeToLoad(self):
        driver = self.webBrowsingOption()
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")

        ''' Calculate the performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart

        print("Back End: %s" % backendPerformance_calc)
        print("Front End: %s" % frontendPerformance_calc)

        driver.quit()

    def findElementById(self, findEllement):
        driver = self.webBrowsingOption()
        data = driver.find_elements_by_id(findEllement)
        print(type(data))
        if len(data) != 0:
            print("We find ID " + findEllement)
            print(data)
        else:
            print("We did not find your item")
            print(data)
        driver.quit()

    def takeScreenshot(self):
        driver = webdriver.Chrome()
        driver.get("http://" + self.url)
        height = driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight )")
        driver.quit()

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument(f"--window-size=1920,{height}")
        chrome_options.add_argument("--hide-scrollbars")
        return webdriver.Chrome(chrome_options=chrome_options)

    def createReference(self):
        # FolderReference
        folder = "./img/screenshotReference/" + self.FolderName + "/"
        # Reference File Picture
        timestr = time.strftime("%d-%m-%Y_%I-%M-%S")
        fileName = timestr + '.png'

        ListFolder = os.listdir("../public/img/screenshotReference/")
        if not util.search(ListFolder, folder):
            try:
                os.mkdir("./public/img/screenshotReference/" + self.FolderName)
            except OSError:
                print(
                    "Creation of the directory " + self.FolderName + " failed ./img/screenshotReference/" + self.FolderName)

        self.listScrennshotReference.append(fileName)

        driver = self.takeScreenshot()
        driver.get("http://" + self.url)
        driver.save_screenshot(folder + fileName)

    def createComparerPicture(self):
        folder = "./public/img/controleScreenshot/" + self.FolderName + "/"

        timestr = time.strftime("%d-%m-%Y_%I-%M-%S")
        fileName = timestr + '.png'

        ListFolder = os.listdir("../public/img/controleScreenshot/")
        if not util.search(ListFolder, folder):
            try:
                os.mkdir("./img/controleScreenshot/" + self.FolderName)
            except OSError:
                print(
                    "Creation of the directory " + self.FolderName + " failed ./img/controleScreenshot/" + self.urlName)

        driver = self.takeScreenshot()
        driver.get("http://" + self.url)
        driver.save_screenshot(folder + fileName)

    def findWordInPicture(self, word, picture_dir):
        data = image.findWordInPicture(word, picture_dir)
        if data:
            print('its true')
        else:
            print('its false')

    # TODO change this code
    global var_log
    var_log = "Pourcentage de modifications = "

    def writeLog(self, param):
        global var_log
        var_log += str(param)

    def comparePicture(self):
        self.writeLog(image.pictureCompare())
        print(" " + str(var_log))
        image.getDiff()

    def test(self):
        # enable browser logging
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Chrome(desired_capabilities=d)

        # load the desired webpage
        driver.get('http://symbiosys.com')

        # print messages
        for entry in driver.get_log('driver'):
            print(entry)
            # print messages
        for entry in driver.get_log('browser'):
            print(entry)
        print(driver.log_types)

    # TODO "Finir la fonction car y'a pas de token"
    def GetPageSpeedScore(self, deviceType):
        url = self.url
        device_type = deviceType

        # Making request
        contents = urllib.request.urlopen(
            'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy={}' \
                .format(url, device_type)
        ).read().decode('UTF-8')
        print(contents)

