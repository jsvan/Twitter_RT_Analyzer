import time
import json
import tweepy
import MyListener
import TwitterSQLite
import sys

CREDPATH    = "twitter_cred.json"
FOLLOWPATH  = "follow_ids.json"
VERBOSE     = True

class Reader:

    def _prepareCreds(self):
        with open(CREDPATH) as F:
            cred = json.load(F)
        auth = tweepy.OAuthHandler(cred['CONSUMER_KEY'], cred['CONSUMER_SECRET'])
        auth.set_access_token(cred['ACCESS_TOKEN'], cred['ACCESS_SECRET'])
        return auth

    def _prepareFollowing(self):
        with open(FOLLOWPATH, 'r') as F:
            following = json.load(F)
            if VERBOSE:
                print('Following: ', end='')
                for name in following.keys():
                    print(name, end=', ')
                print('')
            return list(following.values())

    def __init__(self):
        self.auth = self._prepareCreds()
        self.follow_ids = self._prepareFollowing()
        self.api      = tweepy.API(self.auth)
        self.lstnr    = MyListener.OutListener(self.api)
        #self.stream   = tweepy.Stream(auth=self.api.auth, listener=self.lstnr)


    def run(self):
        self.lstnr.db.on_start()
        self.stream   = tweepy.Stream(auth=self.api.auth, listener=self.lstnr)

        print("Sampling...")
        try:
            self.stream.filter(follow=self.follow_ids)
            while True:
                print('loop')
                self.stream.sample()
                time.sleep(1)


        except KeyboardInterrupt:
            #self.lstnr.on_disconnect()
            print(' Ending. ')
        except Exception as e:
            self.lstnr.on_disconnect()
            print(e)
            print(e.__doc__)
            time.sleep(1)

    def query(self, cmd, slow=False):
        c  = self.lstnr.db.cursor
        if 'drop' in cmd.lower():
            i = input("Are you sure you wish to drop? Y/n")
            if i is not 'Y':
                print("exiting")
                return
        Z = c.execute(cmd)
        titles = [tuple[0] for tuple in Z.description]
        for row in Z.fetchall():
            for i, ele in enumerate(row):
                print('{0:30} : '.format(titles[i]), ele)
            if slow:
                input(" ~~~ *** ~~~ \n")

    def exit(self):
        self.lstnr.on_disconnect()
        sys.exit()

    def tables(self):
        print("\ntweet_tbl\tuser_tbl\tcoord_tbl\tplace_tbl\tbounding_box_tbl\thashtag_tbl\ttweet_2_hashtag_tbl\n")

    def help(self):
        print("\n\t\t\t\t\t\t~~WELCOME~~")
        print("\t\t\t\t\t\tCommands:\n")
        print("> reader.run() \t\t\t\t\truns the twitter collection. Edit follow_ids.json to choose who to follow.")
        print("> reader.query( \"SQL_QUERY\", slow=False). \tSet the optional parameter slow to True for the output to be line by line, rather than a dump.")
        print("> reader.tables() \t\t\t\tgives you the tables")
        print("> reader.help() \t\t\t\tto see this menu again")
        print("> <ctrl>+c \t\t\t\t\tterminates .run() and .query()")
        print("> exit() \t\t\t\t\tterminates this program\n")


def exit():
    reader.exit()

reader = Reader()
reader.help()
