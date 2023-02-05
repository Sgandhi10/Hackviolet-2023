import urllib.request
from bs4 import BeautifulSoup as bs
from flask_cors import CORS
from flask import Flask, jsonify, request
import pandas as pd
import re
import os
import openai
from dotenv import load_dotenv

# import the representatives with there appropriate party, and subcommittee
df = pd.read_csv('database.csv')
print('Dataframe created')
df = df.replace('TBD', '', regex=True)

df['Chair Party'] = df['Chair'].str.extract(r'\((.*?)-*\)')
df['Ranking Member Party'] = df['Ranking Member'].str.extract(r'\((.*?)-*\)')
df['Chair'] = df['Chair'].str.extract(r'(.*)\(')
df['Ranking Member'] = df['Ranking Member'].str.extract(r'(.*)\(')
df['Chair'] = df['Chair'].str.replace(u'\xa0', '')
df['Ranking Member'] = df['Ranking Member'].str.replace(u'\xa0', '')
df['Subcommittee'] = df['Subcommittee'].fillna(0)

committees = list(df['Committee'].unique())

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
contactInfo = list(open('emails.txt',
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


# @app.route('/committees', methods=['GET'])
# def getCommittees():
#     data = {
#         'committees': committes
#     }
#     return jsonify(data)


@app.route('/subcommittees', methods=['POST'])
def getSubCommittees():
    input_json = request.get_json()
    committee = input_json['committee']
    print(committee)
    committee_list = committee.split(', ')
    output = []
    for group in committee_list:
        output += subcommittees[group]
    print(output)
    return jsonify(output)


@app.route('/delegates', methods=['POST'])
def getDelegates():
    input_json = request.get_json()
    committee = input_json['committee']
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

    paragraph = ""
    for para in htmlParse.find_all("p"):
        paragraph += para.get_text()
    paragraph = paragraph[:1000]

    title = ""
    for para in htmlParse.find_all("title"):
        title += para.get_text()

    # pass these two strings into an open ai method
    # open ai is going to pass back a list of committees that are most relevant to the text
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    openai.Model.list()
    prompt = "Given these political committees: " + \
        ";".join(committees) + ". Tell me which 3 committees are most relevant to the following text separated by semi-colons (i.e. x,y,z): \n" + title + "\n" + paragraph
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0
    )
    # list of committees returned by openai
    committee = response['choices'][0]['text']

    # from there, we will pass these committees into a method that gives sub committees for every committee
    committee_list = committee.split(';')
    subcommittees = []
    for group in committee_list:
        subcommittees += subcommittees[group]

    # then open ai will rank the sub committeees, and output an ordered list of sub committees
    prompt2 = "Given these political committees: " + \
        ";".join(subcommittees) + "Rank the committees based on how relevant they are to the following text in a python-styled list like so x,y,z:" + paragraph
    response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt2,
        temperature=0
    )
    # ranked_subcommittees = response['choices'][0]['text']
    # then we will go in and find every single delegate for every single committees

    outputList = [('Billy Bob', 'someboday@gmail.com', '@someboday'),
                  ('Billy Bob2', 'somebody@gmail.com', '@soeboday')]

    return jsonify({"delegates": outputList})


if __name__ == '__main__':
    app.run()
