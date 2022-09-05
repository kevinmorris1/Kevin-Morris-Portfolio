import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

standings_url = "https://www.baseball-reference.com/"

def getTeamURLs(url):
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text, features='lxml')
    tables = soup.select('table#standings_AL') + soup.select('table#standings_NL')

    urls = []
    for t in tables:
        links = t.find_all('a')
        links = [l.get("href") for l in links] 
        links = [f"https://www.baseball-reference.com{l}" for l in links] 
        urls = urls + links
        return urls

def generateDataFrame(urls):
    df = pd.DataFrame()
    for i in range(len(urls)):
        url = urls[i] # first club page link
        print(url)
        data = requests.get(url) 

        soup = BeautifulSoup(data.text, features='lxml') # extract all information from page
        links = soup.find_all('a') # find all links on page for the club
        links = [l.get("href") for l in links] # get reference urls for those links
        links = [l for l in links if l and (('schedule-scores' in l))]
        links = [*set(links)][0]

        sch_url = f"https://www.baseball-reference.com{links}"
        data = requests.get(sch_url) 
        sch = pd.read_html(data.text, match='Team Game-by-Game Schedule')[0]

        df = df.append(sch)
        time.sleep(1)
    return schedule


team_urls = getTeamURLs(standings_url)
schedule = generateDataFrame(team_urls)

schedule.to_csv('schedule.csv', index=False)