from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
import praw
import csv
import datetime
import json
import pandas as pd

app = Flask(__name__)
CORS(app, support_credentials=True)

username = "digitalchaos123"
password = "digitalchaos123"
clientid = "8Lqn66LhUBDv-w"
clientsecret = "hpMcf-vtl5TTvTc1jfm85GoJJ_Q"

def mine_reddit():
    def writeheaders():
        f.writerow(["Number", "Keyword", "Title", "Score", "Comments", "URL", "Domain", "Permalink", "ID", "Subreddit",
                    "CreatedDate"])

    def writefields():
        f.writerow([startNum, search.strip(), submission.title,
                    submission.score, submission.num_comments,
                    submission.url, submission.domain, submission.permalink, submission.id,
                    submission.subreddit, datetime.datetime.utcfromtimestamp(submission.created).strftime('%m-%d-%Y')])

    reddit = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         password=password,
                         user_agent='Reddit search data extractor by /u/' + username + '',
                         username=username)

    print("Authentication for " + str(reddit.user.me()) + " is verified. Proceeding.\r\n")

    outfilename = 'reddit.csv'
    # search =
    sortsub = 'relevance'
    filtersub = 'No'
    search=request.form.get('file')
    search_list=list(search.split(','))
    print(search_list)


    if (filtersub.lower() == "yes"):
        subreddit = input("Enter the subreddit names delimited with commas (i.e., BigSEO):\r\n")
        subreddit_list = subreddit.split(',')
        file = open(outfilename, "w+", newline="\n", encoding="utf-8")
        f = csv.writer(file)
        writeheaders()
        for subs in subreddit_list:
            for search in search_list:
                startNum = 0
                for submission in reddit.subreddit(subs.strip()).search(search, sort=sortsub):
                    startNum += 1
                    writefields()
                print(
                    "Writing out posts results for the search '" + search.strip() + "' in 'r/" + subs.strip() + "'\r\n")
            file.close
    else:
        file = open(outfilename, "w+", newline="\n", encoding="utf-8")
        f = csv.writer(file)
        writeheaders()
        for search in search_list:
            startNum = 0
            for submission in reddit.subreddit('all').search(search.lower(), sort=sortsub):
                startNum += 1
                writefields()
            print("Writing out posts results for the search '" + search.strip() + "' in 'r/all'\r\n")
        file.close

    reddit = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         password=password,
                         user_agent='Reddit search data extractor by /u/' + username + '',
                         username=username)

    print("Authentication for " + str(reddit.user.me()) + " is verified. Proceeding.\r\n")

def preprocess():
    df=pd.read_csv('reddit.csv')
    df=pd.DataFrame(df)
    df=df.groupby('Keyword').head(5)
    df=df[['Keyword','URL','Domain','Permalink','Subreddit','CreatedDate']]
    Row_list=[]
    for index,rows in df.iterrows():
        my_list=[rows.Keyword,rows.URL,rows.Domain,rows.Permalink,rows.Subreddit,rows.CreatedDate]
        Row_list.append(my_list)
    return Row_list



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/reddit',methods=['POST'])
def go():
    mine_reddit()
    Rlist=[]
    Rlist=preprocess()
    return jsonify(Rlist)


@app.route('/hello',methods=['GET'])
def getitem():
    search=request.form.get('file')
    #print(search_list)
    search_list=list(search.split(','))
    print(search_list)
    print(type(search_list))
    return jsonify(search_list)


if __name__ == '__main__':
    app.run(port='5001',debug=True)
