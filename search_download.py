from __future__ import unicode_literals
from googleapiclient import discovery
import youtube_dl
from TOKENS import YOUTUBE_TOKEN


# function to extract time (h, m, s)
def extract_time(string, to_replace=[], replace_with=[]):
    string = string.lower()
    for index in range(len(to_replace)):
        string = string.replace(
            to_replace[index].lower(),
            replace_with[index].lower()).lower()
    return string


# function to download video
def download_vid(videoid, title):
    # set out download link with the videoid
    prefix = "https://www.youtube.com/watch?v="
    link = prefix + videoid

    # set the parameters, such as title and converter
    ydl_opts = {'outtmpl': title, 'postprocessors': [
        {'key': 'FFmpegExtractAudio',
         'preferredcodec': 'mp3',
         'preferredquality': '192'}]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# function to search for youtube videos
def search_vid(query):
    youtube = discovery.build(
        'youtube', 'v3', developerKey=YOUTUBE_TOKEN, cache_discovery=False)
    # MAX_COUNT can be set to a max of 50, but i like lower values
    MAX_COUNT = 5
    nextPageToken = None
    search_by = query
    # send request
    request = youtube.search().list(q=search_by, part='snippet', type='video',
                                    maxResults=MAX_COUNT,
                                    pageToken=nextPageToken)
    # retrieve response
    response = request.execute()
    items = response['items']
    video_ids = []
    video_titles = []
    # iterate over the items so we only take the ones we want
    for each_item in items:
        for x, y in each_item.items():
            if isinstance(y, dict):
                for k, v in y.items():
                    if k == 'videoId':
                        video_ids.append(v)
                    if k == 'title':
                        video_titles.append(v)

    video_durations = []
    for _id in video_ids:
        # same as before but now taking only the content details
        requests = youtube.videos().list(part='snippet, contentDetails',
                                         id=_id)
        response = requests.execute()
        items = response['items']
        for each_item in items:
            for x, y in each_item.items():
                if isinstance(y, dict):
                    for k, v in y.items():
                        if k == "duration":
                            video_durations.append(extract_time(v,
                                                                to_replace=[
                                                                    'P', "T"],
                                                                replace_with=[
                                                                    '', '']))
    # output for the user
    i = 0
    a = ""
    for index in range(len(video_titles)):
        i += 1
        b = (f"{i}. {video_titles[index]} - Duração: ")
        c = (f"{video_durations[index]}\n")
        a = a + b + c
    return a, video_ids, video_titles
