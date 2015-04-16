#!/usr/bin/python

import urllib2
import json
import datetime

FILENAME = "stocktwits.json" # change as necessary

names = ["AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM", "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "NVS", "TM", "PTR", "WFC", "BABA",  "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP"]

def get_tweets(ticker):
    url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
    connection = urllib2.urlopen(url)
    data = connection.read()
    connection.close()
    return json.loads(data)

def get_tweets_list(tickers):
    ret = {}
    for ticker in tickers:
        print "Getting data for", ticker
        try:
            data = get_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = data['messages']
            ret.update({symbol : msgs})
        except Exception as e:
            print e
            print "Error getting", ticker
    return ret

# schema for original and msgs: ticker (key) : msgs (value, list)
def append(original, msgs):
    print "Appending tweets"
    for ticker in msgs.keys():
        if ticker not in original.keys():
            original[ticker] = msgs[ticker]
        else:
            for msg in msgs[ticker]:
                if msg not in original[ticker]: # check for duplicates
                    original[ticker].append(msg)
    return original

def cull(original, age_limit=26):
    # cull all tweets over age_limit days old
    print "Culling tweets that are more than", age_limit, "days old"
    threshold = datetime.datetime.now() - datetime.timedelta(age_limit)
    result = {}
    for ticker in original.keys():
        result[ticker] = []
        for msg in original[ticker]:
            dt = datetime.datetime.strptime(msg["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if dt >= threshold:
                result[ticker].append(msg)
    return result

def read_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_to_file(filename, d):
    with open(filename, 'w+') as f:
        print "Dumping JSON to", filename
        json.dump(d, f)

if __name__ == "__main__":
    old = read_from_file(FILENAME)
    new = get_tweets_list(names)
    new = append(old, new)
    new = cull(new)
    write_to_file(FILENAME, new)
