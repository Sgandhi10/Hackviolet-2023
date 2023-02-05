import pandas as pd
import re
# import beautifulsoup4 as bs4

# import the representatives with there appropriate party, and subcommittee
df = pd.read_csv('Webscraper/database.csv')
print('Dataframe created')
df = df.replace('TBD', '', regex=True)

df['Chair Party'] = df['Chair'].str.extract(r'\((.*?)-*\)')
df['Ranking Member Party'] = df['Ranking Member'].str.extract(r'\((.*?)-*\)')
df['Chair'] = df['Chair'].str.extract(r'(.*)\(')
df['Ranking Member'] = df['Ranking Member'].str.extract(r'(.*)\(')
df['Chair'] = df['Chair'].str.replace(u'\xa0', '')
df['Ranking Member'] = df['Ranking Member'].str.replace(u'\xa0', '')

committes = list(df['Committee'].unique())
# print(committes)

delegates = set(df['Chair']) | set(df['Ranking Member'])
# print(delegates)

subcommittees = {}
for ind, row in df.iterrows():
    if row['Committee'] not in subcommittees.keys():
        subcommittees[row['Committee']] = set()
    subcommittees[row['Committee']].add(row['Subcommittee'])
print(subcommittees)


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

# Flask portion of the code
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/committees', methods=['GET'])
def getCommittees():
    data = {
        'committees': committes
    }
    return jsonify(data)

@app.route('/subcommittees', methods=['POST'])
def getSubCommittees():
    input_json = request.get_json()
    committee = input_json['committee']
    return jsonify(subcommittees[committee])

@app.route('/delegates', methods=['POST'])
def getDelegates():
    input_json = request.get_json()
    committe = input_json['committee']
    subcommittee = input_json['subcommittee']
    outputList = [('Billy Bob', '928-388-2838', 'someboday@gmail.com', '@someboday', 'R'), 
                  ('Billy Bob2', '927-388-2838', 'somebody@gmail.com', '@soeboday', 'D')]
    # tmp = df[(df['Committee'] == committe) & (df['Subcommittee'] == subcommittee)]
    return jsonify(outputList)

@app.route('/webscraper', methods=['POST'])
def webscraper():
    input_json = request.get_json()
    url = input_json['url']
    print(url)
    return jsonify({url: True})
    
if __name__ == '__main__':
    app.run()
