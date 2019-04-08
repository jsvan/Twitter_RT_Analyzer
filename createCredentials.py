import json
credentials = {}
credentials['CONSUMER_KEY'] = ''
credentials['CONSUMER_SECRET'] = ''
credentials['ACCESS_TOKEN'] = ''
credentials['ACCESS_SECRET'] = ''


with open("twitter_cred.json", "w") as F:
    json.dump(credentials, F)

