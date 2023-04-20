#!/usr/bin/env python
# coding: utf-8

# modified from veeravignesh1's YouTube-Summarizer
# original: https://github.com/veeravignesh1/YouTube-Summarizer/

"""
MIT License

Copyright (c) 2020 Veera Vignesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


###################################################################################
# Module Imports
import webvtt
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import yt_dlp
import requests
import pandas as pd
import numpy as np
import spacy
from summarizer import summarizeText

nlp = spacy.load("en_core_web_sm")


####################################################################################
# Function Block

def get_caption(url):
    global video_title

    # Create the YTDL object
    ydl = yt_dlp.YoutubeDL({'format': 'best'})

    # Download the video with subtitles
    info_dict = ydl.extract_info(url, download=False)

    video_title = info_dict['title']

    # Find the subtitle URL for the English subtitles
    subtitles = None
    en_subtitles_url = None

    try:
        if len(info_dict.get('subtitles')) != 0:
            subtitles = info_dict.get('subtitles')
            for lang in subtitles:
                if lang == 'en':
                    en_subtitles_url = subtitles[lang][-1]['url']
                    break
        elif len(info_dict.get('automatic_captions')['en-orig']) != 0:
            subtitles = info_dict.get('automatic_captions')['en-orig']
            en_subtitles_url = subtitles[-1]['url']
        elif len(info_dict.get('automatic_captions')['en']) != 0:
            subtitles = info_dict.get('automatic_captions')['en']
        else:
            print("No subtitles available")
    except:
        print("Could not extract subtitles, perhaps none is available")

    if subtitles:
        for lang in subtitles:
            if lang == 'en':
                en_subtitles_url = subtitles[lang][-1]['url']
                break

    # Download the English subtitles
    if en_subtitles_url:
        response = requests.get(en_subtitles_url)

        with open('test.en.vtt', 'wb') as f:
            f.write(response.content)
    else:
        print('English subtitles not found')
    corpus = []
    for caption in webvtt.read('test.en.vtt'):
        corpus.append(caption.text)
    corpus = "".join(corpus)
    corpus = corpus.replace('\n', ' ')

    return corpus


def summarizer(text, fraction):

    frac = fraction
    return tfidf_based(text, frac)


def tfidf_based(msg, fraction=0.3):
    # Creating Pipeline
    doc = nlp(msg)

    # Sent_tokenize
    sents = [sent.text for sent in doc.sents]

    # Number of Sentence User wants
    num_sent = int(np.ceil(len(sents) * fraction))

    # Creating tf-idf removing the stop words matching token pattern of only text
    tfidf = TfidfVectorizer(stop_words='english', token_pattern='(?ui)\\b\\w*[a-z]+\\w*\\b')
    X = tfidf.fit_transform(sents)

    # Creating a df with data and tf-idf value
    df = pd.DataFrame(data=X.todense(), columns=tfidf.get_feature_names_out())
    indexlist = list(df.sum(axis=1).sort_values(ascending=False).index)

    #     indexlist=list((df.sum(axis=1)/df[df>0].count(axis=1)).sort_values(ascending=False).index)

    # Subsetting only user needed sentence
    needed = indexlist[:num_sent]

    # Sorting the document in order
    needed.sort()

    # Appending summary to a list--> convert to string --> return to user
    summary = []
    for i in needed:
        summary.append(sents[i])
    summary = "".join(summary)
    summary = summary.replace("\n", '')
    return summary

##################################################################################

def on_submit():
    global url, frac, current, folder
    url = input("url: ")
    frac = float(1)
    current = os.getcwd()
    folder = current
    os.chdir(folder)
    corpus = get_caption(url)
    with open("corpus.txt", 'w+') as c:
        print(corpus, file=c)
    # Calling the main summarizer function
    summary = summarizer(corpus, frac)
    with open("summary.txt", "w") as s:
        print(summary, file=s)
    print(summary)
    s = summarizeText(summary)
    print(s)
    try:
        if s['sm_api_error']:
            if s['sm_api_error'] == 3:
                print("Video context is too short")
    except:
        with open("summ.txt", "w") as ss:
            print(s['sm_api_content'], file=ss)
        # os.remove(os.getcwd() + '/test.en.vtt')
        os.chdir(current)

on_submit()