import requests
from bs4 import BeautifulSoup as bs
from configparser import ConfigParser
from configure import reading_config
import pandas as pd
import sqlite3



# Reading config file 
company_list = reading_config()

for i in company_list:
    url = 'https://finance.yahoo.com/quote/'+ i +'/history?p='+ i
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    reqs = requests.get(url,headers=headers,timeout=5)
    soup = bs(reqs.content)

    table = soup.find('table')
    rows = table.find_all('tr')
    list_cells =[]
    for row in rows[1:-1]:
        cells = row.find_all(['td','th'])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        if len(cells_text)>3:
            list_cells.append(cells_text)
    
    # Extracting headers 
    company_headers = []
    for i in table.find_all('th'):
        title = i.text
        company_headers.append(title)

    # creating dataframe of data
    mydata = pd.DataFrame(list_cells,columns=company_headers)

    # Connecting pandas and sql to add dataframe to sql database

    conn = sqlite3.connect('test_database')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS CompanyData (Date text, Open number, High number, Low number, Close number, Adj Close number, Volume number)')
    conn.commit()

    mydata.to_sql( 'CompanyData' , conn, if_exists='append', index = False)
