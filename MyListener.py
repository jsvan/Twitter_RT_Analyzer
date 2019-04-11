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


    def initialize(self, quellenpath, retweeterspath):
        self.QUELLENPATH     = quellenpath
        self.RETWEETERSPATH  = retweeterspath
        self.quellen = self._prepareFollowing(self.QUELLENPATH)
        self.growRTs = False

    def setRetweetersGrowth(self, toGrow):
        self.growRTs = toGrow

    def on_status(self, status):
        try:
            print(status.text)
            print("NAME:", status._json["user"]["screen_name"], '\n')
            #self.print_status(status._json)
            self.db.add_status(status._json, to_commit=True)
            if self.growRTs:
                if self.add_retweeters(status._json) < 0.1:
                    print("~~~ *** ~~~ ^^^", end='')
                    return False  #END THIS STREAM, Updates Following list
        except Exception as e:
            self.print_status(status._json, debug=True)
            print(e)
            print(e.__doc__)
            print("onstatus")
            return False
        print(' ~~~ *** ~~~ \n')
        time.sleep(2)
        return True

    def on_exception(self, exception):
        print('EXCEPTION: \n', exception)
        return True

    def on_timeout(self):
        print("Timeout")

    def on_disconnect(self, notice=''):
        self.db.on_end()
        print('Disconnected')

    def print_status(self, toPrint, debug=False, spacing=0):
        for k in toPrint.keys():
            val = toPrint[k]
            if type(val) is dict:
                print(' '*spacing, k,': ')
                self.print_status(val, debug, spacing+4)
            elif type(val) is list:
                print(' '*spacing, k, ': ')
                for itm in val:
                    if type(itm) is dict:
                        self.print_status(itm, debug, spacing+4)
                    else:
                        if debug:
                            print(' '*spacing, k,': ', itm, type(itm))
                        else:
                            print(' '*spacing, k,': ', itm)
            else:
                if debug:
                    print(' '*spacing, k, ': ', val, type(val))
                else:
                    print(' '*spacing, k, ': ', val)

    def on_error(self, status_code):
        if status_code is '420':
            status_code = '420: Rate Limited (Request from Twitter)'
        print("on_error", status_code)
        time.sleep(10)
        return True

    def save_status(self, status):
        with open('tweet_dataset.json', 'a') as F:
           json.dump(status, F)
           F.write('\n')

    def add_retweeters(self, status_json):
        if "retweeted_status" in status_json and "id_str" in status_json["retweeted_status"]["user"] and status_json["retweeted_status"]["user"]["id_str"] in self.quellen:
            name = status_json["user"]["screen_name"]
            id = status_json["user"]["id_str"]
            with open(self.RETWEETERSPATH, 'r+') as F:
                following = json.load(F)
                if name not in following:
                    print("ADDING", name, id)
                    following[name] = id
                F.seek(0)
                json.dump(following, F)
            return random.random()
        else:
            return 1

    def _prepareFollowing(self, path):
        with open(path, 'r') as F:
            following = json.load(F)
        return list(following.values())
