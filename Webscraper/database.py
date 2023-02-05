import urllib.request
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS
from flask import Flask, jsonify, request
import pandas as pd
import re
# import beautifulsoup4 as bs4

# import the representatives with there appropriate party, and subcommittee
df = pd.read_csv('Webserver/database.csv')
print('Dataframe created')
df = df.replace('TBD', '', regex=True)

df['Chair Party'] = df['Chair'].str.extract(r'\((.*?)-*\)')
df['Ranking Member Party'] = df['Ranking Member'].str.extract(r'\((.*?)-*\)')
df['Chair'] = df['Chair'].str.extract(r'(.*)\(')
df['Ranking Member'] = df['Ranking Member'].str.extract(r'(.*)\(')
df['Chair'] = df['Chair'].str.replace(u'\xa0', '')
df['Ranking Member'] = df['Ranking Member'].str.replace(u'\xa0', '')
df['Subcommittee'] = df['Subcommittee'].fillna(0)

committes = list(df['Committee'].unique())
print(committes)

delegates = set(df['Chair']) | set(df['Ranking Member'])
# print(delegates)

subcommittees = {}
for ind, row in df.iterrows():
    if row['Committee'] not in subcommittees.keys():
        subcommittees[row['Committee']] = set()
    if row['Subcommittee'] != 0:
        subcommittees[row['Committee']].add(row['Subcommittee'])
print(subcommittees)


# import file with emails for representatives
contactInfo = list(open('Webserver/emails.txt',
                   encoding="utf8").read().splitlines())
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
    print(committee)
    committee_list = committee.split(', ')
    output = []
    for group in committee_list:
        output.append(subcommittees[group])
    print(output)
    return jsonify(output)


@app.route('/delegates', methods=['POST'])
def getDelegates():
    input_json = request.get_json()
    committe = input_json['committee']
    subcommittee = input_json['subcommittee']
    outputList = [('Billy Bob', '928-388-2838', 'someboday@gmail.com', '@someboday', 'R'),
                  ('Billy Bob2', '927-388-2838', 'somebody@gmail.com', '@soeboday', 'D')]
    return jsonify(outputList)


@app.route('/webscraper', methods=['POST'])
def webscraper():
    input_json = request.get_json()
    url = input_json['url']

#     r = requests.get(url)
# # convert to beautiful soup
#     soup = bs(r.content)
# # printing our web page
#     title_tag = soup.find_all('title')

    html = urllib.request.urlopen(url)

    htmlParse = bs(html, 'html.parser')

    s = ""
    for para in htmlParse.find_all("p"):
        s += para.get_text()
    s = s[:1000]

    t = ""
    for para in htmlParse.find_all("title"):
        t += para.get_text()

    # pass these two strings into an open ai method
    # open ai is going to pass back a list of committees
    # This is from Rakesh

    committee_list = committee.split(',')
    output = []
    for group in committee_list:
        output.append(subcommittees[group])
    print(output)
    return jsonify(output)
    # from there, we will pass these committees into a method that gives sub committees for every committee
    # This is from Rakesh
    # then open ai will rank the sub committeees, and output an ordered list of sub committees
    # then we will go in and find every single delegate for every single committees

    return jsonify({url: url, 'body': s})


if __name__ == '__main__':
    app.run()
