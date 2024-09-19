from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import pandas as pd

startTime = datetime.now()

chrome_path = '../chromedriver/chromedriver.exe' 
chrome_options = Options()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(chrome_path, options=chrome_options, keep_alive=False)
url = "https://www.insidearbitrage.com/insider-sales/"
driver.get(url)

ticker_list = []
relation_list = []
date_list = []
cost_list = []
share_list = []
held_shares_list = []

for i in range(1,101):
    # ticker of stock
    ticker_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[1]/a"""
    ticker = driver.find_element_by_xpath(ticker_path)
    ticker_list.append(ticker.text)
    
    # relation to company
    relation_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[5]"""
    relation = driver.find_element_by_xpath(relation_path)
    relation_list.append(relation.text)
    
    # date of trade
    date_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[6]/span"""
    date = driver.find_element_by_xpath(date_path)
    date_list.append(date.text)
    
    # cost of each share
    cost_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[7]"""
    cost = driver.find_element_by_xpath(cost_path)
    cost_list.append(cost.text)
    
    # number of shares being traded
    share_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[8]"""
    share = driver.find_element_by_xpath(share_path)
    share_list.append(share.text)

    # number of held shares by the specific individual
    held_share_path = f"""//*[@id="sortTableM"]/tbody/tr[{i}]/td[10]"""
    held_share = driver.find_element_by_xpath(held_share_path)
    held_shares_list.append(held_share.text)

driver.close()

data = pd.DataFrame({
    'ticker': ticker_list,
    'relation': relation_list,
    'date': date_list,
    'cost': cost_list,
    'shares': share_list,
    'held_shares': held_shares_list
})

print(data.head())

save_dir = '../data'

if not os.path.exists(save_dir):
    os.mkdir(save_dir)
    
data.to_csv(os.path.join(save_dir, 'data.csv'))

endtime = f"Execution Time: {datetime.now() - startTime}"
print(endtime)