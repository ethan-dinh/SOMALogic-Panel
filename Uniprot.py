"""
Generating a list of UNIPROT IDs from GENOME NAMES
"""

# Importing Libraries
import csv
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 

# Importing CSV File for GENES
def import_csv(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        genes = []
        for row in csv_reader:
            genes.append(row[0])

    return genes   

# Configuring Selenium
chromedriver = "/Users/ethandinh/Desktop/Personal/Automated Scripts/chromedriver"
option = webdriver.ChromeOptions()
option.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
option.add_experimental_option("excludeSwitches", ['enable-automation'])
option.headless = True
s = Service(chromedriver)
driver = webdriver.Chrome(service=s, options=option)

def scrape(name) -> List:
    search_area = driver.find_element(By.ID, "query")
    search_area.clear()
    search_area.send_keys(name)
    search_area.send_keys(Keys.RETURN)

    for i in range(1,5):
        entry = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[3]").text
        if "HUMAN" in entry:
            print(driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]").text)
            return driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]").text

# Main Function --------------------------------
def main():
    #filename = input("Filename: ")
    filename = "gene_table.csv"
    gene_names = import_csv(filename)
    driver.get("https://www.uniprot.org/")
    
    rows = []
    for name in gene_names:
        try:
            rows.append([scrape(name)])
        except:
            continue
    
    with open("UniprotIDs.csv", 'w') as outFile:
        write = csv.writer(outFile)
        write.writerows(rows)

if __name__ == "__main__":
    main()