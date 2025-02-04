"""
A wrapper aaround external requests to APIs
"""
import json
import logging
import os
import urllib
import random
import re

# from googlesearch import search_images Need to figure out how to install this

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# GOOGLE API KEY info can be found here: https://developers.google.com/custom-search/
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GOOGLE_CUSTOM_SEARCH_KEY = os.environ['GOOGLE_CUSTOM_SEARCH_KEY']

# The Microsoft Azure subscription key
BING_SUBSCRIPTION_KEY = os.environ['BING_SUBSCRIPTION_KEY']
# The Custom Search API (uses bing) in Mircorsoft Azure to use
BING_CUSTOM_SEARCH_KEY = os.environ['BING_CUSTOM_SEARCH_KEY']

# Giphy API Key
GIPHY_API_KEY = os.environ['GIPHY_API_KEY']

# Define the URL of the targeted Slack API resource.
# We'll send our replies there.
SLACK_URL = "https://slack.com/api/"

def submit_slack_request(data, chat_action):
    """
    Submit request obj to slack
    data: a dict object to be placed in the JSON body
    """
    # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(SLACK_URL + chat_action)
    # Add a header mentioning that the text is JSON.
    request.add_header(
        "Content-Type",
        "application/json"
    )
    request.add_header(
        "Authorization", 'Bearer {}'.format(BOT_TOKEN),
    )

    # Fire off the request!
    return urllib.request.urlopen(request, json.dumps(data).encode('utf-8')).read()

def anime_news_network_search(command, query):
    """
    search anilist for series info
    """
    params = urllib.parse.urlencode({
        'id':155,
        'search': query,
        'type': command
    })

    data = urllib.request.urlopen(r'https://www.animenewsnetwork.com/encyclopedia/reports.xml?' + params).read().decode('utf-8')
    show_ids = re.search(r"<id>(\d+)</id>", data)
    if show_ids is not None:
        return f"https://www.animenewsnetwork.com/encyclopedia/{command}.php?id={''.join(i for i in show_ids.groups(1) if i.isdigit())}"

    return None

def google_image_search(query):
    """
    Submit a search to google for images
    :query what to query for
    """
    params = urllib.parse.urlencode({
        'q': query,
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CUSTOM_SEARCH_KEY,
        'num': 10
    })
    data = json.loads(urllib.request.urlopen("https://www.googleapis.com/customsearch/v1?" + params).read())
    if 'items' in data:
        return random.choice(data["items"])["pagemap"]["cse_image"][0]['src']

    return None

def bing_image_search(query):
    """
    Submit a search to bing for images
    :query what to query for
    """
    params = urllib.parse.urlencode({
        'q': query,
        'count': 10,
        'mkt': 'en-US',
        'customconfig': BING_CUSTOM_SEARCH_KEY
    })

    request = urllib.request.Request('https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/images/search?' + params)
    request.add_header("Ocp-Apim-Subscription-Key", BING_SUBSCRIPTION_KEY)

    data = json.loads(urllib.request.urlopen(request).read())

    if 'value' in data and data['value']:
        return random.choice(data["value"])["contentUrl"]

    return None

def youtube_search(query):
    """
    Submit a search to youtube
    :query what to query for
    """
    params = urllib.parse.urlencode({
        'part': 'snippet',
        'q': query,
        'key': GOOGLE_API_KEY,
        'maxResults': 10
    })
    request = urllib.request.Request("https://www.googleapis.com/youtube/v3/search?" + params)
    request.add_header("Content-Type", "application/json")
    data = json.loads(urllib.request.urlopen(request).read())

    if 'items' in data:
        video_id = random.choice(data["items"])["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"

    return None

def wikipedia_search(query):
    """
    Submit a search to wikipedia
    :query what to query for
    """
    request_params = urllib.parse.urlencode({
        'action':'query',
        'list':'search',
        'srsearch': query,
        'format':'json'
    })

    request = urllib.request.Request('https://en.wikipedia.org/w/api.php?' + request_params)

    data = json.loads(urllib.request.urlopen(request).read())

    if 'query' in data:
        wikipedia_title = data['query']['search'][0]['title']
        link_title = '_'.join(wikipedia_title.split())
        return f"https://en.wikipedia.org/wiki/{link_title}"

    return None

def gify_search(command, query):
    """
    submit a search to giphy
    :query what to query for
    """

    limit = 10
    request_params = urllib.parse.urlencode({
        'api_key': GIPHY_API_KEY,
        'limit': limit,
        'q': query,
        'rating':'pg-13',
        'lang': 'en'
    })

    # I appended the s on purpose the end point expects gifs or stickers
    # and I'm being lazy
    url = f'https://api.giphy.com/v1/{command}s/search?'
    request = urllib.request.Request(url + request_params)
    response = json.loads(urllib.request.urlopen(request).read())

    if response['data']:
        return random.choice(response['data'])['images']['original']['url']

    return None

def return_status():
    """
    We always want to return status OK to the gateway API
    This has no bearing on the slack request. It's just
    stating that function completed OK
    """
    return {
        'statusCode': 200,
        'body':'no worries',
    }
