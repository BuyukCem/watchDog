#!/usr/bin/env python3
import requests
import subprocess

import os
import time
import util
import image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebSite:
    def __init__(self, webSiteUrl):
        self.url = webSiteUrl
        self.FolderName = self.url.replace('/', '-')

        self.statusCode = 0
        self.listScrennshotReference = []
        # self.WebImageReference = imgName.replace('/', '-')

    def webBrowsing(self):
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
        driver = self.webBrowsing()
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")

        ''' Calculate the performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart

        print("Back End: %s" % backendPerformance_calc)
        print("Front End: %s" % frontendPerformance_calc)

        driver.quit()

    def findElement(self, findEllement):
        # menu-item-6321
        driver = self.webBrowsing()
        data = driver.find_elements_by_id(findEllement)
        print(type(data))
        if len(data) != 0:
            print("We find ID " + findEllement)
            print(data)
        else:
            print("We did not find your item")
            print(data)

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

        ListFolder = os.listdir("./img/screenshotReference/")
        if not util.search(ListFolder, folder):
            try:
                os.mkdir("./img/screenshotReference/" + self.FolderName)
            except OSError:
                print(
                    "Creation of the directory " + self.FolderName + " failed ./img/screenshotReference/" + self.FolderName)

        self.listScrennshotReference.append(fileName)

        driver = self.takeScreenshot()
        driver.get("http://" + self.url)
        driver.save_screenshot(folder + fileName)

    def createComparerPicture(self):
        folder = "./img/controleScreenshot/" + self.FolderName + "/"

        timestr = time.strftime("%d-%m-%Y_%I-%M-%S")
        fileName = timestr + '.png'

        ListFolder = os.listdir("./img/controleScreenshot/")
        if not util.search(ListFolder, folder):
            try:
                os.mkdir("./img/controleScreenshot/" + self.FolderName)
            except OSError:
                print(
                    "Creation of the directory " + self.FolderName + " failed ./img/controleScreenshot/" + self.urlName)

        driver = self.takeScreenshot()
        driver.get("http://" + self.url)
        driver.save_screenshot(folder + fileName)

    global var_log
    var_log = "Pourcentage de modifications = "
    def writeLog(self, param):
        global var_log
        var_log += str(param)

    def comparePicture(self):
        self.writeLog(image.pictureCompare())
        print(" "+str(var_log))
        image.getDiff()
