import pandas as pd
import sqlite3
import re

# import the representatives with there appropriate party, and subcomittee
df = pd.read_csv('Webscraper\database.csv')
print('Dataframe created')
df = df.replace('TBD', '', regex=True)

df['Chair Party'] = df['Chair'].str.extract(r'\((.*?)-*\)')
df['Ranking Member Party'] = df['Ranking Member'].str.extract(r'\((.*?)-*\)')
df['Chair'] = df['Chair'].str.extract(r'(.*)\(')
df['Ranking Member'] = df['Ranking Member'].str.extract(r'(.*)\(')
df['Chair'] = df['Chair'].str.replace(u'\xa0', '')
df['Ranking Member'] = df['Ranking Member'].str.replace(u'\xa0', '')

committes = set(df['Committee'])
# print(committes)

delegates = set(df['Chair']) | set(df['Ranking Member'])
# print(delegates)



# import file with emails for representatives
contactInfo = list(open('Webscraper/emails.txt', encoding="utf8").read().splitlines())
repInfo = {}
index = 0
while index < len(contactInfo):
    if contactInfo[index].startswith('Rep.') | contactInfo[index].startswith('Sen.'):
        name = re.split(r'Rep.|Sen.', contactInfo[index])[1].strip()
        phone = email = twitter = ''
        index += 1
        if contactInfo[index].startswith('Phone:'):
            phone = re.split(r'Phone:', contactInfo[index])[1].strip()
            index += 1
        if contactInfo[index].startswith('Email:'):
            email = re.split(r'Email:', contactInfo[index])[1].strip()
            index += 1
        if contactInfo[index].startswith('Twitter:'):
            twitter = re.split(r'Twitter:', contactInfo[index])[1].strip()
            index += 1
        repInfo[name] = (phone, email, twitter)
    else:
        index += 1
missing = delegates - repInfo.keys()
print('Missing: ', len(missing), missing)


# add emails to the representatives in df



df.to_csv('Webscraper\database-updated.csv', index=False)

df.to_sql('data', sqlite3.connect('data.db'), if_exists='replace')
print('Database created')

