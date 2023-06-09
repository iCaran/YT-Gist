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
import yt_dlp
import requests
import pandas as pd
import numpy as np
import spacy
from bardapi import Bard
import os

token = 'WwhnUax-lhwktorVFLEInJvkK-dax1IKRjyIkW3mDRj-fuZsaSt7OyOdeJiNiMPCI1Shdw.'
bard = Bard(token=token)

# Set the model, prompt, and parameters
model_engine = "text-davinci-002"
prompt = "Please summarize the following text:\n\n"

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

    print(info_dict.get('subtitles')['en'][-1]['url'])
    title = info_dict['title']

    flag=0

    try:
        if len(info_dict.get('subtitles')) != 0:
            subtitles = info_dict.get('subtitles')
            try:
                for lang in subtitles:
                    print(lang)
                    if lang.startswith('en'):
                        en_subtitles_url = subtitles[lang][-1]['url']
                        print("done")
                        break
                    elif len(info_dict.get('automatic_captions')['en-orig']) != 0:
                        subtitles = info_dict.get('automatic_captions')['en-orig']
                        en_subtitles_url = subtitles[-1]['url']
                    elif len(info_dict.get('automatic_captions')['en']) != 0:
                        subtitles = info_dict.get('automatic_captions')['en']
                        en_subtitles_url = subtitles[-1]['url']
            except:
                try:
                    en_subtitles_url = info_dict.get('subtitles')['en'][-1]['url']
                except:
                    pass

        elif len(info_dict.get('automatic_captions')) != 0:
            flag=1
            if len(info_dict.get('automatic_captions')['en-orig']) != 0:
                subtitles = info_dict.get('automatic_captions')['en-orig']
                en_subtitles_url = subtitles[-1]['url']
            elif len(info_dict.get('automatic_captions')['en']) != 0:
                subtitles = info_dict.get('automatic_captions')['en']
                en_subtitles_url = subtitles[-1]['url']
        else:
            print("No subtitles available")
    except:
        print("Could not extract subtitles, perhaps none is available")

    print(en_subtitles_url)

    # Download the English subtitles
    if en_subtitles_url:
        response = requests.get(en_subtitles_url)

        with open('test.en.vtt', 'wb') as f:
            f.write(response.content)
    else:
        print('English subtitles not found')
        return ""
    corpus = []
    for caption in webvtt.read('test.en.vtt'):
        corpus.append(caption.text)
    corpus = "".join(corpus)
    corpus = corpus.replace('\n', ' ')

    return corpus, title, flag


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

    """# Subsetting only user needed sentence
    needed = indexlist[:num_sent]"""

    # Assigning weights based on sentence position
    weights = [1.0] * len(indexlist)
    for i in range(len(indexlist)):
        weights[i] *= 1.0 - (i / len(indexlist))  # penalty for beginning
        weights[i] *= 1.0 - ((len(indexlist) - i - 1) / len(indexlist))  # penalty for end

    # Subsetting only user needed sentence
    num_sent = int(np.ceil(len(sents) * fraction))
    needed = [indexlist[i] for i in np.argsort(-df.sum(axis=1) * weights)[:num_sent]]

    # Sorting the document in order
    needed.sort()

    # Appending summary to a list--> convert to string --> return to user
    summary = []
    for i in needed:
        summary.append(sents[i])
    summary = "".join(summary)
    summary = summary.replace("\n", '')
    return summary

def ai_summary(text_to_summarize, title, flag):
    # Call the API to generate the summary
    prompt = "The following text is the extracted captions of a video, please summarise this: \n\n"
    summary = bard.get_answer(prompt+text_to_summarize)['content']

    print(flag)
    warned=0

    if flag and "Response Error" not in summary:
        selfcheck = "Do you think the title of the video: '"+title+"' matches this ai-generated summary? Respond with 'Yes' or 'No' :- \n"+summary+""
        response = bard.get_answer(selfcheck)['content']
        print(response)
        if response.startswith("No"):
            print("\n\n ||| This summary is generated over auto-generated captions, which are in itself prone to be off by small or, quite often, large amount, from the actual context of the video. This summary therefore generated has likely compounded the errors and may be wildly off the mark! |||")
            warned=1
    return summary, warned

##################################################################################

def on_submit():
    global url, frac, current, folder
    url = input("url: ")
    frac = float(1)
    current = os.getcwd()
    folder = current
    os.chdir(folder)
    try:
        corpus, title, flag = get_caption(url)
    except:
        return
    with open("corpus.txt", 'w+') as c:
        print(corpus, file=c)
    # Calling the main summarizer function
    nlp_summary = summarizer(corpus, frac)
    print(nlp_summary)
    aiSummary, warned = ai_summary(nlp_summary, title, flag)
    while ("Response Error" in aiSummary[0] or "Response Error" in aiSummary):
        frac -= 0.1
        print(frac)
        if frac<0.1:
            print("unsuccessful :(")
            return
        nlp_summary = summarizer(corpus, frac)
        print(nlp_summary)
        aiSummary = ai_summary(nlp_summary, title, flag)
    print()
    if not isinstance(aiSummary, tuple):
        print(aiSummary)
    else:
        print(aiSummary[0])
    if flag==1 and warned==0:
        print("\n\n||| This summary was made using auto-generated captions, and it's likely that it's more or less inaccurate. |||")
    print()

while 1:
    on_submit()