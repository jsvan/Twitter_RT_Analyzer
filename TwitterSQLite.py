import sqlite3

class TwitterDB:
  TWEET_TBL                           = "tweet_tbl"
  USER_TBL                            = "user_tbl"
  COORD_TBL                           = "coord_tbl"
  PLACE_TBL                           = "place_tbl"
  BOUNDING_BOX_TBL                    = "bounding_box_tbl"
  HASHTAG_TBL                         = "hashtag_tbl"
  TWEET_2_HASHTAG_TBL                 = "tweet_2_hashtag_tbl"

  boundingBoxId = 0
  coordId = 0

  def __init__(self):
    self.db, self.cursor      = self.on_start()

  def on_end(self):
    try:
        z = self.cursor.execute("SELECT COUNT(*) FROM tweet_tbl;")
        for i in z.fetchall():
            print("We have", i[0], "tweets!")
    except sqlite3.ProgrammingError:
        pass
    print("Disconnecting")
    self.db.close()





  def on_start(self):
    self.db = sqlite3.connect('twitter.db')
    self.cursor = self.db.cursor()
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_tbl(
            id_str                    STRING PRIMARY KEY,
            name                      STRING(30),
            screen_name               STRING(20),
            location                  STRING,
            url                       STRING,
            description               STRING,
            verified                  BOOLEAN,
            followers_count           INTEGER,
            friends_count             INTEGER,
            statuses_count            INTEGER,
            created_at                STRING,
            geo_enabled               BOOLEAN,
            lang                      STRING,
            contributors_enabled      BOOLEAN,
            default_profile           BOOLEAN,
            withheld_in_countries     STRING
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS hashtag_tbl(
            hashtag                   STRING PRIMARY KEY
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coord_tbl(
            id                        INTEGER PRIMARY KEY,
            longitude                 INTEGER,
            latitude                  INTEGER
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bounding_box_tbl(
            id                        INTEGER PRIMARY KEY,
            bottom_left               INTEGER,
            top_left                  INTEGER,
            top_right                 INTEGER,
            bottom_right              INTEGER,
            FOREIGN KEY(bottom_left)  REFERENCES coord_tbl(id),
            FOREIGN KEY(top_left)     REFERENCES coord_tbl(id),
            FOREIGN KEY(top_right)    REFERENCES coord_tbl(id),
            FOREIGN KEY(bottom_right) REFERENCES coord_tbl(id)
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS place_tbl(
            id_str                    STRING PRIMARY KEY,
            url                       STRING,
            place_type                STRING,
            full_name                 STRING,
            country                   STRING,
            bounding_box              INTEGER,
            FOREIGN KEY(bounding_box) REFERENCES bounding_box_tbl(id)
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweet_2_hashtag_tbl(
            id                        INTEGER PRIMARY KEY,
            tweet_id                  STRING,
            hashtag_id                STRING,
            FOREIGN KEY(tweet_id)     REFERENCES tweet_tbl(id_str),
            FOREIGN KEY(hashtag_id)   REFERENCES hashtag_tbl(id_str)
    );''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweet_tbl(
            created_at                STRING,
            id_str                    STRING PRIMARY KEY,
            text                      STRING,
            source                    STRING,
            in_reply_to_status_id_str STRING,
            in_reply_to_user_id_str   STRING,
            in_reply_to_screen_name   STRING,
            user                      STRING,
            coordinates               STRING,
            place                     STRING,
            quoted_status_id_str      STRING,
            is_quote_status           BOOLEAN,
            quoted_status             STRING,
            retweeted_status          BOOLEAN,
            quote_count               INTEGER,
            reply_count               INTEGER,
            retweet_count             INTEGER,
            favorite_count            INTEGER,
            favorited                 BOOLEAN,
            retweeted                 BOOLEAN,
            lang                      STRING,
            FOREIGN KEY(user)         REFERENCES user_tbl(id_str),
            FOREIGN KEY(coordinates)  REFERENCES coord_tbl(id_str),
            FOREIGN KEY(place)        REFERENCES place_tbl(id_str),
            FOREIGN KEY(quoted_status)  REFERENCES tweet_tbl(id_str)
    );''')
    self.boundingBoxId = [x for x in self.cursor.execute("SELECT Count(*) FROM bounding_box_tbl;")][0][0]
    self.coordId       = [x for x in self.cursor.execute("SELECT Count(*) FROM coord_tbl;")][0][0]
    return self.db, self.cursor


  def json_val(self, json, tag):
    if tag in json:
        return json[tag]
    return 'NULL'

  def add_status(self, tweet_json, to_commit = False):
    if tweet_json is 'NULL' or not tweet_json:
        return 'NULL'
    tweet_id = self._add_tweet(tweet_json)
    hashtag_list = tweet_json["entities"]["hashtags"]
    if hashtag_list:
        hashtag_list = [x['text'] for x in hashtag_list]
        self._add_tweet_2_hashtags(tweet_json['id_str'], hashtag_list)
    if to_commit:
        self.db.commit()
    return tweet_id

  def _add_place(self, place_json):
    if place_json is 'NULL' or not place_json:
        return 'NULL'
    cmd = '''
        INSERT OR IGNORE INTO place_tbl VALUES(
            ?, ?, ?, ?, ?, ?
    );'''
    self.cursor.execute(cmd, (self.json_val(place_json, 'id_str'), self.json_val(place_json, 'url'), self.json_val(place_json, 'place_type'), self.json_val(place_json, 'full_name'), self.json_val(place_json, 'country'), self._add_bounding_box(self.json_val(place_json, "bounding_box"))))
    return place_json['id_str']

  def _add_bounding_box(self, bb_json):
    if bb_json is 'NULL' or not bb_json:
        return 'NULL'
    self.boundingBoxId += 1
    cmd = '''
        INSERT OR IGNORE INTO bounding_box_tbl VALUES(
            ?, ?, ?, ?, ?
        );'''
    self.cursor.execute(cmd, ( self.boundingBoxId,
                    self._add_coord(bb_json['coordinates'][0][0]),
                    self._add_coord(bb_json['coordinates'][0][1]),
                    self._add_coord(bb_json['coordinates'][0][2]),
                    self._add_coord(bb_json['coordinates'][0][3])))
    return self.boundingBoxId

  def _add_coord(self, coord_json):
    if coord_json is 'NULL' or not coord_json:
        return 'NULL'
    self.coordId +=1
    cmd = '''
        INSERT OR IGNORE INTO coord_tbl VALUES(
            ?, ?, ?
        );'''
    self.cursor.execute(cmd, (self.coordId,
                    coord_json[0],
                    coord_json[1]))
    return self.coordId

  def _add_user(self, user_json):
    if user_json is 'NULL' or not user_json:
        return 'NULL'
    cmd = '''
        INSERT OR IGNORE INTO user_tbl VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );'''
    self.cursor.execute(cmd, (user_json['id_str'],
                    self.json_val(user_json, 'name'),
                    self.json_val(user_json, 'screen_name'),
                    self.json_val(user_json, 'location'),
                    self.json_val(user_json, 'url'),
                    self.json_val(user_json, 'description'),
                    self.json_val(user_json, 'verified'),
                    self.json_val(user_json, 'followers_count'),
                    self.json_val(user_json, 'friends_count'),
                    self.json_val(user_json, 'statuses_count'),
                    self.json_val(user_json, 'created_at'),
                    self.json_val(user_json, 'geo_enabled'),
                    self.json_val(user_json, 'lang'),
                    self.json_val(user_json, 'contributors_enabled'),
                    self.json_val(user_json, 'default_profile'),
                    self.json_val(user_json, 'withheld_in_countries')  ))
    return user_json['id_str']

  def _add_tweet(self, json):
    if json is 'NULL' or not json:
        return 'NULL'
    cmd = '''
        INSERT OR IGNORE INTO tweet_tbl VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );'''
    self.cursor.execute(cmd, (json['created_at'],
                    json['id_str'],
                    json['text'],
                    json['source'],
                    json['in_reply_to_status_id_str'],
                    json['in_reply_to_user_id_str'],
                    json['in_reply_to_screen_name'],
                    self._add_user(json['user']),
                    self._add_coord(json['coordinates']),
                    self._add_place(json['place']),
                    self.json_val(json, 'quoted_status_id_str'),
                    json['is_quote_status'],
                    self.add_status(self.json_val(json, 'quoted_status')),
                    self.add_status(self.json_val(json, 'retweeted_status')),
                    json['quote_count'],
                    json['reply_count'],
                    json['retweet_count'],
                    json['favorite_count'],
                    json['favorited'],
                    json['retweeted'],
                    json['lang']))
    return json['id_str']

  def _add_hashtag(self, hashtag):
    if hashtag is 'NULL' or not hashtag:
        return 'NULL'
    cmd = "INSERT OR IGNORE INTO hashtag_tbl VALUES(?);"
    self.cursor.execute(cmd, (hashtag, ))
    return hashtag

  def _add_tweet_2_hashtags(self, id_str, hashtag_list):
    cmd = "INSERT OR IGNORE INTO tweet_2_hashtag_tbl VALUES( NULL, ?, ?);"
    for hashtag in hashtag_list:
        self.cursor.execute(cmd, ( id_str, self._add_hashtag(hashtag)))
