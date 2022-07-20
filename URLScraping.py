import json
import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from csv import DictReader
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class URLScraping():

    def setUp(self):
        options = Options()
        options.headless = True
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(10)
        self.driver.maximize_window()

    def scrape_url_data(self,url):

         dict = {}
         dict1 = {}

         self.driver.get(url)

         try:

                product = self.driver.find_element("id", "productTitle")
                title = product.text

                image = self.driver.find_element("id", "imgBlkFront")
                imageURL = image.get_attribute("src")

                try:
                   price = self.driver.find_element(By.CLASS_NAME,"a-color-price").text
                except:
                    price = self.driver.find_element(By.CLASS_NAME, "a-color-base").text

                dict1 = {'title': title, 'imageURL' : imageURL, 'price' : price}

                details = self.driver.find_elements(By.XPATH,'//div[@id="detailBullets_feature_div"]/ul/li')

                dict2 = {}
                for item in details:
                    lst = []
                    desc = item.find_element(By.CLASS_NAME,"a-list-item").text
                    # print(desc)
                    lst = desc.split(":")
                    dict2[lst[0]] = lst[1]

                dict = {'product': dict1, 'details': dict2}
                return(dict)

         except Exception as e:
                print("URL not found", url)
                with open('Exceptions.csv', 'a', newline='') as csv_file:
                    except_file = csv.writer(csv_file)
                    except_file.writerow(url.split((" ")))
                    csv_file.close()


    def writejsonFile(self, data):
        jsonString = json.dumps(data, indent =2)

        with open('data.json', 'w') as jsonFile:
            jsonFile.write(jsonString)
            jsonFile.close()


    def Readcsv(self):
        user = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36"
        }

        data = []

        try:
            with open('Amazon_Scraping.csv', 'r') as csv_file:
                #csv_reader = csv.reader(csv_file, delimiter =",")
                csv_reader = DictReader(csv_file, delimiter =",")
                count=0
                for row in csv_reader:
                    str =""
                    str = "https://www.amazon.{}/dp/{}"
                    url = str.format(row['country'], row['Asin'])
                    if (count < 101):
                        scode= ""
                        scode = requests.get(url,headers= user).status_code
                        if (scode != 404):
                           product = self.scrape_url_data(url)
                           data.append(product)
                           count += 1
                        else:
                            print("URL not found", url)
                    else:
                        break

            clean_data = list(filter(None, data))
            self.writejsonFile(clean_data)
        except Exception as e:
            print(e)
        finally:
            csv_file.close()

    def tearDown(self):
        self.driver.close()
        self.driver.quit()



obj = URLScraping()
obj.setUp()
obj.Readcsv()