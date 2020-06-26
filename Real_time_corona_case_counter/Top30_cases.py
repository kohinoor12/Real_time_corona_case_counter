import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = 'https://www.worldometers.info/coronavirus/'
r = requests.get(url)

data = r.text
soup = BeautifulSoup(data,'html.parser')

print(soup.title.text)
print()
live_data = soup.find_all('div',id='maincounter-wrap')
for i in live_data:
	print(i.text)

print()
print('Analysis based on individual countries')
print()

table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

countries = []
cases = []
todays = []
deaths = []

for tr in table_rows:
	td = tr.find_all('td')
	countries.append(td[0].text)
	cases.append(td[1].text)
	todays.append(td[2].text.strip())
	deaths.append(td[3].text.strip())

indices = [i for i in range(1,len(countries)+1)]
headers = ['Countries','Total Cases','Todays Cases','Total Deaths']
df = pd.DataFrame(list(zip(countries,cases,todays,deaths)),index=indices,columns=headers)
df30 = df.head(38)
print(df30)

# Saving it to csv file
df30.to_csv('corona-Top30.csv')

# plotting a graph
cases_sliced = cases[8:38]
countries_sliced = countries[8:38]

y_pos = list(range(len(countries_sliced)))

plt.bar(y_pos,cases_sliced[::-1],align='center',alpha=0.5)
plt.xticks(y_pos,countries_sliced[::-1],rotation=70)
plt.ylabel('Total cases')
plt.title('Population affected by Corona virus')
plt.savefig('Corona-Top30.png',dpi=600)
plt.show()
