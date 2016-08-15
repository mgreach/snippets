#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from grab import Grab
import urllib
import json
import pprint
import re
from HTMLParser import HTMLParser
from random import randrange


def random_insert(lst, item):
    if item not in lst:
        lst.insert(randrange(len(lst) + 1), item)


def snippets(keyword):
    contents = []
    images = []
    rich_text = []
    reviews = []
    result = ''
    content_url = 'https://www.googleapis.com/customsearch/v1element?key=' \
                  'AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&cx=partner-pub-2114605467104271:6649524146&num=' \
                  '20&prettyPrint=false&hl=ru&q=' + urllib.quote_plus(
        keyword.encode('utf-8')) + '&googlehost=www.google.com'
    g = Grab()
    g.setup(timeout=0, connect_timeout=180)
    g.setup(
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    g.go(content_url)
    data = json.loads(g.response.body)
    for snippet in data['results']:
        content_string = snippet['contentNoFormatting'].replace('*', '').replace('"', '') \
            .replace('...', '.').replace('/', '').replace('[', '').replace(']', '')
        print content_string
        if 'richSnippet' in snippet:
            rich_snippet = snippet['richSnippet']
            if 'cseImage' in rich_snippet:
                images.append(rich_snippet['cseImage']['src'])
            if 'metatags' in rich_snippet:
                if 'ogDescription' in rich_snippet['metatags']:
                    text_rich = rich_snippet['metatags']['ogDescription'].replace('*', '').replace('"', '') \
                        .replace('...', '.').replace('/', '').replace('[', '').replace(']', '').replace("'", '')
                    # rich_text.append(text_rich)
                    print text_rich
                    random_insert(contents, text_rich)
            if 'review' in rich_snippet:
                for item in rich_snippet['review']:
                    if 'reviewbody' in item:
                        review = item['reviewbody'].replace('*', '').replace('"', '') \
                            .replace('...', '.').replace('/', '').replace('[', '').replace(']', '').replace("'", '')
                        random_insert(contents, review)
        random_insert(contents, content_string)
    for line in contents:
        line = HTMLParser().unescape(re.sub('<[^<]+?>', '', line))
        result += ' ' + line
    result = result.replace('&', '').replace('*', '').replace('"', '') \
        .replace('...', '.').replace('/', '').replace('[', '').replace(']', '').replace("'", '')
    context = {'text': result, 'images': images}
    return context


def index(request):
    keyword = request.GET.get('key', '')
    context = snippets(keyword)
    # return HttpResponse(json.dumps(context).decode('unicode-escape').encode('utf8'))
    return HttpResponse(json.dumps(context))