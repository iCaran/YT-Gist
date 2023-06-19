#!/usr/bin/env python
# coding: utf-8

# modified from veeravignesh1's YouTube-Summarizer
# original: https://github.com/veeravignesh1/YouTube-Summarizer/

###################################################################################
# Module Imports
import webvtt
import yt_dlp
import requests
import spacy
from bardapi import Bard
import os
import sys
import colorama
from colorama import Fore, Style
from gensim.summarization.summarizer import summarize as gensim_based
def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip()
    return token

# Specify the file path where the token is stored
token_file_path = 'token.txt'

# Check if the token file exists
if not os.path.exists(token_file_path):
    print('Token file not found:', token_file_path)
    print('Please create a file named "token.txt" and store your token in it.')
    exit()

# Read the token from the file
token = read_token_from_file(token_file_path)

bard = Bard(token=token)

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

    title = info_dict['title']

    # Auto generated captions are less likely to be accurate than creator/crowd provided ones.
    # The tool first checks for proper English captions, and if none is found, uses auto-generated ones.
    # If the code proceeds with auto-gen caps, this flag is set to true and it is used to warn the user:
    # that the summary based upon this caption may be more inaccurate than less.
    flag=0

    print(info_color + "Extracting subtitle url...")

    try:
        if len(info_dict.get('subtitles')) != 0:
            subtitles = info_dict.get('subtitles')
            try:
                for lang in subtitles:
                    if lang.startswith('en'):
                        en_subtitles_url = subtitles[lang][-1]['url']
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

    print(info_color + "Downloading subtitles...")

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

    doc = nlp(text)
    text = "\n".join([sent.text for sent in doc.sents])
    return gensim_based(text=text, ratio=frac)

def ai_summary(text_to_summarize, title, flag):
    # Call the API to generate the summary
    prompt = "The following text is the extracted captions of a video, please summarise this: \n\n"
    summary = bard.get_answer(prompt+text_to_summarize)['content']

    warned=0

    if flag and "Response Error" not in summary:
        print(info_color + "Guessing summary accuracy based on video title...")
        selfcheck = "Do you think the title of the video: '"+title+"' matches this ai-generated summary? Respond with 'Yes' or 'No' :- \n"+summary+""
        response = bard.get_answer(selfcheck)['content']
        if response.startswith("No"):
            print(warning_color + "\n\n ||| This summary is generated over auto-generated captions, which are in itself prone to be off by small or, quite often, large amount, from the actual context of the video. This summary therefore generated has likely compounded the errors and may be wildly off the mark! |||")
            warned=1
    return summary, warned

##################################################################################

def on_submit(url):
    global frac, current, folder
    frac = float(1)
    current = os.getcwd()
    folder = current
    os.chdir(folder)
    try:
        corpus, title, flag = get_caption(url)
        print(info_color + "Captions Downloaded...")
    except:
        return
    with open("corpus.txt", 'w+') as c:
        print(corpus, file=c)
        print(info_color + "Corpus generated from captions...")
    # Calling the main summarizer function
    print(info_color + "Generating NLP based summary from corpus")
    nlp_summary = summarizer(corpus, frac)
    print("Generating AI summary...")
    aiSummary, warned = ai_summary(nlp_summary, title, flag)
    while ("Response Error" in aiSummary[0] or "Response Error" in aiSummary):
        print(info_color + "Too long, reducing length and trying again...")
        frac -= 0.1
        if frac<0.1:
            print("unsuccessful :(")
            return
        nlp_summary = summarizer(corpus, frac)
        aiSummary = ai_summary(nlp_summary, title, flag)
    print("---")
    print()
    if not isinstance(aiSummary, tuple):
        print(main_output_color + aiSummary)
    else:
        print(main_output_color + aiSummary[0])
    print("---")
    if flag==1 and warned==0:
        print(warning_color + "\n\n||| This summary was made using auto-generated captions, and it's likely that it's more or less inaccurate. |||")
    print()
    print(warning_color + "Summary contains about "+str(int(frac*100))+"% of the video content")
    print()

def main():
    global info_color, main_output_color, warning_color
    colorama.init()
    info_color = Fore.CYAN
    main_output_color = Fore.WHITE
    warning_color = Fore.MAGENTA
    if len(sys.argv) != 3 or sys.argv[1] != '-u':
        print('Usage: python summ.py -u <url>')
        return
    url = sys.argv[2]
    on_submit(url)

if __name__ == '__main__':
    main()
