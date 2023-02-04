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


print(df.head())

committes = set(df['Committee'])
print(committes)

delegates = set(df['Chair']) | set(df['Ranking Member'])
# print(delegates)



# import file with emails for representatives
contactInfo = list(open('emails.txt').read().splitlines())
repEmails = {}
index = 0
while index < len(contactInfo):
    if contactInfo[index].startswith('Rep.'| 'Sen.'):
        name = contactInfo[index].split()


# add emails to the representatives in df



df.to_csv('Webscraper\database-updated.csv', index=False)

df.to_sql('data', sqlite3.connect('data.db'), if_exists='replace')
print('Database created')

