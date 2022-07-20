import requests
import pytesseract
import cv2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url ='https://www.amazon.com/errors/validateCaptcha'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.delete_all_cookies()
driver.get(url)
driver.set_page_load_timeout(10)
driver.maximize_window()

image = driver.find_element(By.TAG_NAME, "img")
imageURL = image.get_attribute("src")
print(imageURL)


def solveCaptcha(img_name):
    img = Image.fromarray(img_name)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    print("Before result")
    result = pytesseract.image_to_string(img, config = " --psm 9")
    print(result)
    return result


driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver1.get(imageURL)
image = imageURL.split("/")
filename = image[len(image)-1].split(".")
driver1.save_screenshot(filename[0] + ".png")
img_name = filename[0] + ".png"
print(img_name)

img = cv2.imread(img_name)
print("shape:",img.shape)
img_resized= cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
cv2.imshow("REsized" ,  img_resized)
print("Image resized")
#crop_img = img[y:, x:x+w]

captcha_text = solveCaptcha(img_resized)
driver.find_element(By.ID,"captchacharacters").send_keys(captcha_text)
driver.find_element(By.CLASS_NAME, "a-button-text").click()


