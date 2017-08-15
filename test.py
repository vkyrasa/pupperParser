#!/usr/bin/python
import praw
import requests
import json
from ConfigParser import ConfigParser
#maybe don't need

#get configuration
config = ConfigParser()
config.read('config.ini')

subToPull = config.get('default','subreddit')
token = config.get('default','token')
bot_id = config.get('default','bot_id')


#get the URL of the best pupper pic
reddit = praw.Reddit('pupperParser')
subreddit = reddit.subreddit(subToPull)
for submission in subreddit.hot(limit=2):
    imgURL = submission.url

#determine content type of the image
response = requests.get(imgURL)
with open('/tmp/pupper','wb') as f:
	f.write(response.content)
contType = response.headers['Content-Type']

#upload image to GroupMe
data = open('/tmp/pupper','rb').read()

res1 = requests.post("https://image.groupme.com/pictures", params = {'token':token,'Content-Type':contType}, files = {'file':data})

#get the URL
midURL = res1.json().get('payload').get('picture_url')

#send a message to the GroupMe with the image
curlpackage = '{"text":"Here is the daily pupper Yashes:","bot_id":"' + bot_id +',"attachments":[{"type":"image","url":"'+midURL+'"}]}'
apiurl = 'https://api.groupme.com/v3/bots/post'

requests.post(apiurl,data=curlpackage)