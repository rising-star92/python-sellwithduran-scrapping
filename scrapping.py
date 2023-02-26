from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import wget
import gzip
import os
import xml.etree.ElementTree as ET
from videogen import generateVideo

def downAndExtract(_target):
    response = wget.download(_target, "temp.gz")
    with gzip.open("temp.gz", "rb") as f:
        xml_file = f.read()

    os.remove("temp.gz")

    return xml_file

def getUrls(_xml):
    root = ET.fromstring(xml_file)   # parse the xml content to root element 
    urls = []   # create an empty list to store all urls from xml content 
    for item in root:   # loop through each item in root element 
        urls.append(item[0].text)   # append each url to urls list

    return urls

def parsing(url):
    print("Loading page... ")

    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    # driver.maximize_window()
    driver.implicitly_wait(30)

    driver.get(url)

    mls_ele = driver.find_element(By.XPATH, "//strong[text()='MLS#']/following-sibling::span")
    mls_str = mls_ele.text

    if not os.path.exists(mls_str):
        os.mkdir(mls_str)
        
    os.chdir(mls_str)

    print("Downloading images... ")
    imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'owl-lazy')]")
    image_count = 0
    for img in imgResults:
        if (img.get_attribute('data-src') != None):
            image_count += 1
            wget.download("https://" + img.get_attribute('data-src').split("/https://")[1])

    print("Scrapping data... ")

    data = ET.Element('root')

    ET.SubElement(data, "URL").text = url

    ET.SubElement(data, "MLS").text = mls_str

    address_ele = driver.find_element(By.XPATH, "//div[text()='Address']/following-sibling::div")
    ET.SubElement(data, 'Address').text = address_ele.text

    type_ele = driver.find_element(By.XPATH, "//div[text()='Type']/following-sibling::div")
    ET.SubElement(data, "Type").text = type_ele.text
    
    price_ele = driver.find_element(By.XPATH, "//div[text()='Price']/following-sibling::div")
    ET.SubElement(data, "Price").text = price_ele.text

    description_ele = driver.find_element(By.XPATH, "//h5[text()='Property Description']/following-sibling::p")
    ET.SubElement(data, "Description").text = description_ele.text

    bedroom_ele = driver.find_element(By.XPATH, "//strong[text()='Bedrooms']/following-sibling::span")
    ET.SubElement(data, "Bedrooms").text = bedroom_ele.text

    fbathroom = driver.find_element(By.XPATH, "//strong[text()='Full Bathrooms']/following-sibling::span")
    hbathroom = driver.find_element(By.XPATH, "//strong[text()='Half Bathrooms']/following-sibling::span")
    bathrooms = int(fbathroom.text) + int(hbathroom.text)
    ET.SubElement(data, "Bathrooms").text = str(bathrooms)

    subtype_ele = driver.find_element(By.XPATH, "//b[contains(text(),'Property SubType')]/..//..//td")
    ET.SubElement(data, "PropertySubType").text = subtype_ele.text

    proptype_ele = driver.find_element(By.XPATH, "//b[contains(text(),'Property Type')]/..//..//td")
    ET.SubElement(data, "PropertyType").text = proptype_ele.text

    ET.SubElement(data, "Photos").text = str(image_count)

    mydata = ET.tostring(data)  
    myfile = open("data.xml", "wb")
    myfile.write(mydata)

    path = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(path, os.pardir)))


    print("Completed: Saved Data for ", mls_str)
    return mls_str

if __name__ == "__main__":
    # url = input()
    print("\nDownloading and extracting site map data... \n")
    xml_file = downAndExtract("https://s3.amazonaws.com/kunversion-frontend-sitemaps/sellwithduran.com/sitemap-listings-1.xml.gz")

    print("\n\nGetting URLs...")
    urls = getUrls(xml_file)

    print("\n\nProcessing...")

    if not os.path.exists("results"):
        os.mkdir("results")

    os.chdir("results")

    for url in urls:
        print("\n---------- ", url, " ----------")
        path = parsing(url)
        generateVideo(path)
        