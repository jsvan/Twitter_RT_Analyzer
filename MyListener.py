from tweepy import StreamListener
import json
import TwitterSQLite
import time
import random

class OutListener(StreamListener):
    #
    # overriding https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
    #
    # Documentation of what status fields are can be found :
    #  https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    #
    db = TwitterSQLite.TwitterDB()

    def on_status(self, status):
        print("status received")
        print(status.text)
        print("NAME:", status._json["user"]["screen_name"], '\n')
        #self.print_status(status._json)
        self.db.add_status(status._json, to_commit=True)
        self.add_retweeters(status._json["user"]["screen_name"], status._json["user"]["id_str"])
        print('\n ~~~ *** ~~~ \n\n')
        time.sleep(2)
        if random.random() < 0.02:
            raise ValueError('Time to update following list + restart')
        return True

    def on_exception(self, exception):
        print('EXCEPTION: \n', exception)
        return True

    def on_timeout(self):
        print("Timeout")

    def on_disconnect(self, notice=''):
        self.db.on_end()
        print('Disconnected')

    def print_status(self, toPrint, spacing=0):
        for k in toPrint.keys():
            val = toPrint[k]
            if type(val) is dict:
                print(' '*spacing, k,': ')
                self.print_status(val, spacing+4)
            elif type(val) is list:
                print(' '*spacing, k, ': ')
                for itm in val:
                    if type(itm) is dict:
                        self.print_status(itm, spacing+4)
                    else:
                        print(' '*spacing, k,': ', itm)
            else:
                print(' '*spacing, k, ': ', val)

    def on_error(self, status_code):
        print("on_error", status_code)
        time.sleep(10)
        return True

    def save_status(self, status):
        with open('tweet_dataset.json', 'a') as F:
           json.dump(status, F)
           F.write('\n')

    def add_retweeters(self, name, id):
        with open('follow_ids.json', 'r+') as F:
            following = json.load(F)
            if name not in following:
                print("ADDING", name, id)
                following[name] = id
            F.seek(0)
            json.dump(following, F)
