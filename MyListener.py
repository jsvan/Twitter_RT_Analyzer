from tweepy import StreamListener
import json
import TwitterSQLite

class OutListener(StreamListener):
    #
    # overriding https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
    #
    # Documentation of what status fields are can be found :
    #  https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    #
    db = TwitterSQLite.TwitterDB()

    def on_status(self, status):
        print("status received\n")
        #print(status.text)
        self.print_status(status._json)
        self.db.add_status(status._json, to_commit=True)
        print('\n ~~~ *** ~~~ \n\n')
        return True

    def on_exception(self, exception):
        print('EXCEPTION: \n', exception)
        #return True

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
        return False

    def save_status(self, status):
        with open('tweet_dataset.json', 'a') as F:
           json.dump(status, F)
           F.write('\n')
