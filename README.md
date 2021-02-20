# Google Sheets - Automated Data Upload

Part of my role at ![ASRomaData](https://twitter.com/ASRomaData) is to come up with ways to support the page. This includes discovering new ways to scrape data, create charts or to automate certain processes. After the first bigger project, where a ![Twitter Bot](https://github.com/ttothuk-proj/tweepy_match_summary) was created the next big task was to gather players' minutes and match data.  
The best place for such tasks is ![fbref](https://fbref.com/en/squads/cf74a709/Roma-Stats) - where most of the data is available and it is reliable. 

To gather the numbers Python's BeautifulSoup library is used and then on Pandas is helping to manipulate the data. Each Roma player's game is recorded and the data, opponent and the minutes are extracting. To link it up with external data on the squad's performance, fbref keeps record on the matches, from where each game's date, opponent, scores, shots and xG score is acquired. All the data is merged based on the date of the games, since it is a unique variable and there are no 2 games on the same day.  

Once the dataframe is ready it is then uploaded to Google Sheets using the oauth2client and the pygsheets library.

![chart.png]

![gsheets.png]
