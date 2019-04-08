import json
credentials = {}
credentials['CONSUMER_KEY'] = 'ApQMfbH1kNGltaB667ZBOl4uY'
credentials['CONSUMER_SECRET'] = 'qfQav5RAXfrBC5v6Bq2QUNAwhcP4mzVhKdQ1a9OwFyNhX1Cf1J'
credentials['ACCESS_TOKEN'] = '1103737934811934722-zAumildiEx9kxrj5PPQlFTmfRA5AcT'
credentials['ACCESS_SECRET'] = '0pdJOKcj0ahKa6t7ZEg6OTa6KWt54Mzggy3xzISPb7EaO'


with open("twitter_cred.json", "w") as F:
    json.dump(credentials, F)

