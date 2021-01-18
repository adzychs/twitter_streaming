import twitter,json,csv

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth, retry=True)

# setup a file to write to
csvfile = open('UK_mood_02_01Nv3.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter='|')

#  heres a function that takes out characters that can break
#  our import into Excel and replaces them with spaces
#  it also does the unicode bit
def clean(val):
    clean = ""
    if val:
        val = val.replace('|', ' ')
        val = val.replace('\n', ' ')
        val = val.replace('\r', ' ')
        clean = val
    return clean

#  here are some user id's, you can convert easily between the two here https://tweeterid.com/
#  these two are for foxNews and newsmax
u = "3131144855, 117777690, 2425571623, 747807250819981312, 61781260, 18020612, 80802900, 1168968080690749441, 885838630928994304, 20000725, 19825835, 153810216, 328634628, 61660254, 77234984, 80021045, 4764882552, 222748037, 112398730, 164226176, 20052899, 748453510048518145, 94701778, 120236641, 2382227424, 385306338, 19977759, 2797521996, 408454349, 113491007, 114505454, 15580900, 38281180, 545081356, 14104027, 15157283, 2583270112, 3056307455, 532241033, 36924726, 1325563478, 65357102, 3474472, 143212610, 105800463, 93880122, 14077382, 107722321, 368314502, 97402576, 300872531, 124270074, 462856853, 1865540413, 24211594, 240202308, 20362684, 20995648, 23424533, 1350441445, 576682647, 761499948890329088, 482866177, 16884084, 1179455215, 518660800, 32439211, 2173779986, 21713090, 48280657, 225857392, 23580445, 14379403, 318951712, 19397942, 1064867641578438656, 119200469, 1191697129154236416, 771271201419386880, 73340105, 217992827, 348486037, 1096805563, 14238933, 22904581, 493063948, 1724936154, 163191771, 494315232, 725726245317677056, 1110341743, 3291102293"

print ('Filtering the public timeline for track="%s"' % (u,))

twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

stream = twitter_stream.statuses.filter(follow=u)

for tweet in stream:
    # print (json.dumps(tweet, indent=1)) # for debugging purposes

    if tweet['truncated']:
        tweet_text = tweet['extended_tweet']['full_text']
    else:
        tweet_text = tweet['text']

    if 'retweeted_status' in tweet:
        rt_prefix = 'RT @' + tweet['retweeted_status']['user']['screen_name'] + ': '
        if tweet['retweeted_status']['truncated']:
            tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            tweet_text = tweet['retweeted_status']['text']
        tweet_text = rt_prefix +  tweet_text
        if ('quoted_status' in tweet):
            quote_suffix =  tweet['quoted_status_permalink']['url']
            tweet_text = tweet_text + ' ' + quote_suffix

    if ('quoted_status' in tweet) and ('retweeted_status' not in tweet) :
        quote_suffix =  tweet['quoted_status_permalink']['url']
        tweet_text = tweet_text + ' ' + quote_suffix

    geo_coordinates = ""
    if tweet['coordinates']:
        geo_coordinates = tweet['coordinates']['coordinates']

    csvwriter.writerow([tweet['id_str'],
                        tweet['created_at'],
                        clean(tweet['user']['screen_name']),
                        clean(tweet_text),
                        tweet['user']['created_at'],
                        geo_coordinates,
                        tweet['user']['lang'],
                        tweet['in_reply_to_user_id_str'],
                        tweet['in_reply_to_screen_name'],
                        tweet['user']['id_str'],
                        tweet['in_reply_to_status_id_str'],
                        clean(tweet['source']),
                        tweet['user']['profile_image_url_https'],
                        tweet['user']['followers_count'],
                        tweet['user']['friends_count'],
                        tweet['user']['statuses_count'],
                        clean(tweet['user']['location']),
                        tweet['entities']]
                        )

    print('text: ', tweet_text) # just so we can see it runnning
