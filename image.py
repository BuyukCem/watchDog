#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import util
from skimage.measure import compare_ssim
import cv2
import cv2 as cv
import imutils
import numpy as np

'''
def saveScreenshotReference(driver, WebImageReference):
    arr = os.listdir("./img/screenshotReference/")
    print(arr)
    if util.search(arr, WebImageReference):
        print("il y a un image de reference nous allons la supprimer")
        file = "./img/screenshotReference/" + WebImageReference
        os.remove(file)

    driver.save_screenshot("./img/screenshotReference/" + WebImageReference)


def saveScrennComparerPicture(driver, filename, folederName):
    print("hello")
    arr = os.listdir("./img/controleScreenshot/" + folederName)
    path = "./img/controleScreenshot/" + folederName
    #driver.save_screenshot(path)

    # def findRefernceScreenshot(self, reference):
    # def picturesCompare:
    # def getDiff:

'''


def pictureCompare():
    # Path image
    ReferencePict = "./img/screenshotReference/www.symbiosys.com-fr-be-/23-05-2020_11-28-03.png"
    imageA = "./img/controleScreenshot/www.symbiosys.com-nl-be-/23-05-2020_11-26-15.png"

    #ReferencePict = "./img/screenshotReference/www.symbiosys.com-fr-/23-05-2020_10-03-47.png"
    #imageA = "./img/controleScreenshot/www.symbiosys.com-fr-/23-05-2020_10-04-45.png"

    ReferencePicture = cv.imread(ReferencePict)
    src_imageA = cv.imread(imageA)

    hsv_base = cv.cvtColor(ReferencePicture, cv.COLOR_BGR2HSV)
    hsv_test1 = cv.cvtColor(src_imageA, cv.COLOR_BGR2HSV)

    hsv_half_down = hsv_base[hsv_base.shape[0] // 2:, :]
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]

    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists

    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    hist_half_down = cv.calcHist([hsv_half_down], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_half_down, hist_half_down, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    # for compare_method in range(4):
    compare_method = 1
    base_base = cv.compareHist(hist_base, hist_base, compare_method)
    # base_half = cv.compareHist(hist_base, hist_half_down, compare_method)
    base_test1 = cv.compareHist(hist_base, hist_test1, compare_method)
    # base_test2 = cv.compareHist(hist_base, hist_test2, compare_method)
    print('Method:', compare_method, 'Perfect, Base-Test(1) :', \
          base_base, '/', base_test1)
    return base_test1


def getDiff():
    imageA = "./img/screenshotReference/www.symbiosys.com-fr-be-/23-05-2020_11-28-03.png"
    imageB = "./img/controleScreenshot/www.symbiosys.com-nl-be-/23-05-2020_11-26-15.png"

    # Path image
    # imageA = "./img/screenshotReference/www.symbiosys.com-fr-/23-05-2020_10-03-47.png"
    #imageB = "./img/controleScreenshot/www.symbiosys.com-fr-/23-05-2020_10-04-45.png"

    # load the two input images
    imageA = cv2.imread(imageA)
    imageB = cv2.imread(imageB)

    print(imageA.shape)
    print(imageB.shape)
    imagesize = imageA.shape
    imageB = cv2.resize(imageB, (imagesize[1], imagesize[0]))

    print(imageA.shape)
    print(imageB.shape)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("image", grayB)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite("./img/" + "delta" + "test" + ".png", imageB)
    '''
    # show the output images
     cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imwrite(dirpath + "delta" + domain + ".png", imageB)
    # cv2.imshow("Diff", diff)
    # cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    '''
