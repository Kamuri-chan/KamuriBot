def get_hollo_video():
    import feedparser
    print("getting feed...")
    feed = feedparser.parse(r"https://storage.googleapis.com/matome-a7b0d.appspot.com/public/feed_pI6WIBlhnJBEGHZL8YHw")
    return feed


def get_titles(feed):
    titles = []
    print("Working on titles...")
    for k, v in feed.items():
        if k == "entries":
            for x in feed['entries']:
                for key, value in x.items():
                    if key == "title":
                        titles.append(value.strip())
    return titles


def get_urls(titles):
    from get_yt_link import search
    res = {}
    for index in range(0, 5):
        print("Getting link ", index + 1, " of 5")
        fun = True
        while fun:
            try:
                res[titles[index]] = search(titles[index])
                fun = False
            except KeyError:
                pass

    return (res)
