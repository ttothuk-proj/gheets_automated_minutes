import pandas as pd
import numpy as np

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests

from datetime import datetime
now = datetime.today().strftime('%Y-%m-%d')

url = "https://fbref.com/en/squads/cf74a709/Roma-Stats"
response = requests.get(url, headers={'User-Agent': 'Custom5'})
# print(response.status_code)

page_data = response.text
soup = soup(page_data, 'html.parser')

players = soup.tbody.findAll('tr')
# print(len(players))

pretag = "https://fbref.com"

df = pd.read_html(pretag + players[0].findAll("td", {"class": "left group_start"})[0].a['href'])[0]
df.columns = df.columns.droplevel()
df = df[df['Squad'].notna()]
df = df[df["Squad"].str.contains("Roma")]
df = df[["Date", "Min"]]
df.columns = ["Date", players[0].findAll("th")[0].text]

for i in range(1,len(players)):
    df2 = pd.read_html(pretag + players[i].findAll("td", {"class": "left group_start"})[0].a['href'])[0]
    df2.columns = df2.columns.droplevel()
    df2 = df2[df2['Squad'].notna()]
    df2 = df2[df2["Squad"].str.contains("Roma")]
    df2 = df2[["Date", "Min"]]
    df2.columns = ["Date", players[i].findAll("th")[0].text]
    
    df = pd.merge(df, df2, on="Date", how="outer")  

df.replace(np.nan, 0, inplace=True)
df = df.replace(['On matchday squad, but did not play'], 0)
df.loc[:, "Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")


df_matches = pd.read_html("https://fbref.com/en/squads/cf74a709/Roma-Stats")[1]
df_matches2 = df_matches[["Date", "Opponent","GF","GA","xG", "xGA", "Poss"]]
df_matches2.loc[:, "Date"] = pd.to_datetime(df_matches2["Date"])
df_matches2 = df_matches2[df_matches2["Date"] <= now]

df = pd.merge(df, df_matches2, on="Date", how="outer")

col = df.pop("Opponent")
df.insert(1, col.name, col)

col2 = df.pop("GF")
df.insert(2, col2.name, col2)

col3 = df.pop("GA")
df.insert(3, col3.name, col3)

col4 = df.pop("xG")
df.insert(4, col4.name, col4)

col5 = df.pop("xGA")
df.insert(5, col5.name, col5)

col6 = df.pop("Poss")
df.insert(6, col6.name, col6)

df = df.T

df.columns = df.iloc[0]
df = df.iloc[1:,:]

df.to_csv("minuti.csv",encoding='utf-8-sig')

from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pygsheets

df = pd.read_csv("minuti.csv")
gc = pygsheets.authorize(service_file='creds.json')

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13xVfocgRtGI6PSmL-qOt_Pq52qmQ-Sbz8qSBUJE9Qjk/edit?ts=6000cf77#gid=1698030870')
wks = sh[4]

wks.set_dataframe(df,'A1')
