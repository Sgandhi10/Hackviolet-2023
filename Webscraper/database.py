import pandas as pd
import sqlite3

# import the representatives with there appropriate party, and subcomittee
df = pd.read_csv('Webscraper\database.csv')
print('Dataframe created')
df = df.replace('TBD', '', regex=True)
print(df.head())

committes = set(df['Committee'])
print(committes)

delegates = set(df['Chair']) | set(df['Ranking Member'])
print(delegates)

# import file with emails for representatives
# emails_file = open("emails.txt", "rb").read().decode(encoding='utf-8', errors='ignore')
# repEmails = {}
# for line in emails_file.splitlines():
#     if line.startswith('Sen.' | 'Rep.'):
#         name = line.match()


# add emails to the representatives in df



df.to_csv('Webscraper\database-updated.csv', index=False)

df.to_sql('data', sqlite3.connect('data.db'), if_exists='replace')
print('Database created')

